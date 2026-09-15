# 🏢 Cloud Deployment Models

## Three Ways to Combine Owned and Rented Infrastructure

[cloud-computing-fundamentals.md](cloud-computing-fundamentals.md) covered *service* models
(IaaS/PaaS/SaaS) — how much of the stack a provider manages. **Deployment models** answer a
genuinely different question: *where* does the infrastructure physically live, and who owns it?

## Public Cloud

```
Resources are operated by a THIRD-PARTY provider (AWS, Google
Cloud, Azure) and SHARED across many different customers on the
same underlying physical infrastructure — each customer's actual
resources remain fully isolated from every other customer's.

Ideal for: scalability, cost-efficiency, fast provisioning.
```

This is what every prior module in this domain has implicitly assumed — a virtual machine, rented
from a major cloud provider, is the public cloud model in its most common, everyday form.

## Private Cloud

```
Infrastructure is DEDICATED to a SINGLE organization - either
hosted on that organization's own physical premises, or hosted
externally but never shared with other customers.

Ideal for: strict compliance requirements, maximum control over
  the underlying hardware and network.
```

An organization handling especially sensitive, tightly-regulated data (certain healthcare or
financial systems) sometimes chooses private cloud specifically for this greater control — at the
real cost of losing the elasticity and lower operational overhead public cloud offers.

## Hybrid Cloud

```
An IT infrastructure design that INTEGRATES an organization's OWN
internal infrastructure with a THIRD-PARTY public cloud provider's
infrastructure and services - workloads and data can move between
the two as needed.
```

Hybrid cloud lets an organization deliberately choose the best-fitting deployment model *per
workload* — genuinely sensitive data might stay on private infrastructure, while a
public-facing, highly-variable-traffic application runs in the public cloud, both coexisting as
part of one overall system.

## A Practical Decision Framework

```
Does the workload have STRICT regulatory/compliance requirements
  that mandate specific physical control?           → private, or
                                                        hybrid
Does traffic vary UNPREDICTABLY, benefiting from
  elastic, on-demand scaling?                        → public
Does the organization need BOTH - some workloads
  regulated, others genuinely variable?               → hybrid
```

For most applications covered throughout this repository — a typical web application, an API, an
AI-powered feature — public cloud is the practical default, precisely because it offers the fastest
provisioning and the least ongoing infrastructure management overhead, matching the "start simple"
principle already established in [Understanding AI Agents](../../artificial-intelligence/understanding-ai-agents/)
for a genuinely analogous reason: added infrastructure complexity should be justified by an actual,
demonstrated need, not adopted by default.

## Common Mistakes

- Choosing private cloud infrastructure "for control" without a genuine compliance or regulatory
  requirement actually driving that need, incurring real, avoidable operational overhead.
- Assuming hybrid cloud is simply "using two providers" rather than a deliberate architectural
  choice about which specific workloads belong on which infrastructure, and why.
- Treating deployment model and service model (from
  [cloud-computing-fundamentals.md](cloud-computing-fundamentals.md)) as the same decision — they're
  genuinely independent axes; a private cloud can still offer IaaS, PaaS, or SaaS-style services
  internally.

## Module Summary

Across this module: **cloud computing** delivers IT resources on-demand with pay-as-you-go pricing,
across a service-model spectrum from IaaS (raw infrastructure) through PaaS (managed platform) to
SaaS (a complete product) — verified against AWS's own official definitions (see
[cloud-computing-fundamentals.md](cloud-computing-fundamentals.md)); **compute, storage, and
networking** are the three fundamental resource categories every cloud service is built from,
directly paralleling the container concepts already covered earlier in this domain (see
[compute-storage-and-networking.md](compute-storage-and-networking.md)); **virtual machines** are
the most foundational cloud compute resource, capable of running everything covered in this
domain's earlier modules, scaled either vertically (a bigger instance) or horizontally (more
instances, per this domain's reverse-proxy load balancing) (see
[virtual-machines.md](virtual-machines.md)); and **deployment models** — public, private, and
hybrid cloud — answer where infrastructure physically lives and who owns it, a genuinely separate
decision from the service model, chosen deliberately per workload rather than as a default.
