# Data Ownership and Source of Truth Principles

## Purpose

This document defines the principles for data ownership, responsibility, and authoritative sources of information within the Salesforce Learning Platform.

As the platform evolves, information may be created, updated, consumed, and referenced by multiple platform capabilities. Without clear ownership and an agreed source of truth, the same information can become duplicated, inconsistent, or difficult to maintain.

The purpose of these principles is to establish a conceptual model for answering three fundamental questions for every important category of data:

1. What does this data represent?
2. Who or what is responsible for maintaining it?
3. Which source is considered authoritative when multiple representations exist?

These principles are intentionally technology-neutral. They do not prescribe a specific database, Salesforce object model, API architecture, or storage implementation.

---

## Why Data Ownership Matters

A learning platform contains multiple categories of information that evolve independently.

Examples include:

- Learning content
- Learning paths
- Content metadata
- Learner profiles
- Learner progress
- Assessment results
- Projects and submissions
- User roles
- Permissions
- Platform configuration
- Operational events

As the platform grows, the same information may be required by multiple modules.

For example, a learning path may need to display information about multiple learning modules. An assessment capability may need to reference learner identity information. A learner progress capability may need to reference the current version of learning content.

The existence of multiple consumers does not mean that every consumer should maintain its own independent copy of the same data.

A clear ownership model reduces the risk of:

- Conflicting data
- Duplicate records
- Unclear update responsibilities
- Inconsistent learner experiences
- Incorrect reporting
- Difficult system integrations
- Uncontrolled dependencies between modules

The core principle is simple:

> Every important category of data should have a clearly understood authoritative source.

---

## Core Principles

### 1. Every Important Data Domain Should Have an Owner

Each significant category of data should have a clearly understood owner.

The owner is responsible for defining:

- The meaning of the data
- The rules governing its validity
- How it can be created or updated
- Who is allowed to change it
- How other parts of the platform should consume it

Ownership does not necessarily mean that one individual manually manages every record.

Ownership is a responsibility model.

For example, the Content domain may own the authoritative definition of a learning module. The Learner Progress domain may own the learner's progress state. The Assessment domain may own assessment attempts and results.

Other modules may consume this information, but they should not independently redefine what the data means.

---

### 2. One Authoritative Source Should Exist for Each Data Concept

A source of truth is the authoritative location, domain, or capability responsible for a specific data concept.

For example:

```text
Learning Content
        |
        v
Content Domain
Authoritative Source
        |
        +-----------------> Learning Paths
        |
        +-----------------> Assessments
        |
        +-----------------> Search
        |
        +-----------------> Learner Experience
```

Multiple modules may use learning content. However, the authoritative definition of that content should originate from one clearly defined domain.

This does not prevent other modules from storing derived, cached, indexed, or reporting-oriented representations when necessary.

The distinction is:

```text
Authoritative Data
        |
        +--> Defines the official state
        |
        +--> Is responsible for correctness
                |
                v
Derived or Replicated Data
        |
        +--> Supports performance
        +--> Supports reporting
        +--> Supports search
        +--> Supports specific use cases
```

Derived data should not silently become a competing source of truth.

---

### 3. Data Ownership Should Follow Domain Responsibility

Ownership should generally align with the domain that has the strongest business and conceptual responsibility for the data.

For example:

| Data Concept | Conceptual Owner |
|---|---|
| Learning content definition | Content Domain |
| Learning path structure | Learning Path Domain |
| Learner progress | Learner Progress Domain |
| Assessment attempts | Assessment Domain |
| Project submissions | Project-Based Learning Domain |
| User identity | Identity Domain |
| Roles and permissions | Authorization Domain |
| Platform configuration | Platform Administration Domain |

These are conceptual ownership boundaries.

They do not require the platform to be implemented as separate applications, microservices, or databases.

A single implementation may initially support multiple domains.

The important principle is that responsibility remains clear even if the technical implementation changes.

---

## Data Ownership Model

Data ownership can be understood through four levels of responsibility.

```text
+----------------------------------------------+
|                 DATA CONCEPT                 |
|                                              |
| Example: Learner Progress                    |
+----------------------------------------------+
                    |
                    v
+----------------------------------------------+
|                DOMAIN OWNER                  |
|                                              |
| Defines meaning and responsibility           |
+----------------------------------------------+
                    |
                    v
+----------------------------------------------+
|           AUTHORITATIVE SOURCE               |
|                                              |
| Maintains the official state                 |
+----------------------------------------------+
                    |
                    v
+----------------------------------------------+
|                 CONSUMERS                    |
|                                              |
| Read, reference, or derive information       |
+----------------------------------------------+
```

