# Clients, Servers, and Local Networks

## Intuition

When you open a browser and visit a site, your laptop is asking a question and a computer
somewhere else is answering it. The asker is the **client**; the answerer is the **server**. Your
laptop doesn't talk to that server directly over open air — it first has to get onto the
Internet through a chain of intermediate equipment, starting inside your own home or office.

## The Client-Server Model

A **client** is any device or program that initiates a request for a resource or service. A
**server** is a device or program that listens for those requests and responds to them.

- **Client**: your laptop's browser, a mobile app, `curl`, Salesforce making an outbound API
  callout.
- **Server**: a web server hosting a site, a Salesforce org's application servers, a REST API
  backend, a mail server.

Two things worth being precise about:

1. **Client/server is a role, not a device category.** The same physical machine can be a client
   in one interaction and a server in another. A Salesforce org acts as a *server* when your
   browser loads it, and as a *client* when it makes an outbound HTTP callout to an external API.
2. **Servers are built to listen continuously.** A server process binds to a network port and
   waits ("listens") for incoming connections; it doesn't have to already know who will connect.
   Clients, by contrast, typically initiate a connection when they need something and then stop.

```text
   CLIENT                                   SERVER
┌───────────┐        request        ┌───────────────────┐
│  Browser  │ ─────────────────────▶│  Web / App Server  │
│           │◀───────────────────── │  (always listening)│
└───────────┘        response       └───────────────────┘
```

## End Devices and Network Interfaces

An **end device** (or "host") is anything with its own network identity that can send and receive
data: a laptop, phone, smart TV, printer, or server. Every end device connects to a network
through a **network interface** — physically a Wi-Fi radio or Ethernet port, logically represented
by the operating system as a network adapter with its own addresses (a MAC address and, once
connected, an IP address — covered in
[ip-addressing-and-nat.md](ip-addressing-and-nat.md)).

A device can have multiple interfaces (Wi-Fi and Ethernet on the same laptop, or Wi-Fi and
cellular on a phone) and therefore multiple addresses at once, one per interface.

## Local Networks (LANs)

A **local area network (LAN)** is a small, self-contained network confined to one location — a
home, an office floor, a building. Devices on the same LAN can typically reach each other directly
without going through the wider Internet at all (e.g., your laptop printing to a wireless printer
in the next room).

Two devices connect a LAN to the outside world and to each other:

### Switches

A **switch** connects multiple devices *within* the same local network and forwards traffic
between them based on **MAC addresses** (the hardware address burned into a network interface —
see [ip-addressing-and-nat.md](ip-addressing-and-nat.md) for how it differs from an IP address).
A switch operates at the local-network level: it has no concept of "the Internet" and cannot, by
itself, get a packet outside the building.

### Routers

A **router** connects *different* networks to each other and decides, based on **IP addresses**,
which direction to forward a packet so it gets closer to its destination. The router in a typical
home or office sits at the boundary between the LAN and the ISP's network, and is the device that
actually gets your traffic "onto the Internet."

| | Switch | Router |
|---|---|---|
| Connects | Devices within one local network | Different networks to each other |
| Forwards based on | MAC address | IP address |
| Typical scope | Inside a building | Between a LAN and the ISP / other networks |
| "Knows about the Internet"? | No | Yes — holds routing information about where to send traffic next |

Most consumer "routers" sold for home use are actually combined devices: a switch (for the wired
LAN ports), a Wi-Fi access point, and a router (for the connection out to the ISP), bundled into
one box. This is a common source of the router-vs-switch confusion — the box does both jobs, but
the jobs themselves remain distinct.

## Internet Service Providers (ISPs)

An **ISP** is a company that owns or leases the physical infrastructure (fiber, cable, cellular
towers, satellite links) connecting your local network to the rest of the Internet, and that has
commercial interconnection agreements with other ISPs and backbone providers so traffic can reach
networks it doesn't own. When your home router sends a packet destined for a server on the other
side of the world, it hands that packet to your ISP, which forwards it — possibly through several
other ISPs and backbone networks — toward its destination.

```text
Your device (client)
     │  Wi-Fi / Ethernet
     ▼
Local network (switch)
     │
     ▼
Router  (LAN boundary)
     │
     ▼
ISP network
     │
     ▼
Internet backbone / other ISPs
     │
     ▼
Destination network → Server
```

## Common Mistakes

- Assuming "router" and "switch" are interchangeable words for "the box under my desk." They
  perform genuinely different forwarding decisions, even when combined into one physical product.
- Believing a request goes directly from your device to the destination server over one continuous
  wire. In reality it hops through many independently-operated pieces of equipment, and the exact
  path can differ packet to packet or minute to minute.
- Forgetting that "client" and "server" describe a role in a given exchange, not a permanent
  identity of a machine.

## Next

Continue to [ip-addressing-and-nat.md](ip-addressing-and-nat.md) to see exactly how devices on
these networks are addressed and located.
