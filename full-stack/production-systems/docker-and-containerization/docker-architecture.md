# 🏛️ Docker Architecture

## Three Pieces Working Together

```
DOCKER CLIENT (docker)  → the command-line tool you actually type
                           commands into

DOCKER DAEMON (dockerd) → the background service that does the
                           REAL work — building images, running
                           containers, managing networks/volumes

DOCKER REGISTRY          → where images are STORED and shared
                           (Docker Hub is the default public one)
```

Every Docker command you run is really a request sent from the lightweight **client** to the
**daemon**, which does the actual heavy lifting. Understanding this split matters for correctly
reasoning about what's actually happening when a command runs.

## Walking Through `docker run`, Step by Step

```
1. You type: docker run my-app:1.0
2. The CLIENT sends this request to the DAEMON
3. The DAEMON checks: is "my-app:1.0" already available LOCALLY?
4. If NOT, the daemon PULLS it from the configured REGISTRY first
5. The daemon creates and starts the CONTAINER
6. Output streams back through the client to your terminal
```

This is a genuinely useful mental model for debugging: a `docker run` that seems to "hang" the first
time but runs instantly the second time isn't behaving inconsistently — the first run included a
real network pull from the registry (step 4), which the second run skipped since the image was
already cached locally.

## Client and Daemon Don't Have to Be on the Same Machine

```
LOCAL development: client and daemon typically run on the SAME
  machine — this is the default, familiar setup

REMOTE Docker: the client can connect to a daemon running on a
  DIFFERENT machine entirely (a build server, a remote host)
```

This decoupling is a genuinely useful piece of architecture — it's what allows, for instance, a
CI/CD pipeline to trigger Docker builds on a dedicated remote build machine rather than the machine
running the pipeline's own orchestration logic.

## Registries: Public and Private

```
Docker Hub  → the default PUBLIC registry — hosts official images
              (node, postgres, redis) and public community images

Private
registries  → an organization's own registry, hosting proprietary
              application images not meant for public distribution
```

For any real application containing proprietary code, images are typically pushed to a private
registry rather than Docker Hub's public one — exactly the same reasoning that keeps an
organization's source code in a private git repository rather than a public one.

## Common Mistakes

- Assuming every `docker run` command hits the network — an image already cached locally runs
  entirely offline, with no registry interaction at all.
- Pushing an image containing proprietary application code to a public registry by mistake, instead
  of a properly-configured private one.
- Confusing the daemon's role with the client's — the client is just the interface; the daemon is
  what actually builds images and runs containers.

## ➡️ Next

Continue to [writing-dockerfiles.md](writing-dockerfiles.md) to actually build a real image,
starting from a Dockerfile.
