# Platform Roles and Permission Model

## Purpose

This document defines the conceptual role and permission model for the Salesforce Learning Platform.

As the platform evolves, different users will interact with the platform for different purposes. A learner consumes learning content and tracks progress. A contributor may create or update learning material. A reviewer evaluates content before publication. A platform administrator manages broader operational responsibilities.

These users should not automatically receive the same level of access.

The platform therefore requires a clear model for defining:

- User responsibilities.
- Platform roles.
- Permissions.
- Access boundaries.
- Relationships between roles and permissions.
- Resource-level access where required.

This document establishes a conceptual model only.

It does not prescribe a specific implementation technology, Salesforce permission configuration, database schema, identity provider, or authorization framework.

---

## Core Principle

The primary principle of the platform role and permission model is:

> Roles represent responsibilities. Permissions represent specific actions. Access should be granted according to the minimum level required to perform an intended responsibility.

This model separates broad responsibilities from individual access rights.

Conceptually:

```text
User
  |
  v
Assigned Role
  |
  v
Associated Permissions
  |
  v
Allowed Actions
  |
  v
Protected Resources
```

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

The role represents the responsibility.

The permissions define the actions associated with that responsibility.

---

## Why Roles and Permissions Are Needed

A learning platform contains different types of resources and actions.

Examples include:

- Viewing learning content.
- Creating learning modules.
- Editing content.
- Reviewing submitted material.
- Publishing approved content.
- Completing assessments.
- Viewing learner progress.
- Managing platform configuration.
- Assigning access.

If every user received unrestricted access, the platform would create unnecessary security and operational risks.

A structured role and permission model helps establish:

- Clear responsibilities.
- Controlled access.
- Separation of duties.
- Reduced accidental changes.
- Better protection of learner information.
- More predictable system behaviour.
- Easier future administration.

The objective is not to create a large number of roles.

The objective is to create understandable access boundaries that can evolve as the platform becomes more complex.

---

## Conceptual Platform Roles

The initial platform model recognizes several broad categories of responsibility.

```text
Platform Users
      |
      +-----------------------------+
      |                             |
      v                             v
Learning Users                 Platform Contributors
      |                             |
      |                             |
      v                             v
Learner                    Content Author
                           Content Reviewer
                           Content Publisher
                           Administrator
```

These roles represent conceptual responsibilities.

A single person may eventually hold more than one role.

For example:

```text
User
  |
  +--> Learner
  |
  +--> Content Author
```

The implementation should not assume that one user must always belong to exactly one role.

---

## Learner Role

The Learner role represents a user who interacts with the platform primarily to consume learning resources and complete learning activities.

Typical responsibilities may include:

- Accessing published learning content.
- Following learning paths.
- Completing exercises.
- Completing assessments.
- Submitting projects.
- Viewing personal learning progress.
- Viewing permitted assessment results.

Conceptually:

```text
Learner
   |
   +--> View Published Content
   |
   +--> Follow Learning Paths
   |
   +--> Complete Assessments
   |
   +--> Submit Projects
   |
   +--> View Own Progress
```

A learner should not automatically receive permissions to modify platform content, manage other learners, approve content, or administer platform configuration.

---

## Content Author Role

The Content Author role represents a contributor responsible for creating or maintaining learning content.

Typical permissions may include:

- Create new learning content.
- Edit permitted content.
- Update content metadata.
- Add examples and supporting resources.
- Create or update exercises.
- Submit content for review.

Conceptually:

```text
Content Author
       |
       +--> Create Content
       |
       +--> Edit Authorized Content
       |
       +--> Manage Content Metadata
       |
       +--> Submit for Review
```

Content authors should not automatically be able to approve their own work unless the platform explicitly defines such a process.

This separation supports independent review and clearer content governance.

---

## Content Reviewer Role

The Content Reviewer role represents responsibility for evaluating learning content against established quality and review standards.

Typical permissions may include:

- View content submitted for review.
- Review technical and structural quality.
- Request changes.
- Approve content where authorized.
- Add review feedback.

Conceptually:

```text
Content Reviewer
       |
       +--> View Submitted Content
       |
       +--> Evaluate Content
       |
       +--> Request Changes
       |
       +--> Approve Content
```

The reviewer role should focus on review responsibilities.

It should not automatically include unrestricted administrative access.

---

## Content Publisher Role

The Content Publisher role represents responsibility for making approved learning resources available through the active learning experience.

Typical permissions may include:

- Publish approved content.
- Remove or restrict published content where authorized.
- Manage publication state.
- Coordinate content availability.
- Maintain publication relationships with learning paths.

Conceptually:

```text
Content Publisher
       |
       +--> Publish Approved Content
       |
       +--> Update Publication State
       |
       +--> Restrict Content Availability
       |
       +--> Archive Content
```

In an early implementation, publishing responsibilities may be combined with another contributor role.

The conceptual separation remains useful because reviewing content and making content publicly available are different responsibilities.

---

## Platform Administrator Role

The Platform Administrator role represents broader operational and administrative responsibilities.

Typical permissions may include:

