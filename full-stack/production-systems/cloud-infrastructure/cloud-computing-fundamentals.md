# ☁️ Cloud Computing Fundamentals

## Where Does a Server Actually Live?

Every module in this domain so far has referred to "a server" somewhat abstractly — something
running [Docker containers](../docker-and-containerization/), reachable via
[DNS](../domains-dns-and-ssl/), fronted by [Nginx](../nginx-and-reverse-proxies/). This module
finally answers where that server actually *is*: for the overwhelming majority of modern
applications, it's a resource rented from a **cloud provider** — AWS, Google Cloud, or Microsoft
Azure being the three largest.

## What Cloud Computing Actually Means

```
"Cloud computing is the ON-DEMAND delivery of IT resources over
the Internet with PAY-AS-YOU-GO pricing."
```

This is AWS's own definition, and it names the two genuinely important properties: **on-demand**
(a server can be provisioned in minutes, not weeks, unlike physically purchasing and racking
hardware) and **pay-as-you-go** (cost scales with actual usage, rather than a large upfront capital
purchase).

## Three Service Models: IaaS, PaaS, SaaS

```
IaaS (Infrastructure as a Service)
  → the RAW building blocks: virtual servers, storage, networking
  → YOU manage the OS, runtime, and application
  → example: a raw AWS EC2 virtual machine

PaaS (Platform as a Service)
  → the underlying infrastructure is ALREADY managed for you
  → YOU manage only your application code and its configuration
  → example: a managed deployment platform that just runs your
    already-containerized app

SaaS (Software as a Service)
  → a COMPLETE, ready-to-use product, run entirely by the provider
  → YOU manage nothing beyond using the software itself
  → example: a web-based email service
```

This is a genuinely useful spectrum for understanding *where* a given cloud service sits: as you
move from IaaS toward SaaS, you give up control and flexibility in exchange for less operational
responsibility — neither end is universally "better," it depends entirely on how much control a
given project actually needs.

## Where This Domain's Prior Modules Fit on This Spectrum

```
Writing Dockerfiles, configuring Nginx yourself, managing your
OWN server → closer to IaaS - you're responsible for most of the
              stack

Deploying a container to a managed container-hosting service that
handles scaling and networking for you → closer to PaaS
```

Recognizing which layer a given tool or service operates at is genuinely useful for understanding
*why* it requires the configuration it does — an IaaS-level tool inherently needs more manual setup
than a PaaS-level one, by design, not by accident.

## Why "The Cloud" Isn't Actually Magic

```
"The cloud" is, physically, someone ELSE's real, physical data
center - actual servers, actual hard drives, actual networking
equipment, owned and operated by AWS/Google/Microsoft, that you
rent access to remotely.
```

This is a genuinely useful mental model to hold onto: nothing about cloud computing is
conceptually different from the servers and infrastructure already covered in
[DevOps Foundations](../devops-foundations/) — it's the *same* underlying hardware and networking
concepts, just owned and operated by a specialized provider instead of an organization's own
physical premises.

## Common Mistakes

- Treating "the cloud" as a fundamentally different, more abstract concept than physical servers,
  rather than understanding it as rented, remotely-managed physical infrastructure.
- Choosing an IaaS-level service for a project that would be served much better (with far less
  operational overhead) by a PaaS-level one, or vice versa.
- Assuming pay-as-you-go pricing is automatically cheaper than owning hardware — for a genuinely
  large, constant, predictable workload, this isn't always true, and the trade-off is worth
  evaluating deliberately.

## ➡️ Next

Continue to
[compute-storage-and-networking.md](compute-storage-and-networking.md) to see the three
fundamental categories of resource every cloud provider actually offers.
