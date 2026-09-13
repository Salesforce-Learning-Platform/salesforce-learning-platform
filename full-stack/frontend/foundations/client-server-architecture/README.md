# Client-Server Architecture

## Purpose

[how-the-internet-works](../how-the-internet-works/) explained client and server as network
roles — who initiates a connection, who listens. This module goes one layer up: it explains how
that role split becomes an **application architecture**, with frontend and backend as separate
concerns with separate responsibilities, and a repeatable request-response lifecycle that every
web application follows regardless of framework.

## Learning Objectives

- Explain the client-server architectural pattern and why it dominates web application design.
- Draw a clear line between frontend responsibilities and backend responsibilities.
- Narrate the request-response lifecycle of a typical web application, including where state
  lives on each side.
- Recognize the tradeoffs of the client-server model compared to alternatives (peer-to-peer,
  monolithic desktop apps).

## Prerequisites

[How the Internet Works](../how-the-internet-works/), particularly
[clients-servers-and-local-networks.md](../how-the-internet-works/clients-servers-and-local-networks.md).

## Files in This Module

| File | Covers |
|---|---|
| [frontend-and-backend-responsibilities.md](frontend-and-backend-responsibilities.md) | What belongs on each side of the split, and why |
| [the-request-response-lifecycle.md](the-request-response-lifecycle.md) | The repeatable cycle every client-server interaction follows |
| [state-management-across-the-boundary.md](state-management-across-the-boundary.md) | Where state lives, and why HTTP's statelessness matters here |

## Salesforce Relevance

Salesforce is itself a client-server system at multiple levels: the browser is a client to
Lightning Experience's server-rendered and API-driven backend; a Lightning Web Component is a
client to Apex controllers and the underlying database; and an external system calling the
Salesforce REST/SOAP API is a client to the Salesforce org acting as server. The same
responsibility split described in this module — presentation and interaction on the client,
business logic and data authority on the server — is exactly why Apex, not client-side
JavaScript, is the trusted place to enforce sharing rules, validation, and business logic in
Salesforce applications.