- Manage platform configuration.
- Manage user access.
- Assign roles.
- Manage permissions.
- Configure supported platform capabilities.
- Access operational administration functions.

Conceptually:

```text
Platform Administrator
       |
       +--> Manage Platform Configuration
       |
       +--> Manage Access
       |
       +--> Assign Roles
       |
       +--> Manage Operational Settings
```

Administrative access should be granted carefully.

The administrator role should not be treated as the default role for users who simply require additional access.

Broad administrative permissions should only be assigned when required.

---

## System or Service Role

The platform may eventually include automated processes, integrations, background jobs, or external services.

These should be treated as system identities rather than human users.

Conceptually:

```text
Platform Identities
        |
        +-----------------------+
        |                       |
        v                       v
Human Identity             System Identity
        |                       |
        v                       v
Learner                  Integration
Author                   Background Process
Reviewer                 Automated Service
Administrator
```

A system identity should receive only the permissions required for its specific function.

For example:

```text
Progress Processing Service
        |
        +--> Read Required Learning Activity
        |
        +--> Update Learner Progress
```

The service should not automatically receive unrestricted administrative access.

---

## Role and Permission Relationship

Roles provide an understandable grouping mechanism.

Permissions represent individual actions.

Conceptually:

```text
                 +-------------------+
                 |       Role        |
                 +-------------------+
                           |
              +------------+------------+
              |            |            |
              v            v            v
         Permission    Permission   Permission
              |            |            |
              v            v            v
          Action A      Action B     Action C
```

For example:

```text
Role: Content Reviewer

Permissions:

- View Submitted Content
- Add Review Feedback
- Request Changes
- Approve Content
```

This separation allows permissions to remain specific while roles represent broader responsibilities.

---

## Permission Model

Permissions should describe explicit actions.

A conceptual permission may be expressed as:

```text
RESOURCE + ACTION
```

Examples:

```text
Content.Read
Content.Create
Content.Update
Content.SubmitForReview
Content.Review
Content.Approve
Content.Publish

LearningPath.Read
LearningPath.Create
LearningPath.Update

Assessment.Read
Assessment.Attempt
Assessment.Create
Assessment.Update

LearnerProgress.ReadOwn
LearnerProgress.Update

PlatformConfiguration.Manage
UserAccess.Manage
```

These examples are conceptual names only.

They do not define a required implementation format.

The purpose is to demonstrate that permissions should describe a specific capability rather than providing vague or unrestricted access.

---

## Resource-Based Access

Role membership alone may not always be sufficient to determine access.

Some actions may depend on the specific resource involved.

For example:

```text
Content Author
       |
       | Requests Edit
       v
Learning Module
       |
       +--> Assigned to Author? ---- Yes ---> Allow
       |
       +--> Assigned to Author? ---- No ----> Deny or Require Additional Permission
```

Another example:

```text
Learner
   |
   | Requests Progress
   v
Learner Progress Record
   |
   +--> Own Record? ---- Yes ---> Allow
   |
   +--> Other User? ---- No ----> Deny
```

This approach supports more precise access control where required.

---

## Separation of Duties

Some responsibilities should remain separate to reduce the risk of uncontrolled changes.

For example:

```text
Content Author
      |
      v
Creates Content
      |
      v
Content Reviewer
      |
      v
Reviews Content
      |
      v
Content Publisher
      |
      v
Makes Content Available
```

A future implementation may allow one person to perform multiple responsibilities depending on the size and maturity of the platform.

However, the conceptual distinction should remain visible.

Where risk or governance requirements increase, separation of duties can provide stronger control.

---

## Principle of Least Privilege

Permissions should follow the principle of least privilege.

This means:

> Users and systems should receive only the level of access required to perform their intended responsibilities.

Conceptually:

```text
Required Responsibility
          |
          v
Required Actions
          |
          v
Minimum Necessary Permissions
          |
          v
Granted Access
```

For example, a reviewer may need permission to approve content.

The reviewer does not automatically need permission to:

- Manage platform configuration.
- Assign administrator roles.
- Modify learner identity information.
- Access unrelated operational settings.

Least privilege reduces unnecessary exposure and limits the potential impact of accidental or unauthorized actions.

---

## Permission Inheritance and Composition

As the platform grows, permissions may eventually be grouped or composed through roles.

Conceptually:

```text
Role
 |
 +--> Permission A
 |
 +--> Permission B
 |
 +--> Permission C
```

A user may also eventually receive multiple roles.

For example:

```text
User
 |
 +--> Learner
 |
 +--> Content Author
```

The user's effective permissions may therefore be derived from the combination of assigned responsibilities.

The exact rules for combining permissions should be defined when the authorization implementation is designed.

At the conceptual level, the platform should avoid relying on assumptions that a user can perform only one type of responsibility.

---

## Role Assignment

Role assignment should be deliberate and controlled.

The platform should eventually establish:

- Who can assign roles.
- Who can remove roles.
- How role changes are approved where necessary.
- How changes are recorded.
- How access is revoked.

Conceptually:

```text
Administrator
      |
      v
Assign Role
      |
      v
User
      |
      v
Effective Permissions Updated
```

