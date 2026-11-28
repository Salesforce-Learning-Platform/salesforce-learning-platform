#!/usr/bin/env python3
"""Content checks for this repository. Uses only the Python standard library.

    python3 .github/scripts/check_content.py              # relative links, anchors, Python and JSON code blocks
    python3 .github/scripts/check_content.py --external   # links to other websites (slow; runs weekly in CI)

Code blocks are parsed, never run. A block that is meant not to parse (for example, one that shows a
syntax error on purpose) can be listed in .github/content-check-exceptions.json with a reason.
"""
from __future__ import annotations

import argparse
import ast
import concurrent.futures
import hashlib
import html
import http.client
import json
import os
import re
import socket
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import warnings
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCEPTIONS = ROOT / ".github" / "content-check-exceptions.json"

FENCE = re.compile(r"^(?P<indent>[ \t]*)(?P<mark>`{3,}|~{3,})[ \t]*(?P<info>[^\n]*)$")
QUOTE = re.compile(r"^(?:[ \t]{0,3}>)+[ \t]?")
CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)((?:(?!\n[ \t]*\n).)+?)(?<!`)\1(?!`)", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
LINK_TEXT = r"\[(?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*\]"
DESTINATION = r"(<[^<>\n]*>|(?:[^()\s]|\((?:[^()\s]|\([^()\s]*\))*\))+)"
TITLE = r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^()]*\)))?"
INLINE_LINK = re.compile(LINK_TEXT + r"\(\s*" + DESTINATION + TITLE + r"\s*\)")
IMAGE = re.compile("!" + LINK_TEXT + r"\(\s*" + DESTINATION + TITLE + r"\s*\)")
REFERENCE = re.compile(r"^ {0,3}\[(?!\^)[^\]\n]+\]:[ \t]*(<[^<>\n]*>|\S+)", re.M)
HTML_TARGET = re.compile(r"<(?:a|img|source)\b[^>]*?\s(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
AUTOLINK = re.compile(r"<(https?://[^<>\s]+)>")
HTML_ANCHOR = re.compile(r"<[a-z][^>]*?\s(?:id|name)\s*=\s*[\"']([^\"']+)[\"']", re.I)
ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+(.*?))?[ \t]*$")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
PYTHON_LANGUAGES = ("python", "py", "python3")
JSON_LANGUAGES = ("json", "jsonc", "jsonl")


@dataclass
class Block:
    lang: str
    line: int
    code: str


@dataclass
class Document:
    path: Path
    prose: str  # the file with code blocks blanked, so line numbers still match
    blocks: list[Block] = field(default_factory=list)
    unclosed: int | None = None  # line of a code block that is never closed

    @property
    def name(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


def markdown_files() -> list[Path]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        capture_output=True, text=True, check=True,
    ).stdout
    return sorted(ROOT / p for p in out.split("\0") if p and (ROOT / p).is_file())


def parse(path: Path) -> Document:
    """Split a Markdown file into prose and fenced code blocks."""
    lines = path.read_text(encoding="utf-8").split("\n")
    prose: list[str] = []
    blocks: list[Block] = []
    fence = None  # (mark, indent, lang, first line number, collected lines, inside a quote)
    for number, line in enumerate(lines, 1):
        if fence:
            mark, indent, lang, start, body, quoted = fence
            content = QUOTE.sub("", line, count=1) if quoted else line
            closing = content.strip()
            if closing.startswith(mark) and not closing.strip(mark[0]):
                blocks.append(Block(lang, start, "\n".join(body)))
                fence = None
            else:
                body.append(content[len(indent):] if content.startswith(indent) else content.lstrip(" \t"))
            prose.append("")
            continue
        quoted = bool(QUOTE.match(line))
        match = FENCE.match(QUOTE.sub("", line, count=1) if quoted else line)
        if match and not (match["mark"][0] == "`" and "`" in match["info"]):
            lang = match["info"].split()[0].lower() if match["info"].split() else ""
            fence = (match["mark"], match["indent"], lang, number, [], quoted)
            prose.append("")
            continue
        prose.append(line)
    if fence:
        blocks.append(Block(fence[2], fence[3], "\n".join(fence[4])))
    return Document(path, "\n".join(prose), blocks, fence[3] if fence else None)


def without_code_and_comments(prose: str) -> str:
    keep_lines = lambda m: "\n" * m.group(0).count("\n")
    return CODE_SPAN.sub(keep_lines, COMMENT.sub(keep_lines, prose))


def links(doc: Document) -> list[tuple[int, str]]:
    """Every link target in the file's prose, with its line number."""
    text = without_code_and_comments(doc.prose)
    found = []
    for pattern in (INLINE_LINK, IMAGE, REFERENCE, HTML_TARGET, AUTOLINK):
        for match in pattern.finditer(text):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            found.append((text.count("\n", 0, match.start()) + 1, target))
    return sorted(set(found))


