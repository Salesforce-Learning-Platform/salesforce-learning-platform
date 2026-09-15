# 🌐 Container Networking

## Real Applications Are Rarely Just One Container

A [containerized backend service](writing-dockerfiles.md) rarely runs entirely alone — it usually
needs to talk to a database, a cache, or another backend service, each commonly running in its own
separate container. Container networking is how these separate, isolated containers actually
communicate with each other.

## The Default Bridge Network — and Its Real Limitation

```
Any container started WITHOUT specifying a network joins Docker's
DEFAULT bridge network automatically.

Containers on the default bridge CAN reach each other, but ONLY
by IP address — NOT by container name.
```

This is a genuinely important, easy-to-miss limitation: on the default network, one container can't
simply refer to another by a friendly name like `database` — it would need that container's actual,
potentially-changing IP address, which is fragile and impractical for real applications.

## User-Defined Networks Fix This With Real DNS

```bash
docker network create my-app-network

docker run --network my-app-network --name database postgres:16
docker run --network my-app-network --name backend my-backend:1.0
```

```js
// Inside the "backend" container's code, this just WORKS:
const dbUrl = "postgresql://database:5432/myapp";
```

On a **user-defined** bridge network, Docker runs its own embedded DNS server, letting containers
resolve each other by the `--name` they were started with. This is exactly why a backend container
can connect to `database:5432` as though `database` were a real, resolvable hostname — because
within this network, it genuinely is one.

## Exposing vs. Publishing — a Real, Practical Distinction

```
EXPOSE (Dockerfile instruction, or default network behavior):
  → a port is reachable by OTHER CONTAINERS on the same network,
    and by the Docker HOST itself

PUBLISH (`-p` flag at `docker run` time):
  → a port is ALSO reachable from OUTSIDE the host entirely - the
    real, external world
```

This distinction matters for a real deployment's security posture: a database container's port
should typically be *exposed* (reachable by the backend container that needs it) but never
*published* (reachable directly from the public internet) — the backend is the only thing that
should ever talk to it directly.

```bash
# The backend needs to be reachable externally
docker run --network my-app-network -p 3000:3000 --name backend my-backend:1.0

# The database should NEVER be published externally - only exposed
# to other containers on the same network
docker run --network my-app-network --name database postgres:16
```

## Common Mistakes

- Relying on the default bridge network and hardcoding a container's IP address, instead of using a
  user-defined network with proper name-based DNS resolution.
- Publishing a database or internal service's port to the host (and therefore potentially the public
  internet) when it should only ever be exposed to other containers on the same private network.
- Forgetting that containers on genuinely *different* Docker networks can't reach each other at all
  by default, even if they're running on the same physical host.

## ➡️ Next

Continue to [container-volumes.md](container-volumes.md) to see how data — like a database's actual
stored records — can persist beyond a single container's lifetime.
