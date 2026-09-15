# ☁️ Cloud Infrastructure Fundamentals

## 📚 Overview

Every module in this domain so far has referred to "a server" somewhat abstractly. This module
finally covers where that server actually lives: rented infrastructure from a cloud provider like
AWS, Google Cloud, or Azure. It covers the core service models (IaaS/PaaS/SaaS), the three
fundamental resource categories (compute, storage, networking), virtual machines specifically, and
the deployment models organizations choose between.

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Explain cloud computing's on-demand, pay-as-you-go model, and distinguish IaaS, PaaS, and SaaS.
- Identify compute, storage, and networking as the fundamental building blocks behind every cloud
  service.
- Explain what a virtual machine is, and the trade-offs between vertical and horizontal scaling.
- Choose an appropriate deployment model (public, private, hybrid) for a given workload's actual
  requirements.

## 📋 Prerequisites

- [Docker and Containerization](../docker-and-containerization/) and [Nginx and Reverse Proxies](../nginx-and-reverse-proxies/) — this module explains where the infrastructure running those technologies actually lives.

## 📂 Module Contents

| File | Description |
|------|-------------|
| [cloud-computing-fundamentals.md](cloud-computing-fundamentals.md) | On-demand, pay-as-you-go computing, and the IaaS/PaaS/SaaS spectrum |
| [compute-storage-and-networking.md](compute-storage-and-networking.md) | The three fundamental resource categories every cloud service is built from |
| [virtual-machines.md](virtual-machines.md) | Launching a VM, what runs on it, and vertical vs. horizontal scaling |
| [cloud-deployment-models.md](cloud-deployment-models.md) | Public, private, and hybrid cloud, with a practical decision framework; closes with a Module Summary |

## 🔍 When to Deep-Dive vs. Skim

**Deep-dive** if you'll be provisioning or choosing cloud infrastructure for a real project — every
concept here directly informs a genuine architectural decision.

**Skim** if you're working within a platform that already abstracts these choices away — the
underlying vocabulary is still worth knowing for reading documentation and reasoning about cost and
scaling trade-offs.

## 🧠 Knowledge Check

<details>
<summary>What's the key difference between IaaS and PaaS, and where does "managing your own Dockerfile and Nginx config" fall on that spectrum?</summary>

IaaS provides raw building blocks (virtual servers, storage, networking) with the customer managing
the OS, runtime, and application; PaaS manages the underlying infrastructure, leaving the customer
to manage only application code and configuration. Manually managing a Dockerfile and Nginx
configuration sits closer to IaaS — you're responsible for most of the stack yourself.

</details>

<details>
<summary>Why does horizontal scaling have no fixed ceiling the way vertical scaling does, but require more from the application itself?</summary>

Vertical scaling means giving one instance more resources, which eventually hits a hardware limit.
Horizontal scaling means running more instances behind a load balancer — there's no inherent limit
to how many instances can run, but the application must actually be designed to run correctly as
multiple simultaneous, independent instances (handling shared state correctly, for instance).

</details>

## 📚 References

- [AWS - What Is Cloud Computing?](https://aws.amazon.com/what-is-cloud-computing/) — official definitions for cloud computing and the IaaS/PaaS/SaaS service models
- [AWS - Public Cloud vs. Private Cloud](https://aws.amazon.com/compare/the-difference-between-public-cloud-and-private-cloud/) — official comparison of cloud deployment models

## ➡️ Continue Your Learning Path

Continue to [CI/CD Pipelines](../ci-cd-pipelines/) to see how code actually gets built, tested, and
deployed onto infrastructure like this automatically.