def heading_text(raw: str) -> str:
    """The text GitHub shows for a heading, which it turns into the heading's anchor."""
    spans: list[str] = []
    def protect(match):
        content = match.group(2)
        if content.startswith(" ") and content.endswith(" ") and content.strip():
            content = content[1:-1]
        spans.append(content)
        return f"\x00{len(spans) - 1}\x00"
    text = CODE_SPAN.sub(protect, re.sub(r"[ \t]+#+[ \t]*$", "", raw))
    text = re.sub("!" + LINK_TEXT + r"\([^)]*\)", "", text)
    text = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])*)\](?:\([^()]*(?:\([^()]*\))?[^()]*\)|\[[^\]]*\])", r"\1", text)
    text = re.sub(r"</?[A-Za-z][^<>\x00]*>", "", text)  # HTML tags; a "<" followed by a space is text
    text = re.sub(r"(?<![\w\\])(\*\*|__|\*|_)(?=\S)(.+?)(?<=\S)\1(?![\w])", r"\2", text)
    text = html.unescape(re.sub(r"\\([!-/:-@\[-`{-~])", r"\1", text))
    return re.sub("\x00(\\d+)\x00", lambda m: spans[int(m.group(1))], text).strip()


def slugify(text: str) -> str:
    """GitHub's anchor rule: lowercase, drop punctuation and symbols, turn spaces into hyphens."""
    keep = []
    for char in text.lower():
        category = unicodedata.category(char)
        if char in "- \u200c\u200d" or category[0] in "LM" or category in ("Nd", "Nl", "Pc"):
            keep.append(char)
    return "".join(keep).replace(" ", "-")


def anchors(doc: Document) -> set[str]:
    found: set[str] = set()
    seen: Counter = Counter()
    lines = without_html_comments(doc.prose).split("\n")
    for index, line in enumerate(lines):
        match = ATX_HEADING.match(line)
        raw = match.group(1) if match else None
        if raw is None and index and re.match(r"^ {0,3}(=+|-+)[ \t]*$", line):
            previous = lines[index - 1]
            if previous.strip() and not re.match(r"^\s*([#>|]|[-*+] |\d+[.)] )", previous) and "|" not in previous:
                raw = previous.strip()
        if raw is None:
            continue
        slug = slugify(heading_text(raw))
        candidate, count = slug, seen[slug]
        while candidate in found:
            count += 1
            candidate = f"{slug}-{count}"
        seen[slug] = count
        found.add(candidate)
    found.update(HTML_ANCHOR.findall(without_code_and_comments(doc.prose)))
    return found


def without_html_comments(prose: str) -> str:
    return COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), prose)


class Tree:
    """Case-sensitive path lookups, so a check on macOS agrees with the Linux runner and GitHub."""

    def __init__(self):
        self._names: dict[Path, set[str]] = {}

    def exists(self, path: Path) -> bool:
        current = ROOT
        for part in path.relative_to(ROOT).parts:
            if current not in self._names:
                self._names[current] = set(os.listdir(current)) if current.is_dir() else set()
            if part not in self._names[current]:
                return False
            current = current / part
        return True


def check_links(documents: dict[Path, Document]) -> tuple[list, Counter]:
    tree, anchor_cache, problems, counts = Tree(), {}, [], Counter()

    def anchors_of(path: Path) -> set[str]:
        if path not in anchor_cache:
            anchor_cache[path] = anchors(documents[path] if path in documents else parse(path))
        return anchor_cache[path]

    for path, doc in documents.items():
        for line, target in links(doc):
            if SCHEME.match(target) or target.startswith("//"):
                counts["external links (not checked here)"] += 1
                continue
            counts["relative links"] += 1
            file_part, _, fragment = target.partition("#")
            file_part = urllib.parse.unquote(file_part.split("?", 1)[0])
            if not file_part:
                destination = path
            else:
                base = ROOT if file_part.startswith("/") else path.parent
                destination = Path(os.path.normpath(base / file_part.lstrip("/")))
                if destination != ROOT and ROOT not in destination.parents:
                    problems.append((doc.name, line, f"link leaves the repository: {target}"))
                    continue
                if destination != ROOT and not tree.exists(destination):
                    problems.append((doc.name, line, f"broken link: {target}"))
                    continue
            if not fragment:
                continue
            counts["anchors"] += 1
            if destination.is_dir():
                destination = destination / "README.md"
            if destination.suffix.lower() != ".md":
                if not re.fullmatch(r"L\d+(-L\d+)?", fragment):
                    problems.append((doc.name, line, f"cannot check the anchor in: {target}"))
                continue
            if not destination.is_file() or urllib.parse.unquote(fragment) not in anchors_of(destination):
                problems.append((doc.name, line, f"missing heading for anchor: {target}"))
    return problems, counts


