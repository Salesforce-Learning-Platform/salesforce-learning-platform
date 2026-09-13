# What Is the Internet?

## Intuition

Imagine every postal service in every country agreed to use the same envelope format and the
same rules for reading an address, so that a letter from Mumbai could reach a mailbox in Toronto
even though no single postal worker knows the entire route. The Internet is the digital
equivalent of that agreement: it is not a single network owned by one company, but a very large
number of independently-operated networks that have agreed to speak the same set of rules
(protocols) so that data can move between any two of them.

## The Correct Technical Model

**The Internet is a network of networks.** Home networks, university networks, corporate
networks, mobile carrier networks, and data-center networks are each self-contained. They
interconnect through **Internet Service Providers (ISPs)** and **backbone providers**, using a
shared set of open protocols — most importantly the **Internet Protocol (IP)**, which is why the
whole system is often just called "the Internet" (short for "interconnected networks").

No single organization owns or controls the Internet. Instead:

- Technical standards are defined by open bodies such as the **IETF** (Internet Engineering Task
  Force), which publishes protocol specifications as **RFCs** (Requests for Comments).
- Address space and domain name policy are coordinated by **ICANN** (Internet Corporation for
  Assigned Names and Numbers) and regional registries.
- Physical connectivity between networks is negotiated commercially between ISPs and backbone
  operators (a relationship called "peering" or "transit").

This decentralization is a deliberate design property, not an accident: the Internet's
predecessor, ARPANET, was designed in the late 1960s–70s to keep working even if individual links
or nodes failed, by routing data around damage rather than depending on one central switchboard.

## Internet vs. the Web — the Most Important Distinction in This Module

Beginners very commonly use "the Internet" and "the Web" interchangeably. They are not the same
thing, and the distinction matters as soon as you start reasoning about how anything actually
works.

| | The Internet | The Web (World Wide Web) |
|---|---|---|
| What it is | The global network infrastructure — cables, routers, ISPs, and the protocols (IP, TCP, UDP) that move data between machines | One **application** that runs on top of that infrastructure, made of linked documents (pages) accessed over HTTP/HTTPS |
| Introduced | Late 1960s (ARPANET), matured through the 1970s–80s | 1989–1991, invented by Tim Berners-Lee at CERN |
| Core building blocks | IP addresses, routing, TCP/UDP | URLs, HTML, HTTP/HTTPS, browsers |
| Other things that run on it | Email (SMTP), file transfer, video calls, gaming, IoT devices, Salesforce API calls | — |

A useful test: email, a Zoom call, and an SSH session into a server all use **the Internet**, but
none of them use **the Web**. The Web is one (extremely important) tenant of the Internet, not a
synonym for it.

## Packet Switching, at an Intuitive Level

The Internet moves data by breaking it into small chunks called **packets**, sending each packet
independently, and reassembling them at the destination. This is called **packet switching**, and
it's covered in mechanical detail in
[tcp-ip-ports-and-routing.md](tcp-ip-ports-and-routing.md). The intuition worth carrying forward
from this file:

- Packets from the same conversation can take **different physical routes** and still arrive
  correctly, because each one carries enough addressing information to find its own way.
- This is fundamentally different from a traditional phone call, which reserves one dedicated
  circuit for the whole conversation (**circuit switching**). Packet switching is more resilient
  (a failed link doesn't kill the conversation, traffic just reroutes) and lets many conversations
  share the same physical wires efficiently.

## Common Misconceptions

- **"The Internet is basically the Web."** No — see the comparison table above. The Web is one
  application among many that the Internet carries.
- **"The Internet is owned by a company or a government."** No single entity owns it. It exists
  because independently-owned networks agree to interconnect and speak common protocols.
- **"The 'cloud' is a separate thing from the Internet."** Cloud computing (including Salesforce's
  infrastructure) is simply computers in data centers, reachable over the same Internet described
  in this module. "The cloud" is a deployment model, not a different network.

## Why This Matters for Frontend and Salesforce Engineers

You will spend most of your career working one layer above this content — building UIs that call
HTTP APIs. But you're building on top of it: a slow API is often a network problem before it's a
code problem, an "unreachable server" error might mean a DNS misconfiguration rather than a
crashed application, and every Salesforce Named Credential or Experience Cloud custom domain is a
thin, application-facing wrapper around the Internet fundamentals covered in this module.

## Next

Continue to
[clients-servers-and-local-networks.md](clients-servers-and-local-networks.md) to see how
individual devices actually connect to this network of networks.
