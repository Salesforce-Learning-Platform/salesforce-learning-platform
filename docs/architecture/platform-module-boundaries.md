# Platform Module Boundaries

## Purpose

This document defines the major conceptual modules of the Salesforce Learning Platform, their primary responsibilities, and the boundaries that should exist between them.

As a platform grows, responsibilities can easily become mixed across different areas of the system. For example, learning content management should not become responsible for authentication, and learner progress tracking should not determine whether content is approved for publication.

Clear module boundaries help the platform remain understandable, maintainable, and easier to evolve.

This document establishes conceptual boundaries for the platform. It does not prescribe a specific technology stack, microservices architecture, database design, API implementation, or deployment model.

The modules described here may initially exist within a single application. If justified by future scale, ownership, operational, or technical requirements, some capabilities may later evolve into more independently managed components.

---

## Module Boundary Principles

A platform module represents a coherent area of responsibility.

Each module should have a clear understanding of:

- What it is responsible for.
- What information or capabilities it owns.
- What responsibilities belong elsewhere.
- How other modules should interact with it.

The purpose of module boundaries is not to divide the platform into the maximum possible number of components.

Unnecessary decomposition can create:

- Increased technical complexity.
- Difficult dependency management.
- Duplicate responsibilities.
- Excessive communication between components.
- Higher operational overhead.
- Reduced clarity for contributors.

A boundary should therefore exist where separating responsibilities provides meaningful architectural value.

Module boundaries should support:

- Separation of concerns.
- Clear ownership.
- Reduced coupling.
- Maintainability.
- Independent evolution where necessary.
- Better change isolation.
- Clearer security boundaries.
- Improved understanding for contributors.

---

## High-Level Platform Module Model

The Salesforce Learning Platform can be understood through the following conceptual modules:

    +-----------------------------------------------------------+
    |                 SALESFORCE LEARNING PLATFORM               |
    +-----------------------------------------------------------+

                               |
                               v

    +-------------------+      +-------------------+
    | Identity & Access |      | Learning Content  |
    +-------------------+      +-------------------+
              |                        |
              |                        |
              +-----------+------------+
                          |
                          v

    +-----------------------------------------------------------+
    |                   Learning Experience                     |
    |                                                           |
    | Learning Paths | Discovery | Navigation | Content Access  |
    +-----------------------------------------------------------+
                          |
              +-----------+------------+
              |                        |
              v                        v

    +-------------------+      +-------------------+
    | Assessment &      |      | Learner Progress  |
    | Knowledge         |      |                   |
    | Validation        |      |                   |
    +-------------------+      +-------------------+
              |                        |
              +-----------+------------+
                          |
                          v

    +-----------------------------------------------------------+
    |              Projects & Practical Learning                |
    +-----------------------------------------------------------+
                          |
                          v

    +-----------------------------------------------------------+
    |            Platform Governance & Operations               |
    |                                                           |
    | Quality | Lifecycle | Versioning | Maintenance            |
    | Observability | Operational Management                    |
    +-----------------------------------------------------------+
                          |
                          v

    +-----------------------------------------------------------+
    |             Integration & External Services               |
    +-----------------------------------------------------------+

This model represents conceptual relationships.

The modules are not required to correspond directly to separate applications, services, repositories, databases, or deployment units.

---

# Core Platform Modules

## 1. Identity and Access

### Responsibility

The Identity and Access module is responsible for establishing who a user is and determining what that user is allowed to do within the platform.

Its responsibilities may include:

- User identity.
- Authentication.
- Authorization.
- Role assignment.
- Permission evaluation.
- Access control.
- Identity-related security boundaries.

Typical questions handled by this module include:

- Who is the current user?
- Has the user been successfully authenticated?
- What role does the user have?
- Is the user permitted to perform a specific action?
- Can the user access a particular platform capability?

### Boundary

The Identity and Access module determines identity and access.

It should not own learning-specific business responsibilities such as:

- Tracking learner progress.
- Calculating assessment scores.
- Managing learning content.
- Determining content lifecycle status.
- Defining learning paths.

Identity and Access is responsible for:

