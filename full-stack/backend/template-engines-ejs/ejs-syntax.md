# 🔤 EJS Syntax

## The Three Tag Types

```html
<%= user.name %>    <!-- escaped output -->
<% if (user.isAdmin) { %>  <!-- scriptlet: logic, no output -->
  <span>Admin</span>
<% } %>
<%- user.bioHtml %>  <!-- UNESCAPED output -->
```

EJS has exactly three tag types, and choosing correctly between them matters for real security
reasons, not just style:

| Tag | Purpose |
|---|---|
| `<%= %>` | Outputs a value, with HTML characters **escaped** |
| `<% %>` | A **scriptlet** — runs plain JavaScript logic, produces no output itself |
| `<%- %>` | Outputs a value **without** escaping — raw HTML |

## `<%= %>` — the Safe Default

```html
<p><%= comment.text %></p>
```

```
If comment.text is "<script>alert('hacked')</script>", the ESCAPED
output renders it as literal, harmless TEXT on the page:
&lt;script&gt;alert('hacked')&lt;/script&gt;
```

`<%= %>` automatically escapes special HTML characters (`<`, `>`, `&`, and others) in whatever
value it outputs — so even if `comment.text` contains something that looks like an HTML tag or a
`<script>` block, it's rendered as harmless, visible text, not executed as real HTML/JavaScript.
This is the same underlying protection
[Cross-Site Scripting (XSS)](../../web-security/cross-site-scripting-xss/) content covers in full —
`<%= %>` is EJS's built-in defense against exactly that vulnerability, and should be the default
choice for essentially everything.

## `<%- %>` — Raw, Unescaped Output

```html
<!-- Genuinely safe: rendering a TRUSTED, already-sanitized value -->
<div class="article-body"><%- article.sanitizedHtmlBody %></div>

<!-- DANGEROUS: rendering RAW user input, unescaped -->
<div><%- req.body.comment %></div>
```

`<%- %>` outputs a value exactly as-is, with no escaping — genuinely necessary sometimes, like
rendering a trusted block of HTML that's meant to contain real markup (a rich-text article body
that's already been sanitized through a dedicated process). Using it on **untrusted input** —
anything a user submitted directly — is a direct, serious XSS vulnerability: whatever HTML or
JavaScript that input contains would be rendered and executed exactly as written.

## Scriptlets — `<% %>` for Logic, Not Output

```html
<% const now = new Date(); %>
<p>Rendered at: <%= now.toLocaleTimeString() %></p>
```

`<% %>` runs plain JavaScript with no output of its own — declaring a variable, or (as covered in
[loops-conditionals-and-locals.md](loops-conditionals-and-locals.md)) controlling a loop or
conditional. Anything that should actually appear on the page still needs its own `<%= %>` or
`<%- %>` tag.

## Common Mistakes

- Using `<%- %>` on unsanitized user input — a direct XSS vulnerability, exactly the kind
  [Cross-Site Scripting (XSS)](../../web-security/cross-site-scripting-xss/) content warns against.
- Using `<%= %>` when genuinely trusted, pre-sanitized HTML needs to render as real markup — the
  content would show up as visible, escaped text instead of the intended formatted HTML.
- Forgetting that a scriptlet (`<% %>`) produces no output at all — a value declared or computed
  there still needs its own separate `<%= %>` tag to actually appear on the page.

## ➡️ Next

Continue to [loops-conditionals-and-locals.md](loops-conditionals-and-locals.md) to render dynamic
lists and conditional sections of a page.
