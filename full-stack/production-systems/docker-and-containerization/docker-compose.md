# 🎼 Docker Compose for Multi-Service Apps

## Replacing a Sequence of `docker run` Commands With One File

Every piece covered so far in this module — building an image, creating a network, mounting a
volume, publishing a port — required its own separate `docker` command, run manually, in the right
order, every single time. **Docker Compose** replaces this entire sequence with one declarative
YAML file, describing an application's full set of services at once.

## A Complete `docker-compose.yml`, for a Real Backend + Database App

```yaml
services:
  backend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://database:5432/myapp
    depends_on:
      database:
        condition: service_healthy

  database:
    image: postgres:16
    environment:
      - POSTGRES_DB=myapp
    volumes:
      - pg-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  pg-data:
```

```bash
docker compose up
```

One command — `docker compose up` — builds the `backend` image, starts both containers, creates a
shared network between them automatically (Compose does this without an explicit
[`docker network create`](container-networking.md) step), and mounts the `pg-data`
[volume](container-volumes.md). Every concept from this module comes together in this one file.

## Reading the File, Piece by Piece

```
services:    → each top-level entry is ONE container to run
build: .     → build FROM a local Dockerfile, rather than pulling
               a pre-built image
image:       → use an EXISTING, pre-built image (here, the
               official PostgreSQL image) instead of building one
ports:       → publish a port to the host (per container-
               networking.md's "publish" concept)
environment: → set environment variables inside the container -
               directly the SAME per-environment configuration
               pattern from environment-management.md, earlier in
               this domain
volumes:     → mount a named volume for real data persistence
depends_on:  → control STARTUP ORDER between services
```

## `depends_on` With a Health Check — Not Just "Start After"

```yaml
depends_on:
  database:
    condition: service_healthy
```

A plain `depends_on: database` only guarantees the database *container* has started — not that
PostgreSQL is actually *ready* to accept connections yet, which can take a moment even after the
container itself is running. Adding `condition: service_healthy`, paired with the database's own
`healthcheck`, makes `backend` genuinely wait until the database is confirmed ready, not just
started — directly preventing a common, confusing "connection refused" race condition on startup.

## Automatic Networking, Automatic DNS

```
Compose automatically creates a SHARED network for every service
defined in the SAME file - "backend" can reach "database" by that
exact service name, with NO manual `docker network create` step
required.
```

This is a genuinely significant convenience over the manual approach from
[container-networking.md](container-networking.md) — Compose handles the network creation and
service-name DNS resolution automatically, simply from services being defined together in the same
file.

## Common Mistakes

- Using a plain `depends_on` without a health check for a service (like a database) that takes real
  time to become ready after its container starts, causing intermittent startup failures.
- Hardcoding secrets directly into the `environment` section of a committed `docker-compose.yml`
  instead of referencing a separate, gitignored `.env` file.
- Forgetting to define a named volume for a stateful service in Compose, losing data on every
  `docker compose down` exactly as covered in [container-volumes.md](container-volumes.md).

## Module Summary

Across this module: **containers** are lightweight, isolated processes sharing the host's kernel,
genuinely different from — and often complementary to — full virtual machines (see
[introduction-to-containers.md](introduction-to-containers.md)); **an image is a fixed template, a
container is a running instance of it**, with layer caching making repeated builds fast (see
[docker-images-and-containers.md](docker-images-and-containers.md)); **the client/daemon/registry
architecture** underlies every Docker command (see
[docker-architecture.md](docker-architecture.md)); **a Dockerfile's instructions** — `FROM`,
`WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD` — build a real image, with careful instruction ordering,
`.dockerignore`, and multi-stage builds producing smaller, safer final images (see
[writing-dockerfiles.md](writing-dockerfiles.md)); **user-defined networks** give containers real,
name-based DNS resolution, with a clear distinction between exposing a port internally and
publishing it externally (see [container-networking.md](container-networking.md)); **volumes**
solve the ephemeral-writable-layer problem for any data that must genuinely persist beyond a single
container's lifetime (see [container-volumes.md](container-volumes.md)); and **Docker Compose**
brings every one of these pieces — build, network, volumes, environment, startup ordering — into
one declarative file describing a complete, multi-service application.
