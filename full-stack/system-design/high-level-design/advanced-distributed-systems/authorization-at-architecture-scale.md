# 🔐 Authorization at Architecture Scale

## Beyond a Single Service's Auth Check

[Authentication Attacks](../../../web-security/authentication-attacks/) and
[Production Authentication Architecture](../../../backend/production-authentication-architecture/),
both already covered in this repository, established how a single service authenticates and
authorizes a request. This file covers what genuinely changes once authorization must work
*consistently* across an entire microservices architecture, not just one backend.

## The Problem: Every Service Re-Implementing Its Own Auth Logic

```
WITHOUT a coordinated approach, EVERY microservice would need to:
  - independently VALIDATE the user's identity
  - independently CHECK whether that user has permission for
    THIS specific action
  - independently STAY in sync with every OTHER service's
    permission rules
```

This is genuinely error-prone and duplicative — directly the same problem
[the API Gateway pattern](../core-infrastructure/api-gateway-pattern.md), earlier in this domain,
already solved for authentication specifically, now considered for authorization as well.

## The Pattern: a Centralized Identity Provider, Services as Resource Servers

```
1. A dedicated IDENTITY PROVIDER (IdP) authenticates the user
   ONCE, issuing a signed JWT access token containing the user's
   identity and CLAIMS (permissions)
2. Every individual microservice becomes a RESOURCE SERVER - it
   TRUSTS an already-validated token, rather than re-implementing
   authentication itself
3. Each service still makes its OWN authorization DECISION (does
   THIS user have permission for THIS specific action?), but
   based on CLAIMS already present in the trusted token
```

Per microservices.io's own architecture guidance, this is the current, widely-adopted pattern —
authentication is centralized once, at the IdP, while authorization *decisions* remain distributed,
each service still deciding for itself based on shared, trusted claims.

## Propagating Identity Across Service Calls

```
User Request → API Gateway → validates JWT → forwards the SAME
  JWT to URL Service → URL Service forwards it to Analytics
  Service, if IT also needs to know WHO made the original request
```

This directly connects to [JWT Security](../../../web-security/authentication-attacks/jwt-security.md),
already covered in this repository's Web Security domain — the *same* signed token, validated once
at the boundary, is passed along through internal service-to-service calls, so each downstream
service can verify the original user's identity and permissions without needing its own, separate
authentication step.

## OAuth 2.0 and OpenID Connect

```
OAuth 2.0    → the STANDARD protocol for AUTHORIZATION (granting
  access without sharing a genuine password)

OpenID Connect (OIDC) → built ON TOP of OAuth 2.0, adding
  AUTHENTICATION (verifying WHO the user actually is)
```

These are genuinely the industry-standard protocols underlying most real IdP implementations — worth
knowing by name specifically because they're what a genuinely production-grade authentication and
authorization system is almost always actually built on, rather than a fully custom, in-house
protocol.

## Service-to-Service Authorization: When There's No Real "User"

```
For calls with NO real, originating human user (a scheduled
background job, one service calling another directly) - a
SEPARATE mechanism (OAuth's Client Credentials flow, issuing a
SERVICE-level token) authorizes the CALLING SERVICE itself,
rather than any individual user.
```

This is a genuinely important, distinct case worth naming explicitly — not every internal request
has a genuine human user behind it, and the authorization mechanism needs to account for this
service-to-service case separately from ordinary, user-initiated requests.

## Common Mistakes

- Having each microservice independently re-implement authentication logic, risking genuine
  inconsistency and duplicated effort across services.
- Forwarding a user's original JWT to internal services without validating it hasn't expired or
  been revoked at each hop.
- Conflating authentication (who is this?) with authorization (what can they do?) as a single,
  undifferentiated concept, when they're genuinely distinct concerns, even when handled by the same
  centralized token.

## ➡️ Next

Continue to [designing-search-systems.md](designing-search-systems.md) for the final concept in
this module, and a preview of the complete, worked design problems this domain closes with.