For every important data concept, the platform should eventually be able to identify:

- The domain responsible for the concept
- The authoritative source
- The systems or modules allowed to update it
- The consumers that depend on it
- The rules governing synchronization or replication

---

## Conceptual Data Ownership Boundaries

The following table provides an initial conceptual ownership model.

| Data Domain | Primary Responsibility | Example Data |
|---|---|---|
| Content | Define and maintain learning resources | Modules, lessons, exercises |
| Content Metadata | Describe and classify content | Difficulty, topics, prerequisites |
| Learning Paths | Organize structured learning journeys | Path sequence, milestones |
| Learner Progress | Track learner activity and completion | Completion status, progress state |
| Assessment | Validate learner understanding | Questions, attempts, scores |
| Project-Based Learning | Track practical learning work | Projects, submissions, evaluations |
| Identity | Establish who the user is | User identity and authentication attributes |
| Authorization | Define access boundaries | Roles, permissions, access policies |
| Platform Operations | Support platform administration | Configuration and operational settings |

This model may evolve as the platform becomes more detailed.

The purpose at this stage is not to define physical storage or implementation technology. The purpose is to establish clear conceptual responsibility.

---

## Source of Truth Principles

### Authoritative Data Should Be Updated Through Its Owning Domain

Where possible, changes to authoritative information should be performed through the domain responsible for that information.

For example:

```text
Learner Activity
      |
      v
Learner Progress Domain
      |
      v
Authoritative Progress State
      |
      +--> Learning Experience
      +--> Reporting
      +--> Recommendations
```

A reporting capability should not independently modify learner progress simply because it has access to the same information.

Similarly, a learning path should not redefine the authoritative completion state of a learning module.

This separation helps maintain consistency.

---

### Consumers Should Avoid Becoming Competing Sources of Truth

A consumer may need to store a local representation of information for performance, reporting, search, analytics, or operational reasons.

However, the consumer should understand whether its data is:

- Authoritative
- Derived
- Cached
- Replicated
- Historical
- Aggregated

For example:

```text
Content Domain
Authoritative Content
        |
        +----------------------+
        |                      |
        v                      v
Search Index             Analytics Dataset
Derived Data             Derived Data
```

The search index may contain a copy of content information, but it should not become the authoritative location for editing that content.

The analytics dataset may contain learner activity, but it should not become the system responsible for changing learner progress.

---

### Data Meaning Should Be Defined Consistently

A major source of data inconsistency is not always duplicate records. It can also result from the same term meaning different things in different modules.

For example, the term `Completed` could potentially mean:

- A learner opened all lessons
- A learner finished required content
- A learner passed an assessment
- A learner submitted a project
- A learning path reached its final milestone

The platform should avoid allowing each module to redefine important concepts independently without understanding the broader domain meaning.

Important concepts should have clearly understood definitions and ownership.

---

## Data Creation and Update Principles

The platform should distinguish between data ownership and data access.

A module may have permission to access information without having ownership of that information.

For example:

```text
Assessment Module
        |
        | Reads learner identity
        v
Identity Domain

Assessment Module
        |
        | Creates assessment attempt
        v
Assessment Domain
```

The Assessment domain may consume learner identity information but remain responsible for assessment attempts.

This distinction helps prevent uncontrolled cross-domain updates.

---

## Handling Shared Data

Some information may be required by many parts of the platform.

Shared usage does not automatically mean shared ownership.

For example, learner identity may be used by:

- Learning paths
- Assessments
- Projects
- Progress tracking
- Reporting
- Notifications

The Identity domain may still remain the authoritative owner.

A useful principle is:

> Many consumers can exist, but ownership should remain explicit.

---

## Data Replication and Synchronization

As the platform grows, some information may need to be copied or synchronized between systems.

Replication may be required for:

- Performance
- Search indexing
- Analytics
- Reporting
- Offline processing
- Integration with external systems

When replication occurs, the platform should identify:

1. The authoritative source.
2. The replicated destination.
3. The purpose of replication.
4. How updates are synchronized.
5. What happens when synchronization fails.
6. Whether the replicated data can be modified.

Conceptually:

```text
Authoritative Source
        |
        | Data Change
        v
Synchronization Process
        |
        +------------------+
        |                  |
        v                  v
Search Representation   Analytics Representation
Derived Data            Derived Data
```

The existence of replicated data should not create ambiguity about which source represents the official state.

