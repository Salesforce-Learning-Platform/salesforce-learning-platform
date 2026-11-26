# 🛡️ File System Security

## Correct Permissions Are Not Enough

[file-permissions.md](file-permissions.md) showed how a file system decides who may touch a file. A system whose permissions are all set correctly can still be attacked, for two reasons. First, a program often acts on names that someone else supplied or can change, and the file system checks the *program's* authority, not the attacker's: this is the confused deputy of the special-bits section, and it appears again below as a race between checking a name and using it, and as a path that climbs out of its folder. Second, permissions are enforced by the operating system alone: they say nothing about whether a file was changed by somebody who passed the checks, and they mean nothing to someone who reads the disk without the operating system. This lesson covers the two attacks, then the protections that do not rely on permissions (integrity fingerprints and disk encryption) and the principle of least privilege, which limits the damage when a defence fails, ending with a small audit tool. All code was run on CPython 3.9 on a Mac (macOS, Apple silicon) as an ordinary user; machine-dependent results are labelled.

## ⏱️ Races Between Checking and Using

A **time-of-check to time-of-use** (TOCTOU) bug is a race condition between checking the state of something (for example a permission) and using the result of that check; such races are common in Unix between operations on the file system ([Wikipedia: Time-of-check to time-of-use](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use)). It is the *check-then-act* race of [race-conditions.md](../deadlocks-and-concurrency/race-conditions.md), with a file system name in the middle: between the two calls, another process can change what the name means. The Python documentation warns about the commonest instance: calling `os.access` to check whether a file may be opened and then opening it creates a security hole, because the user might exploit the short interval between the two to manipulate the file, and it recommends the *EAFP* approach (easier to ask forgiveness than permission): just try the operation and handle the failure ([Python docs: `os.access`](https://docs.python.org/3/library/os.html#os.access)). The first example is a program that wants to claim a name only if nobody has claimed it yet. To make the unlucky schedule certain, a barrier holds each thread between its check and its action until the other has finished checking:

```python
import os
import stat
import subprocess
import tempfile
import threading

def claim_naively(path, who, results, pause=None):
    if not os.path.exists(path):                  # check: nobody has claimed the name yet
        if pause:
            pause.wait()                          # (to force the bad schedule) both threads finish checking first
        with open(path, "w") as handle:           # act: create it, and truncate it if it has appeared meanwhile
            handle.write(who)
        results[who] = "created it"
    else:
        results[who] = "found it"

with tempfile.TemporaryDirectory() as workshop:
    path = os.path.join(workshop, "lock")
    results, pause = {}, threading.Barrier(2)
    threads = [threading.Thread(target=claim_naively, args=(path, who, results, pause)) for who in "AB"]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(dict(sorted(results.items())))
```

```text
{'A': 'created it', 'B': 'created it'}
```

Both threads believe they created the file. Nothing forces this schedule in real life, but nothing prevents it either. The next block removes the barrier and lets eight threads start at the same instant, 2,000 times, counting in each round how many threads think they won. It compares the naive code with a single system call that checks and creates in one indivisible step: `os.open` with `O_CREAT | O_EXCL`, which fails with `EEXIST` if the path already exists (and does not follow a symbolic link at that path), so exactly one caller can succeed ([`open(2)`](https://man7.org/linux/man-pages/man2/open.2.html)). In Python's high-level `open`, mode `'x'` asks for the same thing, and `tempfile.mkstemp` relies on this flag for its guarantee that there are no races in creating the file ([Python docs: `tempfile`](https://docs.python.org/3/library/tempfile.html)):

```python
import collections

def claim_naively_at_once(path, who, results, gate):
    gate.wait()                                   # all threads start together
    claim_naively(path, who, results)

def claim_atomically(path, who, results, gate):
    gate.wait()
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)    # check and create in ONE step
    except FileExistsError:
        results[who] = "lost"
    else:
        os.close(descriptor)
        results[who] = "won"

def tournament(worker, success, rounds=2000, players=8):
    """In each round, how many threads think they got the name? Returns {number of winners: number of rounds}."""
    tally = collections.Counter()
    with tempfile.TemporaryDirectory() as workshop:
        for number in range(rounds):
            path = os.path.join(workshop, f"claim-{number}")
            results, gate = {}, threading.Barrier(players)
            threads = [threading.Thread(target=worker, args=(path, str(who), results, gate)) for who in range(players)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            tally[sum(1 for outcome in results.values() if outcome == success)] += 1
    return dict(sorted(tally.items()))

print("check, then create:", tournament(claim_naively_at_once, "created it"))
print("O_CREAT | O_EXCL  :", tournament(claim_atomically, "won"))
```

One run on the test machine printed:

```
check, then create: {2: 1, 3: 4, 4: 19, 5: 174, 6: 317, 7: 387, 8: 1098}
O_CREAT | O_EXCL  : {1: 2000}
```

The first line depends on timing and will differ from run to run and from machine to machine. In the run above no round had exactly one winner, and in nearly all of them five or more threads believed they had created the file. The second line does not depend on timing: in every round exactly one thread won, because the kernel makes the check and the creation a single step.

The second example is the classic attack on a program that wants to be careful about symbolic links. A service checks that the file it is asked to serve is not a link, then opens it. Between the two steps a local attacker replaces the file with a link to a file that the attacker may not read, but the service may. In the code, the argument `in_the_gap` stands for what the attacker does at that moment. The safer version asks the kernel to refuse links as part of the open itself (`O_NOFOLLOW`: if the final component of the path is a symbolic link, the open fails with `ELOOP`; links in earlier components are still followed, [`open(2)`](https://man7.org/linux/man-pages/man2/open.2.html)), and then examines the file it actually holds, with `fstat` on the descriptor, not the name:

```python
import errno

def serve_naive(path, in_the_gap):
    if os.path.islink(path):                         # check the name ...
        return "refused: symbolic link"
    in_the_gap()                                     # <- the attacker acts here
    with open(path) as handle:                       # ... then use the name, which may mean something else by now
        return handle.read()

def serve_safely(path, in_the_gap):
    in_the_gap()                                     # the same attack, at the same moment
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)      # the kernel refuses a link as part of the open
    except OSError as error:
        return f"refused: {errno.errorcode[error.errno]}"
    with os.fdopen(descriptor) as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):      # examine what we HOLD, not the name
            return "refused: not a regular file"
        return handle.read()

def make_site(workshop):
    public = os.path.join(workshop, "public.txt")
    secret = os.path.join(workshop, "secret.txt")
    with open(public, "w") as handle:
        handle.write("welcome page")
    with open(secret, "w") as handle:
        handle.write("the private key")
    def attacker():                                  # swap the file for a link to the secret
        os.unlink(public)
        os.symlink(secret, public)
    return public, attacker

for label, server in (("check, then open", serve_naive), ("open with O_NOFOLLOW", serve_safely)):
    for under_attack in (False, True):
        with tempfile.TemporaryDirectory() as workshop:
            public, attacker = make_site(workshop)
            answer = server(public, attacker if under_attack else (lambda: None))
            print(f"{label:<22} {'under attack' if under_attack else 'no attack':<13} -> {answer}")
```

```text
check, then open       no attack     -> welcome page
check, then open       under attack  -> the private key
open with O_NOFOLLOW   no attack     -> welcome page
open with O_NOFOLLOW   under attack  -> refused: ELOOP
```

The general rules follow from the two examples. *Do not check a name and then use the name*: try the operation and handle the error. *Do not test what a name leads to; test what you hold*: a name is looked up afresh on every use, while a descriptor identifies one file for as long as it is open ([files-and-directories.md](files-and-directories.md)). And ask the kernel for the guarantee you need (`O_EXCL`, `O_NOFOLLOW`) in the very call that does the work. On Linux, `openat2(2)` goes further and can block the resolution of symbolic links throughout the path ([`path_resolution(7)`](https://man7.org/linux/man-pages/man7/path_resolution.7.html)).

## 🧭 Path Traversal

A **path traversal** (or directory traversal, or "dot-dot-slash") attack exploits a program that builds a file name from text it received without validating it, so that components meaning "go to the parent directory" reach the operating system's file API ([Wikipedia: Path traversal](https://en.wikipedia.org/wiki/Path_traversal)). In Wikipedia's example, a PHP page includes a template from `/home/users/phpguru/templates/` named in a cookie; a visitor who sets the cookie to `../../../../../../../../../etc/passwd` makes the page include the system's password file. The web application is a confused deputy again: it may read many files, and the attacker chose only a name.

The obvious defences fail in interesting ways. Python's `os.path.join` *discards everything before an absolute segment*: if a segment is an absolute path, all previous segments are ignored ([Python docs: `os.path`](https://docs.python.org/3/library/os.path.html)). And a prefix test on the text is wrong, because a sibling folder can share the prefix:

```python
print(os.path.join("/srv/uploads", "/etc/hosts"))
print("/srv/uploads-private/x.txt".startswith("/srv/uploads"))
```

```text
/etc/hosts
True
```

A correct check first lets the file system do the resolving, with `os.path.realpath`, which returns the canonical path with every `..` resolved and every symbolic link eliminated, and then compares whole path *components* with `os.path.commonpath` (the Python documentation warns that its character-by-character relative, `commonprefix`, may return invalid paths). The block compares the naive version, which normalizes the dots and tests the prefix, with this one, on a small site that has a link that stays inside the upload folder, two links that leave it, and a sibling folder:

```python
def naive_join(base, user_path):
    """The common first attempt: join, tidy the dots, test the prefix."""
    target = os.path.normpath(os.path.join(base, user_path))
    if not target.startswith(base):
        raise PermissionError(user_path)
    return target

def safe_join(base, user_path):
    """The real path that `user_path` names inside `base`; PermissionError if it leads anywhere else."""
    base = os.path.realpath(base)
    target = os.path.realpath(os.path.join(base, user_path))     # resolves every .. and follows every symbolic link
    if os.path.commonpath([base, target]) != base:                # whole components, not characters
        raise PermissionError(user_path)
    return target

def build_site(root):
    for folder in ("uploads/notes", "uploads/docs", "uploads-private", "outside"):
        os.makedirs(os.path.join(root, folder))
    for name in ("uploads/notes/a.txt", "uploads/docs/c.txt", "uploads-private/x.txt", "outside/secret.txt"):
        with open(os.path.join(root, name), "w") as handle:
            handle.write(name)
    os.symlink("notes", os.path.join(root, "uploads", "inner-link"))                  # a link that stays inside
    os.symlink("../outside", os.path.join(root, "uploads", "out-link"))               # a link to a folder outside
    os.symlink("../outside/secret.txt", os.path.join(root, "uploads", "file-link"))   # a link to a file outside
    return os.path.join(root, "uploads")

def verdict(function, base, user_path):
    try:
        function(base, user_path)
        return "accepted"
    except PermissionError:
        return "refused"

with tempfile.TemporaryDirectory() as root:
    base = build_site(root)
    for user_path in ("notes/a.txt", "notes/../docs/c.txt", "inner-link/a.txt", "../outside/secret.txt", "/etc/hosts",
                      "notes/../../outside/secret.txt", "out-link/secret.txt", "file-link", "../uploads-private/x.txt"):
        print(f"{user_path:<32} naive: {verdict(naive_join, base, user_path):<9} safe: {verdict(safe_join, base, user_path)}")
```

```text
notes/a.txt                      naive: accepted  safe: accepted
notes/../docs/c.txt              naive: accepted  safe: accepted
inner-link/a.txt                 naive: accepted  safe: accepted
../outside/secret.txt            naive: refused   safe: refused
/etc/hosts                       naive: refused   safe: refused
notes/../../outside/secret.txt   naive: refused   safe: refused
out-link/secret.txt              naive: accepted  safe: refused
file-link                        naive: accepted  safe: refused
../uploads-private/x.txt         naive: accepted  safe: refused
```

The two versions agree on the plain attacks (`..`, an absolute path, and dots that climb out). The naive one is fooled by the three subtler cases: the two symbolic links that lead out of the folder and the sibling that shares the prefix; the safe one refuses all of them and accepts only paths that stay inside, even when they wander through `..` or an inner link on the way. Two cautions remain. A name that passes the check can still be changed before it is used, the TOCTOU race of the previous section, so a service that must be robust opens with `O_NOFOLLOW` or `openat2` and examines the descriptor as shown there. And the strongest defence does not rely on cleaning names: let the service run as a user who cannot read the secrets in the first place (least privilege, at the end of this file), so that a tricked deputy has little authority to misuse.

## 🔏 Integrity: Has Anything Changed?

Permissions say who *may* change a file; they cannot show that nobody *did*. A bug, a disk error, or an intruder who gained the right privileges all leave files altered with every permission check passed. A **cryptographic hash function** produces a short fixed-size fingerprint of any input, with two properties that make it useful here: a small change in the input results in a very different hash, so it is an efficient way to check whether two copies of data match, and finding two different inputs with the same hash is infeasible ([Wikipedia: Cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic_hash_function)). The example uses SHA-256, a member of the [SHA-2](https://en.wikipedia.org/wiki/SHA-2) family; an older function such as [MD5](https://en.wikipedia.org/wiki/MD5) became unusable for cryptographic applications because of its vulnerabilities. A *manifest* records the fingerprint of every file in a folder, and comparing a fresh manifest with an old one reports what changed, what disappeared, and what appeared:

```python
import hashlib

def fingerprint(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):      # in pieces: the file need not fit in memory
            digest.update(chunk)
    return digest.hexdigest()

def manifest(root):
    result = {}
    for folder, _, names in os.walk(root):
        for name in names:
            full_path = os.path.join(folder, name)
            result[os.path.relpath(full_path, root)] = fingerprint(full_path)
    return result

def compare(old, new):
    return {"changed": sorted(name for name in old if name in new and old[name] != new[name]),
            "missing": sorted(name for name in old if name not in new),
            "added": sorted(name for name in new if name not in old)}

with tempfile.TemporaryDirectory() as root:
    contents = {"salary.csv": b"ada,5000\nlin,4800\n", "notes.txt": b"meeting at ten\n", "logo.bin": b"\x00\x01\x02"}
    for name, data in contents.items():
        with open(os.path.join(root, name), "wb") as handle:
            handle.write(data)
    before = manifest(root)
    for name, digest in sorted(before.items()):
        print(f"{name:<11} {digest[:16]}...")
    with open(os.path.join(root, "salary.csv"), "r+b") as handle:
        handle.seek(4)
        handle.write(b"9")                                       # one character: 5000 becomes 9000
    os.unlink(os.path.join(root, "logo.bin"))
    with open(os.path.join(root, "backdoor.sh"), "wb") as handle:
        handle.write(b"evil")
    after = manifest(root)
    print(f"{'salary.csv':<11} {after['salary.csv'][:16]}...   <- after changing one character")
    print(compare(before, after))
```

```text
logo.bin    ae4b3280e56e2faf...
notes.txt   f233a56920f05d8d...
salary.csv  0e294cef6728af00...
salary.csv  72bbb0989ae67d01...   <- after changing one character
{'changed': ['salary.csv'], 'missing': ['logo.bin'], 'added': ['backdoor.sh']}
```

Changing one character gave `salary.csv` a fingerprint with no resemblance to the old one, and the comparison found the changed file, the deleted one, and the added one. A manifest is only as trustworthy as its storage: an attacker who can change the files can often change a stored manifest too, so keep it somewhere the attacker cannot write (a read-only medium, another machine) or sign it. Crash-safe updates ([file-system-basics.md](file-system-basics.md)) keep the file system itself consistent after an accident, but they say nothing about whether the *contents* are the ones you expect; fingerprints answer that.

## 🔒 Encryption and What It Does Not Do

Everything in this lesson and the last is enforced by the operating system, so none of it helps when someone else reads the disk: if the drive is moved to another machine, or the computer is started from another system, the permission bits are only data. **Disk encryption** closes that gap by encrypting every bit that goes onto a disk or volume, to prevent unauthorized access to the stored data. It is normally *transparent*: data is encrypted as it is written and decrypted as it is read, so once the key has been supplied the files are as accessible as on an unencrypted disk, and the whole file system inside the volume, including file names and other metadata, is encrypted ([Wikipedia: Disk encryption](https://en.wikipedia.org/wiki/Disk_encryption)). Each mainstream system has an implementation: [FileVault](https://en.wikipedia.org/wiki/FileVault) on the Mac (its second version encrypts the entire startup volume), [BitLocker](https://en.wikipedia.org/wiki/BitLocker) on Windows, and [dm-crypt](https://en.wikipedia.org/wiki/Dm-crypt) with the [LUKS](https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup) format on Linux.

The same transparency sets the limit. Disk encryption generally uses one key for the whole drive, so while the machine runs, all of the data can be decrypted: an attacker who gains access at run time has access to all files. Encryption of individual files and folders, with different keys, protects better against that, but it typically leaves metadata such as the directory structure, file names, timestamps, and sizes unencrypted (the same article). So disk encryption and permissions answer different threats and are used *together*: encryption for a disk that is lost, stolen, or copied, permissions for the users and programs of a running system. This lesson has no encryption code on purpose: the rule in cryptography is to use the implementation that your operating system or a well-reviewed library provides, and never to invent your own. The OSTEP chapter on [cryptography](https://pages.cs.wisc.edu/~remzi/OSTEP/security-crypto.pdf) explains the ideas behind it.

## 🧰 Least Privilege and a Small Audit

The **principle of least privilege** says that every module, whether a process, a user, or a program, must be able to access only the information and resources that are necessary for its legitimate purpose; an account that exists only to make backups, for example, should not be able to install software ([Wikipedia: Principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)). For files it comes down to habits: create private things privately (`0o600` and `0o700`); give shared directories the sticky bit and write permission only where it is needed; keep setuid programs few (all of this is in [file-permissions.md](file-permissions.md)); run each service under its own unprivileged account, so that a tricked service can reach only its own files; and keep secrets out of places that others can read. Some software enforces the last rule itself. The manual page of OpenSSH says that a private key file should be readable by the user and not accessible by others, and that `ssh` will simply ignore a key file that is accessible by others ([OpenSSH `ssh(1)`](https://man.openbsd.org/ssh)). The block generates a throw-away key and tries the same file with two modes:

```python
import shutil

if shutil.which("ssh-keygen") is None:
    print("ssh-keygen is not installed on this machine")
else:
    with tempfile.TemporaryDirectory() as workshop:
        key = os.path.join(workshop, "demo_key")
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", key], check=True)     # a throw-away key
        for mode in (0o644, 0o600):
            os.chmod(key, mode)
            result = subprocess.run(["ssh-keygen", "-y", "-f", key], capture_output=True, text=True)   # read the key back
            print(f"mode {mode:04o}:", "accepted" if result.returncode == 0 else "refused")
            for line in result.stderr.replace(key, "demo_key").splitlines():
                if "Permissions" in line or "bad permissions" in line:
                    print("   ", line)
```

One run on the test machine printed:

```
mode 0644: refused
    Permissions 0644 for 'demo_key' are too open.
    Load key "demo_key": bad permissions
mode 0600: accepted
```

Finally, the checks of these two lessons can be turned into a small **audit** that walks a tree and reports what least privilege would not allow: programs with the setuid or setgid bit, files and directories that anybody may write (except sticky directories, whose job is to be shared), and private keys that others can read. Real tools do the same job at larger scale (`find / -perm -4000` lists the setuid files), and the function below was checked against `find`. The demonstration plants one of each problem, and one harmless sticky directory, in a temporary tree:

```python
def audit(root):
    findings = []
    for folder, directories, files in os.walk(root):
        for name in directories + files:
            path = os.path.join(folder, name)
            mode = os.lstat(path).st_mode
            if stat.S_ISLNK(mode):
                continue                                          # a link has no permissions of its own to judge
            shown = os.path.relpath(path, root)
            if stat.S_ISREG(mode) and mode & (stat.S_ISUID | stat.S_ISGID):
                findings.append((shown, "setuid or setgid program"))
            if mode & stat.S_IWOTH and not (stat.S_ISDIR(mode) and mode & stat.S_ISVTX):
                findings.append((shown, "directory writable by everyone" if stat.S_ISDIR(mode) else "file writable by everyone"))
            if stat.S_ISREG(mode) and mode & (stat.S_IRGRP | stat.S_IROTH) and name.endswith((".key", ".pem")):
                findings.append((shown, "private key readable by others"))
    return sorted(findings)

with tempfile.TemporaryDirectory() as root:
    for name, mode, is_folder in (("shared", 0o1777, True), ("scratch", 0o777, True), ("tool", 0o4755, False),
                                  ("server.key", 0o644, False), ("notes.txt", 0o666, False),
                                  ("fine.txt", 0o644, False), ("private.key", 0o600, False)):
        path = os.path.join(root, name)
        if is_folder:
            os.mkdir(path)
        else:
            open(path, "w").close()
        os.chmod(path, mode)                                      # chmod ignores the umask, unlike creation
    for shown, problem in audit(root):
        print(f"{shown}: {problem}")
```

```text
notes.txt: file writable by everyone
scratch: directory writable by everyone
server.key: private key readable by others
tool: setuid or setgid program
```

The sticky directory `shared` (`1777`) is not reported, because world-writable-but-sticky is the correct way to share a directory, and `private.key` (`0o600`) and `fine.txt` are not reported either. An audit like this is worth running whenever a system is set up and after any change of ownership or mode.

## ✅ Checking the Code

Each piece of code was compared with an independent reference. `O_CREAT | O_EXCL` produced exactly one winner in each of 3,000 rounds of 8 threads and in each of 600 rounds of 32. `safe_join` was compared with an independent oracle, the inode of the file that the operating system really opens against the set of inodes inside the upload folder, on 94,967 random paths that exist (including paths that leave the folder and come back through symbolic links): no disagreement, while the naive version was wrong on 30,627 of the same paths. `audit` returned exactly the same files and directories as the corresponding `find` commands on 150 random trees (2,565 entries) with random modes and special bits. And `fingerprint` matched `shasum -a 256` on 26 files, including an empty one and sizes around the 64 KiB chunk boundary.

## Common Misconceptions

- **"Check the file, then open it" is safe.** The name can be made to mean something else between the two calls. Open first, ask the kernel for the guarantee you need (`O_EXCL`, `O_NOFOLLOW`), and examine the descriptor you hold.
- **"A path that starts with the right folder stays inside it."** An absolute segment, `..` components, symbolic links, and sibling folders with a common prefix each break that assumption; resolve the path first and compare whole components.
- **"Encrypting the disk makes file permissions unnecessary."** Disk encryption protects a disk that is lost or copied; on a running system with the volume unlocked, every process that is allowed to read a file sees it in plain form.
- **"A hash proves that a file is genuine."** It proves only that the file matches the hash. An attacker who can change the file can often change a stored copy of the hash too, so keep the manifest out of reach or sign it.

## ➡️ Next

This completes the File Systems module: what a file system is and how it survives crashes, how names lead to files, how blocks are allocated to them, and how access to them is controlled and attacked. The next module, [Virtual Memory](../virtual-memory/README.md), returns to the paging of [paging.md](../memory-management/paging.md) to show how page tables let a process use more memory than the machine has, and how the system decides which pages to keep in RAM.
