# 🚀 Production Systems

## 📚 Overview

These modules take an application from a developer's machine to a service people use: DevOps practices, containers, domains and HTTPS, reverse proxies, cloud infrastructure, CI/CD pipelines, monitoring, and logging in production. They assume you understand how a typical web application is built, as covered in the [backend path](../backend/README.md).

## 🧭 The Learning Path

Work through the modules in this order. The last column names the earlier modules each one relies on, so you can also start partway through; links point to modules in other areas.

| # | Module | What it covers | Builds on |
|---|--------|----------------|-----------|
| 1 | [DevOps Foundations](devops-foundations/README.md) | DevOps, keeping development and production alike, infrastructure as code, and environments | How a web application is built, as in the [backend path](../backend/README.md) |
| 2 | [Docker and Containerization](docker-and-containerization/README.md) | Containers and images, Dockerfiles, networking, volumes, and Docker Compose | DevOps Foundations, [Express.js Fundamentals](../backend/expressjs-fundamentals/README.md) |
| 3 | [Domains, DNS, and SSL](domains-dns-and-ssl/README.md) | DNS records and resolution, TLS certificates, and an HTTPS deployment | Docker |
| 4 | [Nginx and Reverse Proxies](nginx-and-reverse-proxies/README.md) | Reverse proxies, configuration, routing requests to services, and serving static files | Domains, DNS, and SSL, Docker |
| 5 | [Cloud Infrastructure Fundamentals](cloud-infrastructure/README.md) | Service models, compute, storage and networking, virtual machines, and cloud deployment models | Docker, Nginx |
| 6 | [CI/CD Pipelines](ci-cd-pipelines/README.md) | GitHub Actions: build, test, and deploy, with rollback and scoped secrets | DevOps Foundations, Docker |
| 7 | [Monitoring and Observability](monitoring-and-observability/README.md) | Metrics, logs, and traces, health checks, and alerting | CI/CD Pipelines |
| 8 | [Logging in Production](logging-in-production/README.md) | Log levels, structured logs and request IDs, central log storage, and retention | Monitoring and Observability, [Logging and Monitoring](../backend/logging-and-monitoring/README.md) |

## ➡️ Start Here

Begin with [DevOps Foundations](devops-foundations/README.md). After the last module, the course continues with [Web Security](../web-security/README.md).
