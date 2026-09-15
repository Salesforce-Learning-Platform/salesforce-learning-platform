# 💻 Command Injection

## The Same Pattern, Applied to the Operating System Shell

[understanding-injection.md](understanding-injection.md) established injection as a general
pattern: untrusted input combined with executable instructions, without proper separation.
**Command injection** is exactly this pattern applied to operating system shell commands instead of
SQL queries — an application that runs a shell command incorporating user input can have that input
interpreted as *additional commands*, not just as inert data.

## The Vulnerable Pattern

```js
const { exec } = require("node:child_process");

app.get("/ping", (req, res) => {
  const host = req.query.host;
  exec(`ping -c 4 ${host}`, (error, stdout) => {   // VULNERABLE
    res.send(stdout);
  });
});
```

```
Attacker sends: GET /ping?host=example.com; rm -rf /important-data

The resulting shell command BECOMES:
ping -c 4 example.com; rm -rf /important-data

The shell treats ";" as a command SEPARATOR - it runs "ping",
THEN separately runs "rm -rf /important-data" as a SECOND,
entirely independent command.
```

Node.js's own official documentation states this risk directly: "Never pass unsanitized user input
to this function. Any input containing shell metacharacters may be used to trigger arbitrary command
execution" — this is exactly the same severity of risk as SQL injection, just targeting the
operating system shell instead of a database.

## The Fix: `execFile` Instead of `exec`

```js
const { execFile } = require("node:child_process");

app.get("/ping", (req, res) => {
  const host = req.query.host;
  execFile("ping", ["-c", "4", host], (error, stdout) => {   // SAFE
    res.send(stdout);
  });
});
```

This is the exact same structural-separation principle already established for SQL injection, now
applied here: `execFile` does **not** spawn a shell by default — it passes `host` as a literal
*argument* directly to the `ping` executable, never interpreted as shell syntax at all. Per Node.js's
own documentation, this makes `execFile` genuinely safer by default than `exec`, precisely because
there's no shell present to misinterpret metacharacters like `;` or `|` in the first place.

## Verifying the Fix Actually Works

```
Attacker sends the SAME payload: host=example.com; rm -rf /important-data

With execFile, this entire string is passed as ONE literal
argument to "ping" - ping receives a single, nonsensical hostname
argument (which simply fails to resolve), and "rm -rf" is NEVER
executed as a separate command at all.
```

This is the genuine payoff: the fix doesn't rely on detecting or blocking specific dangerous
characters — it eliminates the shell interpretation step entirely, so there's no mechanism left for
an attacker's input to ever be treated as anything other than a literal, inert value.

## When a Shell Is Genuinely Needed

```
If shell features (pipes, wildcards) are GENUINELY required,
Node's own documentation is explicit: "If the shell option is
enabled, do NOT pass unsanitized user input to this function."
```

For the rare, genuine case where shell features are actually needed, the safe approach is never
"carefully sanitize the input" — it's avoiding passing untrusted input into that shell context at
all, restructuring the command to use only trusted, application-controlled values.

## Common Mistakes

- Using `exec()` (which spawns a shell) for a command that incorporates any user-supplied value,
  rather than `execFile()`.
- Attempting to sanitize user input by blocklisting specific "dangerous" characters (`;`, `|`, `&`),
  an approach that's genuinely easy to bypass with an unanticipated character or encoding.
- Passing the `shell: true` option to `execFile()` "just in case," which reintroduces the exact same
  shell-interpretation risk `execFile()` was chosen specifically to avoid.

## ➡️ Next

Continue to
[preventing-injection-attacks.md](preventing-injection-attacks.md) to bring the SQL and command
injection defenses together into one complete, general prevention strategy.