def block_hash(code: str) -> str:
    normal = "\n".join(line.rstrip() for line in code.strip("\n").split("\n"))
    return hashlib.sha256(normal.encode("utf-8")).hexdigest()[:16]


def strip_json_comments(code: str) -> str:
    """Remove // and /* */ comments outside strings, for JSON with comments (jsonc)."""
    return re.sub(r'("(?:\\.|[^"\\])*")|//[^\n]*|/\*.*?\*/', lambda m: m.group(1) or "", code, flags=re.S)


def syntax_error(block: Block) -> str | None:
    if block.lang in PYTHON_LANGUAGES:
        if block.code.lstrip().startswith(">>>"):
            return None  # an interactive session, not a script
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                compile(block.code, "<block>", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT, dont_inherit=True)
        except (SyntaxError, ValueError) as error:
            return f"Python block does not parse (line {getattr(error, 'lineno', '?')} of the block: {getattr(error, 'msg', error)})"
    elif block.lang in JSON_LANGUAGES:
        try:
            if block.lang == "jsonl":
                for number, line in enumerate(block.code.split("\n"), 1):
                    if line.strip():
                        try:
                            json.loads(line)
                        except ValueError as error:
                            raise ValueError(f"line {number} of the block: {error}")
            else:
                json.loads(strip_json_comments(block.code) if block.lang == "jsonc" else block.code)
        except ValueError as error:
            return f"{block.lang} block does not parse ({error})"
    return None


def check_code(documents: dict[Path, Document]) -> tuple[list, Counter]:
    allowed = json.loads(EXCEPTIONS.read_text(encoding="utf-8")) if EXCEPTIONS.exists() else []
    used: set[int] = set()
    problems, counts = [], Counter()
    for doc in documents.values():
        if doc.unclosed:
            problems.append((doc.name, doc.unclosed, "this code block is never closed, so the rest of the file renders as code"))
        for block in doc.blocks:
            if block.lang in PYTHON_LANGUAGES:
                counts["Python blocks"] += 1
            elif block.lang in JSON_LANGUAGES:
                counts["JSON blocks"] += 1
            error = syntax_error(block)
            if not error:
                continue
            digest = block_hash(block.code)
            match = next((i for i, e in enumerate(allowed) if e["file"] == doc.name and e["block"] == digest), None)
            if match is None:
                problems.append((doc.name, block.line, f"{error}. If it is meant not to parse, add "
                                 f'{{"file": "{doc.name}", "block": "{digest}", "reason": "..."}} to {EXCEPTIONS.relative_to(ROOT).as_posix()}'))
            else:
                used.add(match)
    for index, entry in enumerate(allowed):
        if index not in used:
            problems.append((EXCEPTIONS.relative_to(ROOT).as_posix(), 1, "unused exception (the block changed or now parses): "
                             f"{entry.get('file')} {entry.get('block')}"))
    counts["allowed exceptions"] = len(used)
    return problems, counts


# ---------------------------------------------------------------------------------------------------------------
# Links to other websites

SKIP_HOSTS = re.compile(r"(^|\.)(localhost|example\.(com|net|org)|example|test|invalid|local)$|^(127\.|0\.0\.0\.0|10\.|192\.168\.)|^::1$", re.I)
USER_AGENT = "Mozilla/5.0 (compatible; content-link-check)"
TIME_BUDGET = 35 * 60  # seconds; the weekly job is stopped after 45 minutes


def fetch(url: str) -> tuple[str, str]:
    """Return ("ok" | "dead" | "unverified" | "limited" | "unreachable", detail).

    "limited" and "unreachable" are also unverified; they tell check_host that the site is not answering
    properly. A temporary DNS failure is not "dead"."""
    parts = urllib.parse.urlsplit(url)
    safe = urllib.parse.urlunsplit(parts._replace(path=urllib.parse.quote(parts.path, safe="/%:@!$&'()*+,;=-._~"),
                                                  query=urllib.parse.quote(parts.query, safe="=&%:/?+,;@!$'()*-._~"), fragment=""))
    status, detail = "unverified", ""
    for attempt in range(3):
        pause = 5 * (attempt + 1)
        try:
            request = urllib.request.Request(safe, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8",
                                                            "Accept-Language": "en"})
            with urllib.request.urlopen(request, timeout=30) as response:
                response.read(1024)
                return "ok", str(response.status)
        except urllib.error.HTTPError as error:
            detail = f"HTTP {error.code}"
            if error.code in (404, 410):
                return "dead", detail
            status = "limited" if error.code == 429 else "unverified"
            if error.code not in (429, 500, 502, 503, 504):
                return status, detail
            retry_after = error.headers.get("Retry-After", "") if error.headers else ""
            if retry_after.isdigit():
                pause = max(pause, min(int(retry_after), 30))
        except urllib.error.URLError as error:
            if isinstance(error.reason, socket.gaierror) and error.reason.errno != socket.EAI_AGAIN:
                return "dead", f"the host name does not resolve ({error.reason})"
            status, detail = "unreachable", f"{error.reason}"
        except (OSError, http.client.HTTPException) as error:
            status, detail = "unreachable", f"{type(error).__name__}: {error}"
        except ValueError as error:
            return "unverified", f"{type(error).__name__}: {error}"
        if attempt < 2:
            time.sleep(pause)
    return status, detail


