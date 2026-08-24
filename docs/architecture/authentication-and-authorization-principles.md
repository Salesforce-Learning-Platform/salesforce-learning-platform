# Authentication and Authorization Principles

## Purpose

This document defines the conceptual principles for identity, authentication, authorization, and access control within the Salesforce Learning Platform.

As the platform evolves, different users and systems may require different levels of access. Learners may access learning content and track progress. Contributors may create or maintain content. Reviewers may evaluate changes before publication. Administrators may manage platform-level configuration and access.

The platform must therefore distinguish clearly between:

- Who or what is interacting with the platform.
- How that identity is verified.
- What actions that identity is permitted to perform.
- Which resources or data that identity is allowed to access.

These principles establish an architectural foundation for future security and access-control decisions.

They do not prescribe a specific identity provider, authentication technology, Salesforce product, or authorization framework.

---

## Core Security Concepts

Authentication and authorization are related but different concepts.

### Authentication

Authentication answers the question:

> Who are you?

Authentication is the process of verifying the identity of a user, application, service, or other system interacting with the platform.

Conceptually:

```text
User or System
       |
       | Provides Identity Evidence
       v
+-----------------------+
| Authentication        |
|                       |
| Verify Identity       |
+-----------+-----------+
            |
            v
Verified Identity
```

Examples of authentication evidence may include:

- Username and password.
- Single sign-on.
- Security tokens.
- Multi-factor authentication.
- OAuth-based authentication.
- Federated identity.
- Service credentials.

The specific authentication mechanism should depend on the platform's implementation requirements and security model.

---

### Authorization

Authorization answers the question:

> What are you allowed to do?

Authorization determines whether an authenticated identity has permission to perform a requested action.

Conceptually:

```text
Authenticated Identity
        |
        | Requests Action
        v
+-----------------------+
| Authorization         |
|                       |
| Check Access Rules    |
+-----------+-----------+
            |
       +----+----+
       |         |
       v         v
    Allowed    Denied
```

Authentication should generally occur before authorization.

A platform should first establish who or what is making a request before determining what that identity is allowed to access.

---

## Core Architectural Principle

The primary principle established by this document is:

> Authentication establishes identity. Authorization determines access. These responsibilities should remain conceptually distinct.

The complete interaction can be represented as:

```text
User or System
       |
       v
+-----------------------+
| Authentication        |
|                       |
| Who are you?          |
+-----------+-----------+
            |
            v
     Verified Identity
            |
            v
+-----------------------+
| Authorization         |
|                       |
| What can you do?      |
+-----------+-----------+
            |
            v
      Access Decision
            |
       +----+----+
       |         |
       v         v
    Allowed    Denied
```

Keeping these concepts separate helps prevent unclear security responsibilities and supports future changes to identity or permission systems.

---

## Identity Should Have a Clear Source of Truth

Every platform user or system identity should originate from a clearly understood authoritative identity source.

The identity source may eventually provide information such as:

- Unique identifier.
- Authentication state.
- Identity type.
- Associated roles.
- Account status.
- Relevant attributes required for access decisions.

Conceptually:

```text
Identity Provider
       |
       v
+-----------------------+
| Authoritative         |
| Identity Source       |
+-----------+-----------+
            |
            +------------------+
            |                  |
            v                  v
      Learning Platform    External Service
```

The learning platform may consume identity information without necessarily becoming the authoritative owner of authentication credentials.

This principle supports the broader data ownership model established for the platform.

---

## Authentication Should Be Centralized Where Practical

Authentication should generally be handled through a clearly defined identity boundary rather than being independently implemented by every platform capability.

For example:

```text
                  +------------------+
                  | Identity Provider |
                  +---------+--------+
                            |
                            v
+---------------+    +------+-------+    +----------------+
| Learning      |    | Authentication|    | Assessment     |
| Content       |<---| Boundary      |--->| Capability     |
+---------------+    +------+-------+    +----------------+
                            |
                            v
                     +------+-------+
                     | Learner       |
                     | Progress      |
                     +--------------+
```