---

## Data Conflict Principles

Conflicts can occur when multiple systems attempt to update the same conceptual information.

The preferred approach is to prevent unnecessary conflicts through clear ownership boundaries.

When a conflict occurs, resolution should consider:

- Which source is authoritative
- Whether the change was valid
- Whether the data is replicated or independently owned
- Whether the conflict represents a synchronization issue
- Whether manual review is required

The platform should avoid using arbitrary mechanisms such as "the last system to write wins" as a universal conflict strategy.

Conflict resolution should depend on the meaning and ownership of the data.

---

## Data Lifecycle and Ownership

Data ownership should remain connected to the lifecycle of the information.

For example, learning content may move through:

```text
Draft
  |
  v
In Review
  |
  v
Approved
  |
  v
Published
  |
  v
Under Maintenance
  |
  v
Archived
```

The Content domain remains responsible for the authoritative lifecycle state of that content.

Other domains may react to lifecycle changes.

For example:

```text
Content Status Changes
        |
        v
Published Content
        |
        +--> Available to Learning Paths
        +--> Available to Learners
        +--> Indexed for Search
        +--> Referenced by Assessments
```

Consumers may respond to lifecycle changes, but they should not independently determine the official lifecycle status.

---

## Relationship to Platform Architecture

Data ownership is closely connected to platform architecture and module boundaries.

Clear ownership helps define:

- Which module is responsible for a capability
- Which module is allowed to modify specific information
- How modules communicate
- Which dependencies are acceptable
- Where integration boundaries should exist

The conceptual relationship is:

```text
Platform Architecture
        |
        +--> Module Boundaries
        |         |
        |         v
        |    Domain Responsibilities
        |         |
        |         v
        |      Data Ownership
        |
        +--> Integration Principles
        |
        +--> API and Service Principles
```

Data ownership should therefore be considered when defining future module, integration, API, and service boundaries.

---

## Relationship to Security and Access Control

Data ownership and access control are related but separate concepts.

Data ownership determines who is responsible for the authoritative state of information.

Authorization determines who is allowed to perform specific actions.

For example:

```text
Content Domain
      |
      v
Owns Learning Content
      |
      +--------------------------+
      |                          |
      v                          v
Content Author              Content Reviewer
Can propose changes         Can review changes
```

Neither role changes the conceptual ownership of the data domain.

Ownership should not be confused with individual user permissions.

Detailed authentication, authorization, roles, and permission models are defined separately.

---

## Design Guidance for Future Implementation

When implementing a new platform capability, the following questions should be considered before introducing new data structures:

1. What business or learning concept does this data represent?
2. Which domain owns that concept?
3. Does an authoritative source already exist?
4. Is this data original, derived, replicated, or cached?
5. Who is allowed to create or update it?
6. Which other modules need to consume it?
7. What happens if the authoritative data changes?
8. Does this introduce duplicate ownership?
9. How should consistency be maintained?
10. What is the lifecycle of the data?

These questions should be answered conceptually before implementation details are finalized.

---

## Future Evolution

As the platform grows, data ownership practices may evolve to include:

- Formal data contracts
- Domain-specific schemas
- Data lineage tracking
- Automated synchronization monitoring
- Data quality validation
- Event-driven updates
- Master data management practices
- Data cataloging
- Formal data governance processes

These capabilities are not required at the current stage.

The current objective is to establish clear principles so that future architectural and implementation decisions do not create unnecessary ambiguity around ownership and authoritative information.

---

## Key Architectural Principle

The most important principle established by this document is:

> Data may be consumed by many parts of the platform, but responsibility for its authoritative meaning and state should remain clearly owned.

This principle supports consistency, maintainability, scalability, and clearer architectural boundaries as the Salesforce Learning Platform evolves.

---

## References

The following resources provide broader architectural and data management principles relevant to data ownership, bounded contexts, authoritative systems, and data governance:

- Martin Fowler — Bounded Context: https://martinfowler.com/bliki/BoundedContext.html

- Martin Fowler — Event-Driven Architecture: https://martinfowler.com/articles/201701-event-driven.html

- Microsoft Azure Architecture Center — Data Architecture: https://learn.microsoft.com/en-us/azure/architecture/data-guide/

- Microsoft Azure Architecture Center — Domain Analysis: https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis

- AWS Prescriptive Guidance — Data Architecture: https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-data-architecture/

- Salesforce Architecture Center: https://architect.salesforce.com/

- DAMA International — Data Management Body of Knowledge Overview: https://www.dama.org/