- Identity.
- Authentication.
- Authorization.
- Roles.
- Permissions.

Identity and Access is not responsible for:

- Learning progress.
- Assessment results.
- Content authoring.
- Content publication.
- Learning path structure.

Other modules may rely on Identity and Access to determine whether an action is permitted, but they should not duplicate the core authorization model.

---

## 2. Learning Content

### Responsibility

The Learning Content module is responsible for the learning resources available within the platform.

This includes the conceptual management of:

- Learning modules.
- Topics.
- Lessons.
- Documentation.
- Exercises.
- Supporting resources.
- Content metadata.
- Content relationships.
- Content lifecycle.
- Content versioning.

The primary responsibility of this module is to define and manage what learners can learn.

### Boundary

The Learning Content module should not be responsible for:

- Tracking whether a learner completed content.
- Determining whether a learner passed an assessment.
- Authenticating users.
- Managing platform-wide permissions.
- Rendering the user interface.
- Managing external integrations unrelated to content.

Learning Content is responsible for:

- Content structure.
- Learning resources.
- Metadata.
- Content relationships.
- Lifecycle.
- Versioning.

Learning Content is not responsible for:

- Learner authentication.
- Progress tracking.
- Assessment scoring.
- UI implementation.
- External identity management.

The Content module provides information about learning resources. Other modules determine how those resources are accessed, presented, assessed, or tracked.

---

## 3. Learning Experience

### Responsibility

The Learning Experience module is responsible for how learning resources are organized and experienced by learners.

This may include:

- Learning path navigation.
- Content discovery.
- Learning resource sequencing.
- Navigation between related resources.
- Learner-facing content access.
- Conceptual user journeys.

The Learning Experience module acts as a bridge between available learning content and the learner's journey through that content.

### Boundary

This module should not become the owner of the learning content itself.

For example, a learning path may reference several learning resources, but the learning path should not duplicate ownership of the underlying content.

Similarly, the Learning Experience module should not independently calculate assessment results or own the identity system.

Learning Experience is responsible for:

- Learner journeys.
- Learning path organization.
- Discovery.
- Navigation.
- Content access experience.

Learning Experience is not responsible for:

- Content source ownership.
- Authentication.
- Assessment scoring.
- Core authorization logic.

---

## 4. Assessment and Knowledge Validation

### Responsibility

The Assessment and Knowledge Validation module is responsible for evaluating learner understanding.

This may include:

- Questions.
- Assessment structures.
- Knowledge validation.
- Evaluation criteria.
- Assessment attempts.
- Scoring concepts.
- Completion criteria related to assessments.

The purpose of this module is to answer questions such as:

- Has the learner demonstrated understanding?
- What knowledge or capability is being evaluated?
- What criteria determine successful completion?
- What result should be associated with an assessment attempt?

### Boundary

This module should not own:

- The learner's identity.
- The complete learning content lifecycle.
- Platform authorization.
- General learner progress across all resources.

Assessment results may contribute to learner progress, but assessment evaluation and progress tracking represent separate responsibilities.

Assessment is responsible for:

- Knowledge validation.
- Assessment structure.
- Evaluation criteria.
- Assessment results.

Assessment is not responsible for:

- Authentication.
- General progress ownership.
- Content lifecycle.
- Platform roles.

---

## 5. Learner Progress

### Responsibility

The Learner Progress module is responsible for tracking a learner's relationship with learning resources over time.

This may include:

- Started content.
- Completed content.
- Learning milestones.
- Progress through learning paths.
- Completion state.
- Progress indicators.
- Learning activity history where appropriate.

The central responsibility is to answer:

- What has the learner started?
- What has the learner completed?
- Where is the learner within a learning journey?
- What learning milestones have been achieved?

### Boundary

Learner Progress should not determine:

- Whether learning content is technically correct.
- Whether content should be published.
- Whether a user is authenticated.
- How an assessment is evaluated internally.

Instead, it may consume relevant information from other modules.

For example:

    Assessment Module
            |
            | Assessment result
            v
    Learner Progress Module
            |
            | Updated progress state
            v
    Learning Experience