def check_host(host: str, urls: list[str], deadline: float) -> dict[str, tuple[str, str]]:
    """Check one site's URLs one at a time, with a pause between requests, so no site is hammered."""
    gap = 3.0 if host.endswith("wikipedia.org") else 1.0
    results, failures_in_a_row = {}, 0
    for index, url in enumerate(urls):
        if failures_in_a_row >= 3:
            results[url] = ("unverified", "not requested: the site kept rate limiting or not answering")
            continue
        if time.monotonic() > deadline:
            results[url] = ("unverified", "not requested: the time budget ran out")
            continue
        if index:
            time.sleep(gap)
        status, detail = fetch(url)
        failures_in_a_row = failures_in_a_row + 1 if status in ("limited", "unreachable") else 0
        results[url] = ("unverified" if status in ("limited", "unreachable") else status, detail)
    return results


def check_external(documents: dict[Path, Document]) -> int:
    where: dict[str, list[str]] = {}
    for doc in documents.values():
        for line, target in links(doc):
            if target.lower().startswith(("http://", "https://")):
                host = urllib.parse.urlsplit(target).hostname or ""
                if not SKIP_HOSTS.search(host) and not re.search(r"[<>{}]", target):
                    where.setdefault(target.split("#")[0], []).append(f"{doc.name}:{line}")
    hosts: dict[str, list[str]] = {}
    for url in sorted(where):
        hosts.setdefault((urllib.parse.urlsplit(url).hostname or "").lower(), []).append(url)
    print(f"checking {len(where)} URLs on {len(hosts)} sites", flush=True)
    results: dict[str, tuple[str, str]] = {}
    deadline = time.monotonic() + TIME_BUDGET
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        busiest_first = sorted(hosts.items(), key=lambda item: -len(item[1]))
        futures = {pool.submit(check_host, host, urls, deadline): host for host, urls in busiest_first}
        for future in concurrent.futures.as_completed(futures):
            host_results = future.result()
            results.update(host_results)
            if len(host_results) >= 20:
                print(f"  finished {futures[future]} ({len(host_results)} URLs)", flush=True)
    dead = sorted((u, d) for u, (s, d) in results.items() if s == "dead")
    unverified = sorted((u, d) for u, (s, d) in results.items() if s == "unverified")
    summary = ["## External links", "",
               f"{len(results)} URLs checked: {len(results) - len(dead) - len(unverified)} reachable, "
               f"{len(dead)} dead, {len(unverified)} could not be verified.", ""]
    for title, rows in (("Dead links (fix these)", dead), ("Could not be verified (check by hand)", unverified)):
        if rows:
            summary += [f"### {title}", "", "| URL | Result | Used in |", "|---|---|---|"]
            summary += [f"| {u} | {d.replace('|', '/')} | {', '.join(where[u][:3])}{' …' if len(where[u]) > 3 else ''} |" for u, d in rows]
            summary.append("")
    report = "\n".join(summary)
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as handle:
            handle.write(report + "\n")
    for url, detail in dead:
        for spot in where[url]:
            file, line = spot.rsplit(":", 1)
            annotate(file, int(line), f"dead link ({detail}): {url}")
    return 1 if dead else 0


def annotate(file: str, line: int, message: str) -> None:
    if os.environ.get("GITHUB_ACTIONS"):
        escaped = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error file={file},line={line}::{escaped}")
    else:
        print(f"{file}:{line}: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--external", action="store_true", help="check links to other websites instead")
    arguments = parser.parse_args()
    documents = {path: parse(path) for path in markdown_files()}
    if arguments.external:
        return check_external(documents)
    link_problems, link_counts = check_links(documents)
    code_problems, code_counts = check_code(documents)
    for file, line, message in sorted(link_problems + code_problems):
        annotate(file, line, message)
    counts = Counter({"Markdown files": len(documents)}) + link_counts + code_counts
    print("checked: " + ", ".join(f"{value} {key}" for key, value in counts.items()))
    total = len(link_problems) + len(code_problems)
    print("no problems found" if not total else f"{total} problem(s) found")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
