# Password Hashing

## Never Store a Password in Plain Text

```js
// CATASTROPHIC — if the database is ever breached, every user's
// actual password is immediately exposed
await User.create({ email, password: req.body.password });
```

Storing a password exactly as the user typed it means anyone who ever gains access to the database
— a breach, a careless backup, an insider — instantly has every user's real password, usable
directly on this and (since people frequently reuse passwords) likely many *other* services too.
This is never acceptable, under any circumstance.

## Why a Plain Hash (MD5/SHA256) Still Isn't Enough

```js
// STILL DANGEROUS — SHA256 is a real cryptographic hash, but it's
// deliberately FAST, which is exactly the wrong property here
const hash = crypto.createHash("sha256").update(password).digest("hex");
```

A general-purpose cryptographic hash like SHA256 does stop a password from being stored in
*readable* form — but it's deliberately designed to be **fast**, since hashing is used for many
purposes (verifying file integrity, for instance) where speed is genuinely desirable. That same
speed is a serious liability specifically for passwords: an attacker with a stolen database of
SHA256 hashes can try billions of password guesses per second against them, making even a
reasonably strong password crackable in a practical amount of time.

## bcrypt — Deliberately Slow, on Purpose

```js
import bcrypt from "bcrypt";

const saltRounds = 10;
const hashedPassword = await bcrypt.hash(req.body.password, saltRounds);
await User.create({ email: req.body.email, password: hashedPassword });
```

**bcrypt** is a hashing algorithm purpose-built for passwords — it's deliberately, tunably *slow*.
The `saltRounds` parameter controls exactly how slow: each additional round roughly **doubles** the
computational cost (`2^rounds` iterations), making a brute-force attack against stolen bcrypt
hashes dramatically more expensive than against a SHA256 hash, even though both are equally "real"
cryptographic hashes.

## Salt — Defeating Precomputed Attacks

```
Same password, hashed twice with bcrypt → DIFFERENT output each time,
because bcrypt automatically generates a unique random salt per hash
```

A **salt** is random data mixed into the password before hashing, so the same password produces a
genuinely different hash every time. This defeats **rainbow table** attacks — a precomputed lookup
table mapping common passwords to their hash — since an attacker would need a separate precomputed
table for every possible salt value, which is computationally infeasible. bcrypt generates and
manages this salt automatically as part of `bcrypt.hash()`, so it doesn't need to be handled
manually.

## Verifying a Password on Login

```js
app.post("/login", async (req, res) => {
  const user = await User.findOne({ email: req.body.email });
  if (!user) return res.status(401).json({ error: "Invalid credentials" });

  const isValid = await bcrypt.compare(req.body.password, user.password);
  if (!isValid) return res.status(401).json({ error: "Invalid credentials" });

  // credentials are valid — proceed to issue a session or JWT
});
```

`bcrypt.compare(plainTextPassword, storedHash)` re-hashes the submitted password using the same
salt already embedded in the stored hash, and compares the results — there's no way to "decrypt" a
bcrypt hash back into the original password; verification only ever works by re-hashing and
comparing.

## A Deliberately Vague Error Message Matters

Notice the identical error message (`"Invalid credentials"`) whether the email doesn't exist at all
or the password is simply wrong. Returning a different message for each case ("no account with
that email" vs. "wrong password") leaks information — it lets an attacker use the login endpoint
itself to discover which email addresses actually have accounts, one guess at a time.

## Common Mistakes

- Storing a password in plain text or with a fast general-purpose hash (MD5, SHA256, SHA1) instead
  of a purpose-built, deliberately slow algorithm like bcrypt.
- Implementing a custom, manual salting scheme instead of using bcrypt's built-in, already-correct
  handling of it.
- Returning different error messages for "no such user" vs. "wrong password," leaking which emails
  have registered accounts.

## Next

Continue to [sessions.md](sessions.md) to see one of the two standard ways a server remembers a
user is logged in across multiple requests, after this initial password check.