Role assignment should not be treated as a permanent condition.

Access should be reviewed and changed when responsibilities change.

---

## Permission Revocation

Permissions and roles should be removable when access is no longer required.

Examples include:

- A contributor changes responsibilities.
- A reviewer is no longer assigned to content review.
- An administrator leaves an operational role.
- A system integration is retired.
- A service credential is replaced.

Conceptually:

```text
Current Access
      |
      v
Responsibility Changes
      |
      v
Role or Permission Review
      |
      +--> Retain
      |
      +--> Modify
      |
      +--> Revoke
```

The platform should eventually ensure that revoked access is reflected in future authorization decisions.

---

## Role and Permission Decision Model

When introducing a new platform capability, the following questions should be considered:

1. Who needs to perform this action?
2. Is the actor a learner, contributor, administrator, or system?
3. What specific action needs to be permitted?
4. Which resource is being accessed?
5. Does the actor require access to all resources or only specific resources?
6. Can the action be represented as an existing permission?
7. Does a new role need to be introduced?
8. Can the responsibility be assigned to an existing role?
9. Does granting this permission violate least privilege?
10. Should the action require separation from another responsibility?
11. How can the permission be revoked?
12. How will access decisions be monitored or audited where required?

These questions should be considered before creating new roles or broad permissions.

---

## Relationship to Authentication and Authorization

The role and permission model operates within the broader authentication and authorization architecture.

Conceptually:

```text
User or System
       |
       v
Authentication
       |
       v
Verified Identity
       |
       v
Assigned Roles
       |
       v
Associated Permissions
       |
       v
Authorization Decision
       |
       v
Protected Resource
```

Authentication verifies identity.

Roles represent responsibilities.

Permissions represent allowed actions.

Authorization evaluates whether the identity has sufficient permission to perform the requested action on the requested resource.

These concepts should remain distinct even when implemented using a common technology platform.

---

## Relationship to Platform Architecture

The role and permission model supports multiple architectural areas.

```text
Platform Architecture
        |
        +--> Authentication
        |
        +--> Authorization
        |
        +--> Roles and Permissions
        |
        +--> Domain Ownership
        |
        +--> Data Access
        |
        +--> API Security
        |
        +--> Operational Administration
```

The permission model should remain aligned with:

- Domain boundaries.
- Data ownership.
- Integration principles.
- API and service interaction principles.
- Security requirements.
- Operational responsibilities.

Permissions should not be created independently without understanding which domain owns the protected resource and why access is required.

---

## Initial Conceptual Role Matrix

The following table provides an initial conceptual model.

| Capability | Learner | Content Author | Content Reviewer | Content Publisher | Platform Administrator | System Identity |
|---|---|---|---|---|---|---|
| View published content | Yes | Yes | Yes | Yes | Yes | As required |
| Create content | No | Yes | As required | As required | As required | No |
| Edit authorized content | No | Yes | As required | As required | As required | As required |
| Submit content for review | No | Yes | No | As required | As required | No |
| Review content | No | No | Yes | As required | As required | No |
| Approve content | No | No | Yes | As required | As required | No |
| Publish content | No | No | No | Yes | As required | No |
| Complete assessments | Yes | As required | As required | As required | As required | No |
| View own progress | Yes | Yes | Yes | Yes | Yes | As required |
| Manage roles and permissions | No | No | No | No | Yes | No |
| Manage platform configuration | No | No | No | No | Yes | As required |

This matrix is conceptual.

The final permission model may evolve as actual platform requirements, workflows, and implementation decisions become more detailed.

---

## Future Evolution

As the Salesforce Learning Platform grows, the role and permission model may later support:

- Role-based access control.
- Attribute-based access control.
- Resource-level permissions.
- Permission groups.
- Delegated administration.
- Temporary access.
- Approval workflows for privileged access.
- Automated access reviews.
- Audit history.
- Fine-grained API permissions.
- Context-aware authorization.
- Policy-based access control.

These capabilities are not required at the current stage.

The purpose of this document is to establish a clear conceptual model that can guide future implementation decisions.

---

## Key Architectural Principle

The primary principle established by this document is:

> Platform access should be based on clearly defined responsibilities and explicit permissions, with each identity receiving only the access required to perform its intended role.

This approach supports security, maintainability, separation of responsibilities, controlled administration, and the long-term evolution of the Salesforce Learning Platform.

---

## References

The following resources provide broader guidance related to role-based access control, authorization, least privilege, and access management:

- OWASP — Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

- OWASP — Authorization Testing Automation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet.html

- NIST — Role Based Access Control: https://csrc.nist.gov/projects/role-based-access-control

- NIST — Guide to Attribute Based Access Control: https://csrc.nist.gov/projects/attribute-based-access-control

- NIST — Security and Privacy Controls for Information Systems and Organizations: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

- Microsoft Azure Architecture Center — Authorization: https://learn.microsoft.com/en-us/azure/architecture/framework/security/design-identity

- AWS IAM Best Practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

- Salesforce Architecture Center: https://architect.salesforce.com/