# 🛠️ Backend Engineering

## 📚 Overview

The backend is the server side of an application: it handles requests, stores data, decides who may do what, and has to keep working. These modules start with Node.js and Express, then cover API design, SQL and MongoDB, authentication, and architecture, followed by features real services need: server-rendered pages, file uploads, API documentation, logging, production authentication, real-time updates, caching, payments, and testing. They assume the JavaScript taught in the [frontend path](../frontend/README.md).

## 🧭 The Learning Path

Work through the modules in this order. The last column names the earlier modules each one relies on, so you can also start partway through; links point to modules in other areas.

| # | Module | What it covers | Builds on |
|---|--------|----------------|-----------|
| 1 | [Starting with Node.js](starting-with-nodejs/README.md) | What Node.js is, how it runs JavaScript outside the browser, installing it, and npm | JavaScript, from the [frontend path](../frontend/README.md) |
| 2 | [Node.js Core Concepts](nodejs-core-concepts/README.md) | Modules, the file system, paths, environment variables, process control, and the event loop | Starting with Node.js |
| 3 | [Creating Your First Server](creating-your-first-server/README.md) | An HTTP server with the `http` module: requests, responses, routing by hand, and status codes | Node.js Core Concepts |
| 4 | [Express.js Fundamentals](expressjs-fundamentals/README.md) | Routing, middleware, request and response helpers, and error handling | Creating Your First Server |
| 5 | [REST API Design](rest-api-design/README.md) | Resources, naming, methods, status codes, validation, pagination, and versioning | Express.js Fundamentals |
| 6 | [SQL Fundamentals](sql-fundamentals/README.md) | Tables, queries, writes, joins, aggregation, subqueries, and indexes, used from Express | REST API Design |
| 7 | [MongoDB Fundamentals](mongodb-fundamentals/README.md) | Documents, CRUD with Mongoose, queries, aggregation, embedding or referencing, and indexes | SQL Fundamentals |
| 8 | [Database Design and Modeling](database-design-and-modeling/README.md) | Relationships, keys and constraints, normalization, schema design, and SQL or NoSQL | SQL Fundamentals, MongoDB Fundamentals |
| 9 | [Authentication and Authorization](authentication-and-authorization/README.md) | Password hashing, sessions, JWTs, authentication middleware, and role-based access | Express.js Fundamentals, Database Design and Modeling |
| 10 | [Backend Architecture](backend-architecture/README.md) | Layers, controllers, services and repositories, configuration, and central error handling | All the modules above |
| 11 | [Template Engines — EJS](template-engines-ejs/README.md) | Rendering HTML on the server with EJS views | Express.js Fundamentals |
| 12 | [Handling Files with Express](handling-files-with-express/README.md) | File uploads with Multer, storage choices, validation, and cloud storage | Express.js Fundamentals |
| 13 | [API Documentation and Developer Experience](api-documentation-and-developer-experience/README.md) | OpenAPI and Swagger UI, Postman collections, versioning in practice, and generated clients | REST API Design |
| 14 | [Logging and Monitoring](logging-and-monitoring/README.md) | Structured logs and log levels, request logs with Morgan, and error logging | Backend Architecture |
| 15 | [Production Authentication Architecture](production-authentication-architecture/README.md) | Access and refresh tokens, rotation, Redis storage, logging out everywhere, and CSRF protection | Authentication and Authorization |
| 16 | [Real-Time Communication — WebSockets and Socket.io](real-time-communication/README.md) | WebSockets and Socket.io: events, rooms, and authenticating a connection | Authentication and Authorization |
| 17 | [Caching — Local and Redis](caching-local-and-redis/README.md) | In-memory and Redis caching, cache-aside, invalidation, expiry, and Pub/Sub | SQL or MongoDB Fundamentals, Production Authentication Architecture |
| 18 | [Payments Integration](payments-integration/README.md) | Payment intents, webhooks and signature checks, and idempotency | REST API Design, Database Design and Modeling |
| 19 | [Backend Testing](backend-testing/README.md) | Unit tests with mocks, integration tests, API tests with Supertest, and what to test first | Backend Architecture, [Frontend Testing Fundamentals](../frontend/testing/frontend-testing-fundamentals/README.md) |

## ➡️ Start Here

Begin with [Starting with Node.js](starting-with-nodejs/README.md). After the last module, the course continues with [Artificial Intelligence Engineering](../artificial-intelligence/README.md).
