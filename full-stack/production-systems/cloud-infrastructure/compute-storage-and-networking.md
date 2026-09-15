# 🧱 Compute, Storage, and Networking

## Three Fundamental Resource Categories

Every cloud provider, regardless of specific product names, fundamentally sells the same three
categories of resource — everything more specific (a managed database, a container service, a CDN)
is built on top of these three primitives.

## Compute: Where Code Actually Runs

```
COMPUTE = raw processing power - CPU, memory, the actual machine
          (virtual or physical) that runs an application's code

Cloud examples: a virtual machine (AWS EC2, covered next in
  virtual-machines.md), a serverless function, a managed
  container-running service
```

This is the most direct analog to the physical hardware a
[Docker container](../docker-and-containerization/) actually runs on — in the cloud, that
underlying compute resource is rented rather than owned.

## Storage: Where Data Actually Lives

```
BLOCK storage → attached directly to ONE compute instance, like a
                virtual hard drive - fast, but tied to that
                specific instance

OBJECT storage → a separate, independently-accessible store for
                files (images, backups, static assets) - not
                "attached" to any one server, reachable over the
                network from anywhere
```

This distinction directly parallels
[container-volumes.md](../docker-and-containerization/container-volumes.md)'s named-volume-vs-
bind-mount comparison from earlier in this domain: block storage is like a dedicated resource tied
to one instance, while object storage is independently managed and accessible, much like a Docker
named volume is managed independently of any one container.

## Networking: How It All Connects

```
VIRTUAL NETWORK (a "VPC" on AWS) → an isolated, private network
  within the cloud provider's infrastructure, where an
  organization's own resources live

SECURITY GROUPS / FIREWALL RULES → control exactly which traffic
  is allowed IN and OUT of a given resource
```

This is the cloud-scale equivalent of the container networking already covered in
[container-networking.md](../docker-and-containerization/container-networking.md) — the same
underlying principle (deliberately controlling what can reach what) applies at every layer, from a
single Docker network up to an entire cloud provider's virtual networking.

## How These Three Combine in a Real Deployment

```
1. COMPUTE instance (a virtual machine) runs the containerized
   application
2. STORAGE (a block volume) holds the application's persistent
   data, OR object storage holds uploaded user files
3. NETWORKING (a virtual network + security group rules) controls
   exactly what can reach that compute instance, and what it
   can reach in turn
```

Every real cloud deployment is, at its core, a combination of these three resource categories
configured together — the specific managed services layered on top (a managed database, a load
balancer) are conveniences built from these same underlying primitives.

## Common Mistakes

- Attaching block storage to hold files that genuinely need independent, network-wide
  accessibility, when object storage is the actual right tool for that use case.
- Leaving default, overly permissive networking/security group rules in place, exposing resources
  more broadly than actually necessary.
- Treating "compute" as synonymous with "a virtual machine" specifically, when modern cloud compute
  also includes serverless and container-native options with genuinely different trade-offs.

## ➡️ Next

Continue to [virtual-machines.md](virtual-machines.md) to see the most common, foundational form
of cloud compute in detail.
