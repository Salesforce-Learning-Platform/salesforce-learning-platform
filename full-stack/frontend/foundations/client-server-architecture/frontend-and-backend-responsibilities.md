# Frontend and Backend Responsibilities

## Intuition

A restaurant separates the dining room from the kitchen. The dining room (frontend) is what
customers see and interact with — menus, seating, presentation. The kitchen (backend) does the
work customers never see directly — sourcing ingredients, cooking, enforcing food-safety rules —
and only the kitchen is trusted to decide whether an order is actually safe to serve. Client-server
web architecture draws the same line, for the same reason: trust and responsibility.

## The Split

**Frontend (client)** responsibilities:

- Rendering the user interface and handling user interaction (clicks, form input, navigation).
- Client-side state that only matters for the current interaction (an open dropdown, unsaved form
  input, scroll position).
- Making requests to the backend for data or actions, and presenting the results.
- Lightweight, *non-authoritative* input validation for immediate user feedback (e.g., "this field
  is required") — a UX convenience, not a security boundary.

**Backend (server)** responsibilities:

- Business logic: the rules that define what the application is actually allowed to do.
- Data persistence and retrieval — the backend is the sole authority on what data exists and its
  current state.
- **Authoritative validation and authorization** — the backend must never trust that data arriving
  from a client is well-formed, permitted, or unmodified, because a client can be anything: a
  legitimate browser, a modified browser, or a script bypassing the UI entirely.
- Integration with other systems, databases, and external services.

## Why the Split Exists (Not Just Convention)

The split isn't arbitrary — it follows directly from a security reality covered in
[how-the-internet-works](../how-the-internet-works/): **the client is never trustworthy**. Anyone
can open browser DevTools, modify client-side JavaScript, or send HTTP requests directly with a
tool like `curl`, bypassing your frontend entirely. Any rule enforced only in frontend code (a
disabled button, a client-side `if` statement) can be trivially bypassed by someone who skips the
frontend altogether.

This is why "validate on the client for UX, validate on the server for security" is not a
suggestion — it's the only model that actually works. The frontend validating a field client-side
improves the experience (instant feedback, fewer round trips); the backend validating the same
field is what actually protects the system, because the backend is the one component the client
cannot directly control.

## A Concrete Example

Consider a signup form requiring a unique email address:

| Layer | What it does | What it prevents |
|---|---|---|
| Frontend | Checks the field isn't empty and looks like an email, shows an inline error immediately | Nothing security-relevant — purely UX |
| Backend | Re-validates format, queries the database for an existing account with that email, rejects the request if it's a duplicate | The actual constraint the business cares about — enforced regardless of what the client sent |

If only the frontend checked for duplicates, a request sent directly to the backend's API
(skipping the UI) could still create duplicate accounts. The backend check is what makes the rule
real.

## Common Mistakes

- **Treating client-side validation as sufficient.** It is a UX layer, never a security or
  data-integrity guarantee.
- **Putting business logic in the frontend "for speed."** Logic that determines what a user is
  *allowed* to do (pricing, permissions, workflow rules) belongs on the server, where it can't be
  tampered with.
- **Assuming the backend can trust its own frontend's requests just because they "usually" come
  from the official UI.** The backend has no reliable way to know a request didn't come from a
  script or a modified client — this is exactly why backend authorization checks exist
  independently of what the frontend displays.

## Salesforce Relevance

This split maps directly onto Lightning Web Components: an LWC (frontend) can perform light,
UX-oriented checks, but record-level security, sharing rules, field-level security, and business
validation must be enforced in Apex and the platform's own security model (server-side), never
assumed from what the component displays or disables. A hidden button in an LWC does not stop a
user with API access from performing the underlying action if the backend doesn't also enforce
the restriction.

## Next

Continue to
[the-request-response-lifecycle.md](the-request-response-lifecycle.md) to see how a single
interaction moves across this boundary from start to finish.