The Assessment module owns assessment evaluation.

The Learner Progress module owns the learner's progress state resulting from learning activity.

---

## 6. Projects and Practical Learning

### Responsibility

The Projects and Practical Learning module is responsible for practical, project-based learning experiences.

This may include:

- Project definitions.
- Practical assignments.
- Project requirements.
- Expected outcomes.
- Project milestones.
- Submission concepts.
- Validation criteria.

This module supports the principle that technical learning should extend beyond passive content consumption.

A learner may study a topic, complete exercises, and then apply that knowledge through a practical project.

### Boundary

The Projects and Practical Learning module should not own:

- Core authentication.
- General content lifecycle rules.
- Platform-wide authorization.
- All learner progress logic.
- General assessment infrastructure.

Projects may interact with assessment and learner progress capabilities, but the responsibilities remain distinct.

---

## 7. Platform Governance and Content Operations

### Responsibility

The Platform Governance and Content Operations area is responsible for maintaining the quality, consistency, and long-term health of platform content and related operational processes.

This conceptual area includes:

- Content quality assurance.
- Content review.
- Lifecycle management.
- Versioning.
- Content maintenance.
- Content archival.
- Operational governance.

This area answers questions such as:

- Is the content ready for publication?
- Does the content meet platform standards?
- Does the content require maintenance?
- Which version is current?
- Should the content remain active or be archived?

### Boundary

Governance and operations should establish rules and processes without taking ownership of unrelated platform capabilities.

For example, the governance process may determine that content requires review, but it does not determine whether a learner has completed that content.

Platform Governance is responsible for:

- Quality standards.
- Review processes.
- Lifecycle management.
- Versioning.
- Maintenance principles.

Platform Governance is not responsible for:

- Learner authentication.
- Learner progress ownership.
- Assessment evaluation.
- User interface rendering.

---

## 8. Integration and External Services

### Responsibility

The Integration and External Services module represents the boundary between the Salesforce Learning Platform and external systems.

External systems may eventually include:

- Identity providers.
- Salesforce services.
- Analytics platforms.
- Notification services.
- Content delivery systems.
- Third-party APIs.
- Learning or productivity tools.

This module should define how external capabilities interact with the platform while protecting the internal domain model from unnecessary dependency on external implementation details.

### Boundary

External systems should not directly define or control the platform's internal business model without an explicit architectural decision.

A useful conceptual pattern is:

    External System
          |
          v
    Integration Boundary
          |
          v
    Platform Capability

The integration boundary acts as a controlled point of interaction.

This reduces the risk of external implementation details spreading throughout the platform.

---

# Module Interaction Principles

Modules will need to interact with one another.

However, interaction should not mean unrestricted access to internal responsibilities.

A module should communicate through clearly understood contracts, capabilities, or interfaces.

The general principle is:

    Module A
       |
       | Request or Event
       v
    Defined Interaction Boundary
       |
       v
    Module B

A module should avoid directly depending on the internal implementation details of another module.

For example, Learner Progress may need to know that an assessment was successfully completed.

It does not need to understand every internal calculation used by the Assessment module.

This distinction helps reduce coupling.

---

# Dependency Direction

Dependencies should generally move toward stable, well-defined responsibilities.

A higher-level learner experience should be able to use content capabilities without becoming responsible for how those capabilities are internally implemented.

For example:

    Learning Experience
            |
            v
    Learning Content

    Learning Experience
            |
            v
    Learner Progress

    Learner Progress
            |
            v
    Assessment Results

This does not require a strict layered architecture in every implementation.

Instead, it establishes the principle that modules should depend on capabilities and contracts rather than internal implementation details.

---

# Avoiding Boundary Violations

A boundary violation occurs when one module begins taking responsibility for another module's core concerns.

## Example 1: Content Owning Learner Progress

Incorrect approach:

    Learning Content
        |
        +-- Stores learner completion
        +-- Calculates learner progress
        +-- Determines learning milestones

Preferred approach:

    Learning Content
        |
        | Provides learning resource
        v
    Learner Progress
        |
        | Tracks learner relationship
        v
    Progress State