A centralized or federated identity approach can reduce:

- Duplicate credential management.
- Inconsistent authentication logic.
- Security implementation differences.
- Repeated identity verification.
- Unnecessary coupling between modules and authentication mechanisms.

This does not require every implementation to use a single technical service.

The architectural principle is that identity responsibilities should remain explicit and controlled.

---

## Authentication Should Not Be Confused With Application Roles

Successfully authenticating a user does not automatically determine what the user can do.

For example:

```text
Authentication

User Identity
     |
     v
Verified User

Authorization

Verified User
     |
     v
Determine Permissions
     |
     +--> Read Content
     |
     +--> Submit Assessment
     |
     +--> Create Content
     |
     +--> Review Content
     |
     +--> Administer Platform
```

The same authentication mechanism may support multiple categories of users with different authorization levels.

Authentication establishes identity.

Authorization determines the permitted actions associated with that identity.

---

## Principle of Least Privilege

Access should be limited to the permissions required to perform an intended responsibility.

This principle is commonly known as the principle of least privilege.

Conceptually:

```text
User Responsibility
        |
        v
Required Permissions
        |
        v
Grant Only Necessary Access
```

For example, a learner who needs to complete an assessment may require permission to:

- Access the assessment.
- Submit responses.
- View permitted results.

The learner should not automatically receive permission to:

- Modify assessment definitions.
- Access other learners' responses.
- Change platform configuration.
- Manage user roles.

Least privilege helps reduce unnecessary access and limits the impact of accidental or unauthorized actions.

---

## Access Should Be Based on Explicit Policies

Authorization decisions should be based on clearly defined access rules.

Conceptually:

```text
Authenticated Identity
        |
        v
Requested Action
        |
        v
+--------------------------+
| Access Policy            |
|                          |
| Identity Attributes      |
| Role                     |
| Permission               |
| Resource                 |
| Context                  |
+------------+-------------+
             |
             v
       Access Decision
```

Access policies may eventually consider:

- User role.
- Assigned permissions.
- Ownership of a resource.
- Resource state.
- Organizational or platform context.
- Authentication strength.
- System or service identity.

The specific authorization model should be selected when detailed platform requirements are defined.

---

## Roles and Permissions Should Represent Different Concepts

Roles and permissions should not be treated as identical concepts.

A role generally represents a category of responsibility.

A permission represents a specific allowed action.

For example:

```text
Role: Content Author
        |
        +--> Create Content
        |
        +--> Edit Assigned Content
        |
        +--> Submit Content for Review
```

Another example:

```text
Role: Content Reviewer
        |
        +--> View Submitted Content
        |
        +--> Approve Content
        |
        +--> Request Changes
```

The platform may eventually use roles to group related permissions.

However, the underlying access model should remain sufficiently flexible to avoid creating unnecessary role duplication.

Detailed platform roles and permission boundaries are defined separately.

---

## Authorization Should Consider Resource Boundaries

Access decisions should not depend only on who the user is.

They may also depend on what resource is being accessed.

For example:

```text
Authenticated User
        |
        | Request
        v
Resource
        |
        +--> Learning Module
        |
        +--> Assessment
        |
        +--> Learner Progress Record
        |
        +--> Project Submission
```

A user may have permission to access one resource but not another.

Examples include:

- A learner can view their own progress but not another learner's progress.
- A contributor can edit assigned content but not all platform content.
- A reviewer can review content assigned to their review responsibility.
- An administrator may have broader management access.

Authorization should therefore eventually support the relationship between identity, action, and resource.

---

## Access Control Should Respect Domain Ownership

Authorization should align with platform domain and module boundaries.

For example:

```text
Identity
    |
    v
Authentication
    |
    v
Authorization Decision
    |
    +----------------------+
    |                      |
    v                      v
Content Domain        Assessment Domain
```

Each domain remains responsible for protecting access to the resources it owns.

A centralized authorization mechanism may provide common identity and permission information.

However, domain boundaries should still be respected when determining access to domain-specific resources.

This prevents unrelated modules from becoming uncontrolled authorities over resources they do not own.

---

## Human and System Identities Should Be Distinguished

The platform may eventually need to support both human users and system-to-system interactions.

Conceptually:

```text
Identity
   |
   +----------------------+
   |                      |
   v                      v
Human Identity       System Identity
   |                      |
   v                      v
Learner              External Service
Contributor          Integration
Reviewer             Automated Process
Administrator        Background Job
```

A system identity should not automatically receive the same permissions as a human administrator.

System access should be explicitly scoped according to the capability being performed.

This supports better security boundaries and clearer operational accountability.

---

## Credentials and Secrets Should Be Managed Securely

Authentication mechanisms may require credentials, secrets, tokens, certificates, or other sensitive information.

These should not be treated as ordinary application configuration.

The platform should eventually establish controls for:

- Secure storage.
- Restricted access.
- Rotation.
- Expiration.
- Revocation.
- Auditability.
- Separation between environments.

Conceptually:

```text
Application
     |
     | Requests Authorized Credential
     v
+-------------------------+
| Secure Secret Boundary  |
+------------+------------+
             |
             v
      Authentication
```

Sensitive credentials should not be unnecessarily embedded in source code, documentation, repositories, or publicly accessible configuration.

The specific secret-management technology should be selected during implementation.

---

## Authentication and Authorization Failures Should Be Explicit

The platform should clearly distinguish between different types of security failures.

For example:

```text
Request
   |
   v
Authentication Successful?
   |
   +---- No ----> Authentication Failure
   |
   +---- Yes
          |
          v
   Authorization Allowed?
          |
          +---- No ----> Access Denied
          |
          +---- Yes
                 |
                 v
             Continue
```

An authentication failure indicates that identity could not be successfully established.

An authorization failure indicates that the identity is known but does not have the required access.

Keeping these failure types distinct improves:

- Security diagnostics.
- Operational monitoring.
- User experience.
- Incident investigation.
- Access troubleshooting.

---

## Access Should Be Revocable

Authorization should not assume that granted access is permanent.

The platform should support the ability to change or revoke access when appropriate.

Examples may include:

- A user changes responsibilities.
- A contributor no longer manages specific content.
- A system integration is retired.
- A credential is compromised.
- An account is disabled.
- A role assignment changes.

Conceptually:

```text
Identity
    |
    v
Current Access Policy
    |
    +--> Permission Granted
    |
    +--> Permission Changed
    |
    +--> Permission Revoked
```

Access decisions should reflect the current authorization state rather than relying indefinitely on historical assignments.

---

## Authentication and Authorization Events Should Be Observable

Security-relevant events should provide appropriate operational visibility.

Examples may include:

- Successful authentication.
- Failed authentication.
- Access denied.
- Permission changes.
- Role changes.
- Credential revocation.
- Suspicious repeated failures.

Conceptually:

```text
Authentication / Authorization Event
                 |
                 v
+--------------------------------+
| Security and Operational       |
| Visibility                     |
+--------------------------------+
                 |
                 +--> Monitoring
                 |
                 +--> Diagnostics
                 |
                 +--> Audit where required
```

The level of logging and monitoring should be appropriate to the platform's security, privacy, and operational requirements.

Sensitive information such as passwords, secrets, or authentication tokens should not be unnecessarily recorded in logs.

---

## Integration Security

External systems may need to interact with the Salesforce Learning Platform.

These interactions should establish:

- The identity of the calling system.
- The permissions assigned to that system.
- The scope of accessible resources.
- The allowed operations.
- Credential lifecycle requirements.

Conceptually:

