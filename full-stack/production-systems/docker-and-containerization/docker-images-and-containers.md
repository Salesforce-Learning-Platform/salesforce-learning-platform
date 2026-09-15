# 🖼️ Images vs. Containers

## The Class-and-Instance Relationship

```
IMAGE     → a read-only TEMPLATE: the filesystem, dependencies,
            and default startup command for an application —
            never changes once built

CONTAINER → a RUNNING INSTANCE of an image — has its own
            writable layer, its own process, its own state
```

This is one of the most important conceptual distinctions in Docker, and it maps directly onto a
concept familiar from object-oriented programming: an image is like a **class** (a fixed
definition/template), and a container is like an **instance** of that class (a live, running thing
built from it).

## Building One Image, Running Many Containers

```bash
docker build -t my-app:1.0 .        # build ONE image, once

docker run my-app:1.0                # container instance #1
docker run my-app:1.0                # container instance #2 -
                                      # a SEPARATE, independent
                                      # running instance, from the
                                      # SAME image
```

The same image can be used to start any number of independent, isolated containers — each gets its
own writable layer and its own process, but they all start from the identical, unchanging image
definition. This is exactly how a real production deployment runs multiple identical instances of
the same service for scaling and redundancy.

## Layers: How an Image Is Actually Built

```
Image layers, built bottom-up from a Dockerfile:
  Layer 1: base OS (e.g. node:20-slim)
  Layer 2: installed dependencies (npm install)
  Layer 3: application code (COPY . .)

Each layer is CACHED — rebuilding an image after only changing
application code reuses the CACHED base OS and dependency layers,
rather than rebuilding everything from scratch.
```

This layered structure is a genuinely important practical detail: it's why Docker builds can be
fast on repeated builds — Docker only rebuilds the layers that actually changed, reusing everything
above them from cache. [writing-dockerfiles.md](writing-dockerfiles.md), next in this module, covers
how to structure a Dockerfile to take real advantage of this caching.

## A Container's Writable Layer

```
Image layers: READ-ONLY, shared across every container started
  from that image

A running container ADDS its own thin, WRITABLE layer on top —
  any file the application writes at runtime lives here, and is
  DISCARDED when the container is removed (unless explicitly
  persisted - covered in container-volumes.md, later in this
  module).
```

This is why a container's own runtime changes (a log file it writes, a temporary file it creates)
don't persist by default once the container is removed — they exist only in that container's own
ephemeral writable layer, not in the shared, unchanging image underneath.

## Common Mistakes

- Confusing "rebuilding an image" with "restarting a container" — an image change requires an
  explicit `docker build`; simply restarting an existing container reuses the same, unchanged image.
- Storing important application data only in a container's writable layer, then losing it entirely
  when the container is removed or recreated.
- Structuring a Dockerfile so that frequently-changing code is copied before rarely-changing
  dependencies, defeating the layer-caching benefit this file covers.

## ➡️ Next

Continue to [docker-architecture.md](docker-architecture.md) to see the pieces — the daemon, the
CLI, and image registries — that actually make building and running images and containers work.
