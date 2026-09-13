# The Request-Response Lifecycle

## Intuition

Regardless of the framework, language, or platform involved, almost every client-server
interaction on the web follows the same repeatable cycle. Learning to see this cycle underneath
any unfamiliar stack is one of the most transferable skills in frontend engineering.

## The Cycle

```text
1. User action        User clicks a button, submits a form, or the app loads
2. Client prepares     Frontend gathers the needed data, builds an HTTP request
   a request
3. Request sent        Travels the network path described in how-the-internet-works
                        (DNS → TCP/TLS → HTTP)
4. Server receives      Backend framework routes the request to the correct handler
   and routes it
5. Server processes     Business logic runs: validate input, apply rules, read/write data
6. Server responds      Backend sends an HTTP response: status code + headers + body
7. Client receives      Frontend parses the response
8. Client updates       UI re-renders to reflect the new state (success message, updated
   the UI                list, error banner)
```

```text
   Frontend                                              Backend
      │                                                     │
      │── user clicks "Save" ──────────────────────────────▶│  (conceptually — request
      │                                                     │   actually travels via the
      │◀── HTTP response: 201 Created + saved record ──────│   network layers in
      │                                                     │   how-the-internet-works)
      │── update UI: show success, refresh list ──          │
      ▼                                                     ▼
```

## Where State Lives at Each Step

This is the step most beginners skip past, and it's the source of a lot of real bugs:

- **Before the request**: the *intended* new state exists only on the client (what the user typed
  into a form).
- **During processing**: the *source of truth* is the backend's data store. The backend decides
  whether the intended change is actually valid and applies it.
- **After the response**: the client's UI should reflect what the *server confirmed*, not simply
  what the user attempted. If the backend rejects or modifies the request (e.g., trims whitespace,
  applies a default value, rejects due to a business rule), the frontend must update its view based
  on the response — not assume its own optimistic version was correct.

This is why well-built frontends distinguish between **optimistic updates** (updating the UI
immediately, before the server confirms, for perceived speed) and **confirmed state** (what the
server actually persisted) — and reconcile the two, rolling back the optimistic change if the
server's response indicates failure.

## A Complete Example

Submitting a comment on a blog post:

1. User types a comment and clicks "Post."
2. Frontend builds a `POST /posts/42/comments` request with the comment text in the body.
3. Request travels to the server.
4. Server's routing layer directs it to the comment-creation handler.
5. Server validates the comment (not empty, not too long, user is authenticated), then writes it
   to the database.
6. Server responds `201 Created` with the saved comment (including a server-generated ID and
   timestamp) — or `400 Bad Request` with an error if validation failed.
7. Frontend receives the response.
8. On success, frontend adds the *server's version* of the comment (with its real ID) to the
   displayed list; on failure, frontend shows the error message and leaves the input for
   correction.

## Common Mistakes

- **Rendering the client's optimistic guess as if it were final**, without reconciling against
  what the server actually returned — leading to UI that shows something the backend never
  actually saved.
- **Ignoring the response body on error responses.** A `400` or `422` response typically carries
  specific, actionable validation detail in its body — surfacing that to the user is usually far
  better than a generic "something went wrong."
- **Assuming the lifecycle is only relevant to full-page loads.** Every `fetch`/AJAX call, every
  API request from a mobile app, and every Apex HTTP callout follows this same shape.

## Next

Continue to
[state-management-across-the-boundary.md](state-management-across-the-boundary.md) to look more
closely at why HTTP's statelessness makes this lifecycle repeat independently for every request.
