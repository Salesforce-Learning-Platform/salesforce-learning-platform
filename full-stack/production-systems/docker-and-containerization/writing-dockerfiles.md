# 📝 Writing Dockerfiles

## The Core Instructions, One at a Time

```dockerfile
FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

This is a real, working Dockerfile for a typical Node.js backend service. Each instruction plays a
specific, distinct role:

```
FROM     → the BASE image everything else builds on top of (here,
           an official, minimal Node.js image)
WORKDIR  → sets the working directory INSIDE the container for
           every instruction that follows
COPY     → copies files from the BUILD CONTEXT (your local
           project) into the image
RUN      → executes a command DURING the build (installing
           dependencies, compiling code) - its result is BAKED
           into the resulting image layer
EXPOSE   → documents which port the container listens on (doesn't
           actually publish it - that happens at `docker run` time
           with a -p flag)
CMD      → the DEFAULT command that runs when a container STARTS
           from this image
```

## Containerizing a Real Backend Service, Step by Step

```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

This directly containerizes an
[Express.js backend](../../backend/expressjs-fundamentals/) already covered earlier in this
repository — the same real application, packaged to run identically regardless of the host machine,
directly solving the tools-gap problem from
[development-to-production-lifecycle.md](../devops-foundations/development-to-production-lifecycle.md).

```bash
docker build -t my-backend:1.0 .
docker run -p 3000:3000 my-backend:1.0
```

`-p 3000:3000` maps the host machine's port 3000 to the container's exposed port 3000 — this is the
step that actually makes the containerized service reachable from outside the container.

## Why Copying `package*.json` Separately From the Rest of the Code Matters

```dockerfile
COPY package*.json ./     # ← changes RARELY
RUN npm install            # ← this expensive step gets CACHED
COPY . .                   # ← changes FREQUENTLY (every code edit)
```

This ordering directly exploits Docker's layer caching, covered in
[docker-images-and-containers.md](docker-images-and-containers.md): as long as `package.json` hasn't
changed, Docker reuses the cached `npm install` layer on every rebuild — meaning only *actual*
dependency changes trigger a fresh, slow `npm install`, while ordinary code edits rebuild almost
instantly.

## `.dockerignore` — Keeping the Build Context Clean

```
# .dockerignore
node_modules
.git
.env
*.log
```

Just like `.gitignore` excludes files from version control, `.dockerignore` excludes files from the
**build context** sent to the Docker daemon — critically, this prevents a local `node_modules`
folder (built for the host's own OS/architecture) from accidentally overwriting the one installed
*inside* the container, and keeps secrets like `.env` files out of the image entirely.

## Multi-Stage Builds: Smaller, Safer Final Images

```dockerfile
# Stage 1: build
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: runtime — only what's actually needed to RUN the app
FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

Multiple `FROM` statements define genuinely separate build stages — the first stage has every build
tool and dev dependency needed to *build* the application; the final stage, using `COPY --from=
builder`, pulls in *only* the compiled output and production dependencies, discarding every build
tool entirely. The resulting final image is meaningfully smaller and has a smaller attack surface,
since tools only needed at build time never ship in the actual runtime image.

## Common Mistakes

- Copying the entire project before running `npm install`, defeating Docker's layer cache and
  forcing a full dependency reinstall on every single code change.
- Omitting `.dockerignore`, accidentally including a host-installed `node_modules` folder, `.git`
  history, or a `.env` file with real secrets inside the built image.
- Skipping multi-stage builds for a compiled/built application, shipping an unnecessarily large
  final image containing build tools no longer needed at runtime.

## ➡️ Next

Continue to [container-networking.md](container-networking.md) to see how a containerized service
like this one actually communicates with other containers.