```text
External System
       |
       | Authenticate
       v
+-----------------------+
| Platform Identity     |
| Boundary              |
+-----------+-----------+
            |
            v
+-----------------------+
| Authorization         |
| Policy                |
+-----------+-----------+
            |
            v
Allowed Platform Action
```

System integrations should receive only the access required for their intended purpose.

Broad administrative access should not be used as a default integration strategy.

---

## Environment Separation

Authentication and authorization configuration should consider separation between environments.

For example:

```text
Development
     |
     +--> Development Identities
     |
     +--> Development Credentials

Testing
     |
     +--> Testing Identities
     |
     +--> Testing Credentials

Production
     |
     +--> Production Identities
     |
     +--> Production Credentials
```

Development or testing credentials should not automatically be reused in production.

Environment-specific security configuration should be managed deliberately as the platform implementation evolves.

---

## Authentication and Authorization Decision Model

Before introducing a new platform capability, the following questions should be considered:

1. Who or what needs to access this capability?
2. Is the caller a human user or another system?
3. How will the caller's identity be authenticated?
4. What resources does the caller need to access?
5. What specific actions are required?
6. Can access be limited according to least privilege?
7. Which domain owns the protected resource?
8. Are roles, permissions, or additional resource rules required?
9. How can access be changed or revoked?
10. How will authentication and authorization failures be observed?
11. What sensitive credentials or secrets are involved?
12. How should access differ between environments?

These questions should be considered before implementing authentication or authorization controls for a new capability.

---

## Relationship to Other Platform Architecture Principles

Authentication and authorization principles work together with other platform architecture areas.

```text
Platform Architecture
        |
        +--> Identity and Authentication
        |
        +--> Authorization and Access Control
        |
        +--> Platform Roles and Permissions
        |
        +--> Data Ownership
        |
        +--> Integration Principles
        |
        +--> API and Service Interaction
        |
        +--> Observability and Operations
```

These areas should remain conceptually aligned.

For example:

- Identity establishes who is interacting with the platform.
- Authorization determines permitted actions.
- Roles and permissions organize access responsibilities.
- Data ownership identifies which domain owns protected information.
- Integration principles govern system-to-system interactions.
- API principles define how access boundaries are exposed.
- Observability provides operational visibility into access-related events.

---

## Future Evolution

As the Salesforce Learning Platform evolves, authentication and authorization capabilities may later include:

- Single sign-on.
- Federated identity.
- Multi-factor authentication.
- OAuth-based authorization.
- Role-based access control.
- Attribute-based access control.
- Fine-grained resource permissions.
- Service identities.
- Automated credential rotation.
- Centralized policy management.
- Security auditing.
- Session management.
- Conditional access policies.

These capabilities are not mandated at the current stage.

Specific technology and implementation decisions should be based on platform requirements, user needs, integration requirements, risk level, and the selected technical architecture.

---

## Key Architectural Principle

The primary principle established by this document is:

> Every platform interaction should establish a trusted identity before access is evaluated, and access should be granted only according to explicit permissions appropriate to the requested action and resource.

This principle supports stronger security boundaries, clearer responsibilities, controlled integrations, and the long-term evolution of the Salesforce Learning Platform.

---

## References

The following resources provide broader guidance related to authentication, authorization, identity management, access control, and application security:

- OWASP — Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

- OWASP — Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

- OWASP — Credential Stuffing Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html

- NIST — Digital Identity Guidelines: https://pages.nist.gov/800-63-3/

- OAuth 2.0 Authorization Framework: https://datatracker.ietf.org/doc/html/rfc6749

- OpenID Connect: https://openid.net/developers/how-connect-works/

- Microsoft Azure Architecture Center — Identity Management: https://learn.microsoft.com/en-us/azure/architecture/framework/security/design-identity

- AWS Security Reference Architecture: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/

- Salesforce Architecture Center: https://architect.salesforce.com/