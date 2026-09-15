# 🖥️ Virtual Machines

## The Most Foundational Cloud Compute Resource

A **virtual machine (VM)** is a complete, virtualized computer — its own virtual CPU, memory, disk,
and operating system — running on a cloud provider's physical hardware. It's the direct cloud
equivalent of the VM concept already introduced in
[introduction-to-containers.md](../docker-and-containerization/introduction-to-containers.md), now
as something an organization actually rents rather than a general architectural concept.

## Launching a Virtual Machine, Conceptually

```
1. Choose a MACHINE IMAGE - the base operating system (Ubuntu,
   Amazon Linux) and any pre-installed software
2. Choose an INSTANCE TYPE - how much CPU and memory the VM gets
   (a t2.micro is small/cheap; larger types cost proportionally
   more)
3. Choose NETWORKING settings - which virtual network it joins,
   what traffic is allowed
4. LAUNCH - the provider provisions a real, running VM, typically
   within minutes
```

This directly parallels the Terraform `aws_instance` example already introduced in
[infrastructure-basics.md](../devops-foundations/infrastructure-basics.md) — launching a VM through
a cloud console is the manual equivalent of exactly what that Infrastructure as Code example
automates.

## What Runs on a VM

```
A cloud VM is, from the OS's own perspective, indistinguishable
from a physical computer - it can run:
  - a Docker daemon, hosting containers (per Docker and
    Containerization)
  - Nginx, acting as a reverse proxy (per Nginx and Reverse
    Proxies)
  - a database directly, or any other server software
```

This is a genuinely useful mental model: everything covered in this domain's earlier modules —
containers, Nginx, a backend application — runs perfectly normally *inside* a cloud VM, exactly as
it would on a physical machine sitting under someone's desk.

## Scaling: Vertical vs. Horizontal

```
VERTICAL scaling  → give the SAME VM more CPU/memory (a bigger
                     instance type) - simple, but has a real
                     ceiling, and requires downtime to resize

HORIZONTAL scaling → run MORE VMs, each handling a share of the
                     traffic (load-balanced, per reverse-proxy-
                     concepts.md) - has no fixed ceiling, but
                     requires the application to genuinely support
                     running multiple instances
```

This distinction is genuinely important for real capacity planning: vertical scaling is simpler to
reason about but eventually hits a hard limit, while horizontal scaling — directly enabled by the
load-balancing concept already covered in
[reverse-proxy-concepts.md](../nginx-and-reverse-proxies/reverse-proxy-concepts.md) — scales much
further, at the cost of needing an application actually designed to run as multiple, independent
instances.

## Ephemeral vs. Persistent VM State

```
A VM's own local disk behaves like a container's writable layer
(per docker-images-and-containers.md) - data on it can be LOST if
the VM is terminated, unless it's on separate, persistent block
storage (per compute-storage-and-networking.md).
```

This is exactly the same lesson already established for containers, now applying at the VM level:
genuinely important data belongs on explicitly persistent storage, never assumed to survive simply
because "it's on the server" — a VM can be terminated and replaced just as readily as a container
can.

## Common Mistakes

- Assuming a VM's local disk is inherently durable, then losing real data when the VM is terminated
  or replaced without that data living on separate persistent storage.
- Reaching immediately for horizontal scaling before the application has actually been designed to
  run correctly as multiple simultaneous instances (shared state, per the concerns already covered
  in [managing-shared-state-between-services.md](../../artificial-intelligence/multi-agent-architecture-concerns/managing-shared-state-between-services.md)).
- Over-provisioning a much larger instance type than an application actually needs, incurring
  unnecessary ongoing cost for capacity that's never actually used.

## ➡️ Next

Continue to [cloud-deployment-models.md](cloud-deployment-models.md) to see how organizations
choose between running entirely in the cloud, entirely on their own infrastructure, or a mix of
both.
