# 💾 Container Volumes

## The Problem: A Container's Writable Layer Is Ephemeral

[docker-images-and-containers.md](docker-images-and-containers.md) already established that a
running container's own writable layer is discarded when the container is removed. This is a
genuine problem for anything a container needs to *keep* — a database's actual stored records, an
uploaded file, anything that must outlive the container itself. **Volumes** are Docker's answer to
this problem.

## Mounting a Named Volume

```bash
docker volume create pg-data

docker run --network my-app-network --name database \
  -v pg-data:/var/lib/postgresql/data \
  postgres:16
```

`-v pg-data:/var/lib/postgresql/data` mounts the named volume `pg-data` at that specific path inside
the container — PostgreSQL's own directory for storing its actual database files. Even if this
`database` container is removed entirely and a brand-new one started, mounting the same `pg-data`
volume gives the new container access to exactly the same, real, persisted data.

## Named Volumes vs. Bind Mounts

```
NAMED VOLUME  → Docker fully manages the storage location, backup,
                and lifecycle - portable, works consistently across
                different host operating systems

BIND MOUNT    → directly maps a SPECIFIC HOST DIRECTORY into the
                container - useful for live-editing local source
                code, but tied to that host's actual filesystem
                layout
```

```bash
# Bind mount - live-editing local source code during development
docker run -v $(pwd)/src:/app/src my-backend:1.0
```

Named volumes are the right choice for genuine data persistence (a database's real data); bind
mounts are the right choice for local development convenience (seeing local code changes reflected
immediately inside a running container) — using the wrong one for the wrong purpose is a common,
avoidable mistake.

## Why This Matters Specifically for Databases

```
WITHOUT a volume: docker rm database → EVERY row of real data is
  GONE, permanently

WITH a properly mounted volume: docker rm database (followed by a
  new container mounting the SAME volume) → the data is still
  there, completely unaffected
```

This is genuinely critical to understand before running any stateful service (a database, a message
queue) in a container — without a properly configured volume, removing or recreating that container
means genuinely, irreversibly losing whatever data it held.

## Volumes Persist Independently of Any Single Container

```
docker volume ls          # list all volumes, independent of
                           # which containers are currently running
docker volume rm pg-data  # EXPLICITLY delete a volume - this is
                           # the only way real, persisted data
                           # actually goes away
```

A volume's lifecycle is genuinely decoupled from any one container's lifecycle — it exists as its
own, independently-managed resource, and only an explicit `docker volume rm` (or an equivalent
cleanup command) actually deletes the data it holds.

## Common Mistakes

- Running a database container without mounting a volume for its data directory, then being
  surprised when all data disappears on the next `docker rm`.
- Using a bind mount for production data persistence instead of a properly-managed named volume,
  tying the deployment to a specific host's exact filesystem layout.
- Running `docker system prune --volumes` (or an equivalent aggressive cleanup command) without
  realizing it will also remove volumes holding genuinely important, unbacked-up data.

## ➡️ Next

Continue to [docker-compose.md](docker-compose.md) to see how networking, volumes, and multiple
containers all come together to define a complete, multi-service application in one file.
