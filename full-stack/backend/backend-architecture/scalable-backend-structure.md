# Scalable Backend Structure

## Putting Every Piece of This Module Together

```
src/
├── config/
│   └── index.js              # per configuration-management.md
├── controllers/
│   └── orderController.js    # per controllers-services-and-repositories.md
├── services/
│   └── orderService.js
├── repositories/
│   └── orderRepository.js
├── routes/
│   └── orders.js
├── middleware/
│   ├── requireAuth.js        # per authentication-and-authorization/
│   └── errorHandler.js       # per error-handling-architecture.md
├── errors/
│   └── AppError.js
└── app.js                    # wires everything together
```

This folder structure is the concrete, physical expression of
[layered-architecture.md](layered-architecture.md)'s idea: each layer gets its own folder, so the
project's actual architecture is visible directly from its file tree — a new developer joining the
project (recall
[reading-and-navigating-unfamiliar-codebases](../../frontend/frontend-architecture/reading-and-navigating-unfamiliar-codebases/))
can understand its shape before reading a single line of code.

## Grouping by Layer vs. by Feature

```
BY LAYER (shown above):              BY FEATURE:
controllers/orderController.js        orders/
controllers/productController.js        controller.js
services/orderService.js                service.js
services/productService.js              repository.js
                                       products/
                                         controller.js
                                         service.js
                                         repository.js
```

Just as [Frontend's understanding-project-structure.md](../../frontend/frontend-architecture/reading-and-navigating-unfamiliar-codebases/understanding-project-structure.md)
described for frontend code, a backend can also group by *type* (all controllers together, as
shown first) or by *feature* (everything for "orders" together, regardless of layer). Grouping by
feature tends to scale better for larger applications with many distinct domains, since it keeps
everything related to one feature physically close together, rather than spread across several
top-level folders that all grow in parallel.

## `app.js` — Wiring, Not Logic

```js
// app.js
import express from "express";
import ordersRouter from "./routes/orders.js";
import { errorHandler } from "./middleware/errorHandler.js";

const app = express();

app.use(express.json());
app.use("/orders", ordersRouter);
app.use(errorHandler); // always last, per error-handling-architecture.md

export default app;
```

The application's entry point should contain almost no real logic of its own — just wiring
together the pieces already built by every other layer: registering middleware
([Express's middleware.md](../expressjs-fundamentals/middleware.md)), mounting routers, and
registering the central error handler last.

## Why This Structure Scales

- A new feature means adding a new controller/service/repository set, following the exact same
  established pattern — not inventing a new structure each time.
- Testing is straightforward: a service can be tested with a fake repository, with no real
  database or HTTP server involved at all.
- Changing *how* data is stored (per
  [SQL vs. NoSQL](../database-design-and-modeling/sql-vs-nosql.md)) touches only the repository
  layer.
- Onboarding a new developer is faster: the folder structure itself teaches the architecture.

## This Is a Starting Point, Not a Rigid Law

This structure is a strong, well-reasoned default — not a rule that applies identically,
unmodified, to every project regardless of its actual size and needs. A tiny prototype genuinely
doesn't need this much ceremony; a much larger system might eventually need further structure
(splitting into separate services entirely, a topic beyond this module's scope). The judgment to
apply the *right amount* of structure for a project's actual size and complexity is itself part of
real architectural skill.

## Common Mistakes

- Copying this exact structure onto a five-route prototype where it adds more ceremony than value —
  per [layered-architecture.md](layered-architecture.md)'s point about over-layering small
  projects.
- Letting `app.js` accumulate real business logic over time instead of staying purely wiring,
  losing the clear separation the rest of the structure establishes.
- Treating the layer-vs-feature folder-grouping choice as fixed forever — a project's natural
  grouping can and sometimes should evolve as it grows.

## Module Summary

Across this module: **layered architecture** separates HTTP handling, business logic, and data
access into distinct layers with one-directional dependencies, making each independently testable
and replaceable (see [layered-architecture.md](layered-architecture.md)); the concrete
**controller-service-repository** pattern applies this to real Express code, with each layer having
exactly one job (see
[controllers-services-and-repositories.md](controllers-services-and-repositories.md));
**configuration** belongs strictly in the environment, never hardcoded or committed, per the
Twelve-Factor App's reasoning (see [configuration-management.md](configuration-management.md));
**dependencies** are managed deliberately — audited, updated at a sensible cadence, and added only
when genuinely justified (see [dependency-management.md](dependency-management.md)); a **centralized
error-handling architecture**, with named error classes and one shared handler, replaces ad hoc
per-route error formatting (see
[error-handling-architecture.md](error-handling-architecture.md)); and all of it comes together in
a concrete, **scalable folder structure** that makes a project's real architecture visible directly
from its file tree — a strong default, deliberately scaled to match a project's actual size and
needs.