---

## Example 2: Assessment Owning Authorization

Incorrect approach:

    Assessment Module
        |
        +-- Defines user roles
        +-- Manages permissions

Preferred approach:

    Assessment Module
            |
            | Requests access decision
            v
    Identity & Access

---

## Example 3: User Interface Owning Business Rules

Incorrect approach:

    User Interface
        |
        +-- Determines publication rules
        +-- Calculates assessment logic
        +-- Defines lifecycle transitions

Preferred approach:

    User Interface
            |
            v
    Platform Capabilities
            |
            v
    Business Rules

User interface components may enforce presentation behavior, but core platform rules should not exist only within the interface.

---

# Module Ownership

Every major platform capability should have a clearly understood conceptual owner.

Ownership does not necessarily mean one individual or one team.

It means that the platform should be able to identify which module is responsible for a particular concern.

| Platform Concern | Conceptual Owner |
|---|---|
| User authentication | Identity and Access |
| Learning resource structure | Learning Content |
| Learning path navigation | Learning Experience |
| Assessment evaluation | Assessment and Knowledge Validation |
| Learner completion state | Learner Progress |
| Practical projects | Projects and Practical Learning |
| Content review | Platform Governance |
| External system communication | Integration and External Services |

Clear ownership reduces duplication and conflicting responsibilities.

---

# Future Evolution

The module boundaries defined in this document are conceptual and may evolve as the Salesforce Learning Platform grows.

Future architectural decisions may introduce:

- More detailed domain boundaries.
- Formal bounded contexts.
- API contracts.
- Event-driven communication.
- Service boundaries.
- Dedicated ownership models.
- Data ownership boundaries.
- Independent deployment strategies.

However, these decisions should be based on demonstrated architectural requirements rather than assumptions.

A small platform does not automatically require microservices.

A conceptual module does not automatically require a separate repository, application, database, or deployment pipeline.

The platform should preserve clear responsibilities first and introduce additional technical separation only when there is sufficient justification.

---

## Summary

The Salesforce Learning Platform is organized around major conceptual responsibilities rather than arbitrary technical divisions.

The primary module boundaries are:

1. Identity and Access.
2. Learning Content.
3. Learning Experience.
4. Assessment and Knowledge Validation.
5. Learner Progress.
6. Projects and Practical Learning.
7. Platform Governance and Content Operations.
8. Integration and External Services.

These boundaries provide a foundation for future architectural decisions.

They help ensure that:

- Content remains separate from learner state.
- Assessment remains separate from general progress tracking.
- Authentication remains separate from learning business rules.
- Governance remains separate from content consumption.
- External systems interact through controlled boundaries.
- The platform can evolve without unnecessary coupling.

This document establishes the conceptual module structure that future architecture, data ownership, integration, API, and implementation decisions should build upon.

---

## References

### Domain-Driven Design

Eric Evans introduced Domain-Driven Design concepts that emphasize modeling complex software around meaningful domain boundaries and separating responsibilities through bounded contexts.

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*.
- https://www.domainlanguage.com/ddd/reference/

### Martin Fowler — Monolith First

Martin Fowler discusses the importance of understanding domain and architectural boundaries before introducing distributed systems or microservices.

- https://martinfowler.com/bliki/MonolithFirst.html

### Martin Fowler — Bounded Context

The bounded context concept describes how a domain model should have a clearly defined boundary and meaning within a specific context.

- https://martinfowler.com/bliki/BoundedContext.html

### Microsoft Architecture Center

Microsoft provides guidance on architectural styles, service boundaries, domain modeling, separation of concerns, and distributed system design.

- https://learn.microsoft.com/en-us/azure/architecture/

### AWS Prescriptive Guidance

AWS provides guidance on domain-driven design, microservice decomposition, service boundaries, and avoiding tightly coupled architectures.

- https://docs.aws.amazon.com/prescriptive-guidance/

### Salesforce Well-Architected

Salesforce provides architecture guidance focused on scalable, maintainable, secure, and well-governed solutions.

- https://architect.salesforce.com/