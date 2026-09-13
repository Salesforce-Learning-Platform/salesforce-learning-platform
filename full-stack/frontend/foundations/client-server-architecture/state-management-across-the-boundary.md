# State Management Across the Client-Server Boundary

## Intuition

HTTP, as covered in
[how-the-internet-works](../how-the-internet-works/http-https-and-tls.md), is **stateless**: the
server treats every request independently, with no built-in memory of previous ones. But real
applications clearly do remember things — you stay logged in, your shopping cart persists between
page loads. This file explains how applications create the illusion of continuity on top of a
protocol that has none.

## Why Statelessness Was a Deliberate Choice

A stateless protocol means any server that receives a request has everything it needs to handle
it, without depending on which specific server handled a previous request from the same client.
This is what makes it possible to run a web application across many interchangeable servers behind
a load balancer — any of them can handle any request, because none of them are required to
remember you individually. The cost of this design is that "remembering" has to be built
deliberately, rather than coming for free.

## How Continuity Is Actually Achieved

| Mechanism | How it works | Where the state actually lives |
|---|---|---|
| **Cookies** | Server sets a `Set-Cookie` header; browser automatically resends it on every subsequent request to that domain | A small piece of data on the client, but often just an identifier — see sessions below |
| **Sessions** | The cookie holds a session ID; the actual data (who's logged in, cart contents) is stored server-side, keyed by that ID | Server (database or in-memory store), referenced by a client-held key |
| **Tokens (e.g., JWT)** | The client stores a signed token (often in memory or local storage) and sends it with each request, typically in an `Authorization` header | Client holds the full token; server verifies its signature rather than looking anything up |
| **Client-side application state** | Frontend frameworks hold in-memory state (open modals, form drafts, fetched data) for the current page session | Client only, and lost on a full page reload unless separately persisted |

## Server-Side State vs. Client-Side State

This distinction matters for correctness, not just terminology:

- **Server-side state** (what's actually stored in a database, keyed by a session or user ID) is
  the authoritative record — this is what determines what a user is genuinely allowed to see or
  do, and it's why authentication and authorization must be checked server-side on every request
  that needs them, not inferred from anything the client claims about itself.
- **Client-side state** (React component state, a Redux store, form input, LWC component
  properties) is a *local, disposable* representation used purely for rendering and interaction. It
  should be treated as a cache of — or a draft toward — server state, not a second source of truth.

## Common Mistakes

- **Trusting client-held state for anything security-relevant.** A token or cookie can identify
  *who is asking*, but the server must still independently decide *what they're allowed to do* —
  never take a client's self-reported role or permission level at face value.
- **Conflating "logged in on the frontend" with "authenticated on the backend."** A frontend that
  simply hides a login screen because a flag is set in local storage, without the backend
  independently verifying a valid session/token on every request, is not actually enforcing
  authentication.
- **Losing track of what happens when state gets out of sync** — e.g., a shopping cart shown in
  the UI that no longer matches the server's actual cart because a request failed silently. The
  request-response lifecycle in
  [the-request-response-lifecycle.md](the-request-response-lifecycle.md) exists precisely to keep
  these reconciled.

## Salesforce Relevance

Salesforce sessions are a direct application of this pattern: a session ID (delivered via a
cookie or an OAuth access token, depending on the integration) identifies an authenticated user on
every subsequent API or page request, while the platform's actual security model — sharing rules,
field-level security, object permissions — is evaluated server-side on every single request,
regardless of what a client-side component believes about the current user's access.

## Module Summary

Across this module: the frontend and backend split responsibilities along a trust boundary (see
[frontend-and-backend-responsibilities.md](frontend-and-backend-responsibilities.md)); every
interaction follows a repeatable request-response cycle (see
[the-request-response-lifecycle.md](the-request-response-lifecycle.md)); and because HTTP itself
has no memory, applications build continuity deliberately on top of it using cookies, sessions, or
tokens — with the server always remaining the authoritative source of truth.
