# 🐳 Docker and Containerization

## 📚 Overview

[DevOps Foundations](../devops-foundations/) established the dev/prod parity problem and pointed to
containers as its practical solution. This module delivers on that: a complete, hands-on
introduction to Docker — containers vs. VMs, images vs. containers, writing real Dockerfiles,
networking and persisting data between containers, and Docker Compose for tying a full multi-service
application together in one file.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain how a container differs from a VM, and why containers close the dev/prod tools gap.
- Distinguish a Docker image from a container, and understand layer caching.
- Write a real Dockerfile — including a multi-stage build and `.dockerignore` — to containerize a
  backend service.
- Set up container networking and volumes for a multi-container application.
- Define a complete, multi-service application with Docker Compose.

## 📋 Prerequisites

- [DevOps Foundations](../devops-foundations/) — this module directly delivers on the dev/prod parity problem introduced there.
- [Express.js Fundamentals](../../backend/expressjs-fundamentals/) — the backend service containerized throughout this module's examples.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [introduction-to-containers.md](introduction-to-containers.md) | Containers vs. VMs: shared kernel, isolation, and why containers start faster |
| [docker-images-and-containers.md](docker-images-and-containers.md) | Images as templates, containers as instances, and layer caching |
| [docker-architecture.md](docker-architecture.md) | The client/daemon/registry model behind every Docker command |
| [writing-dockerfiles.md](writing-dockerfiles.md) | FROM/WORKDIR/COPY/RUN/EXPOSE/CMD, containerizing a real backend service, multi-stage builds, `.dockerignore` |
| [container-networking.md](container-networking.md) | User-defined networks, name-based DNS, exposing vs. publishing ports |
| [container-volumes.md](container-volumes.md) | Named volumes vs. bind mounts, and persisting data beyond a container's lifetime |
| [docker-compose.md](docker-compose.md) | Defining a complete multi-service application in one declarative file; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you'll be containerizing any real application — the Dockerfile, networking, and
volumes files are directly hands-on, practical skills you'll use immediately.

**Skim** if you already have solid Docker experience — this module establishes the vocabulary and
patterns [CI/CD Pipelines](../ci-cd-pipelines/), later in this domain, builds on.

## 🧠 Knowledge Check

<details>
<summary>Why does copying <code>package*.json</code> and running <code>npm install</code> BEFORE copying the rest of the application code matter for build speed?</summary>

Docker caches each layer of a build. As long as `package.json` hasn't changed, Docker reuses the
cached `npm install` layer on every rebuild, rather than reinstalling dependencies from scratch.
Copying the rest of the (frequently-changing) code afterward means only that layer needs rebuilding
on an ordinary code edit — dependency installation stays cached.

</details>

<details>
<summary>Why should a database container's port typically be exposed but never published?</summary>

Exposing a port makes it reachable by other containers on the same network and by the Docker host —
exactly what a backend container needs to reach the database. Publishing a port makes it reachable
from outside the host entirely, including the public internet — something a database should almost
never be, since only the backend service should ever connect to it directly.

</details>

## 📚 References

- [Docker - What Is a Container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) — official documentation on containers vs. VMs
- [Docker - Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/) — official documentation for the multi-stage build pattern used in this module
- [Docker - Networking Overview](https://docs.docker.com/engine/network/) and [Volumes](https://docs.docker.com/engine/storage/volumes/) — official documentation for this module's networking and persistence content
- [Docker - Compose Getting Started](https://docs.docker.com/compose/gettingstarted/) — official documentation for the Docker Compose example in this module

## ➡️ Continue Your Learning Path

Continue to [CI/CD Pipelines](../ci-cd-pipelines/) to see how building and testing a containerized
application like this one is automated on every code change.
