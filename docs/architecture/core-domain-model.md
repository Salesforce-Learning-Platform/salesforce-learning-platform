# Core Domain Model

## Purpose

This document defines the core conceptual domains and entities that make up the Salesforce Learning Platform.

A domain model provides a shared understanding of the important concepts within a system and the relationships between them. It establishes a common vocabulary that can be used by architects, developers, contributors, and future platform maintainers.

The purpose of this model is not to define database tables, Salesforce objects, APIs, or implementation details.

Instead, it answers a fundamental architectural question:

> What are the core concepts the Salesforce Learning Platform needs to understand and manage?

This conceptual model provides a foundation for future decisions involving platform architecture, data modeling, module boundaries, APIs, permissions, learner experiences, integrations, and operational processes.

---

## Scope

The domain model focuses on the major concepts required to support the learning platform.

The initial model includes the following primary concepts:

- Learning Path
- Learning Module
- Learning Content
- Learning Objective
- Learner
- Learner Progress
- Assessment
- Assessment Result
- Exercise
- Project
- Content Lifecycle
- Content Version
- Content Metadata
- Content Relationships

These concepts represent the core business and learning domains of the platform.

Additional concepts may be introduced as the platform evolves, but new concepts should be added only when they represent a distinct responsibility or meaningful domain concern.

---

## Domain Modeling Principles

The core domain model follows several architectural principles.

### Shared Language

The platform should use consistent terminology for important concepts.

For example, a Learning Path, Learning Module, Assessment, and Project should each have a clearly understood meaning.

The same concept should not be represented using multiple names unless there is a deliberate architectural distinction between them.

A shared vocabulary reduces ambiguity between contributors and helps maintain consistency as the platform grows.

---

### Clear Responsibilities

Each domain concept should have a clearly defined responsibility.

For example:

- A Learning Path defines a broader learning journey.
- A Learning Module organizes related learning material.
- Learning Content provides instructional knowledge.
- An Assessment validates learner understanding.
- A Project supports practical application.
- Learner Progress records advancement through learning activities.

A concept should not take responsibility for unrelated concerns simply because doing so may appear convenient during implementation.

Clear responsibilities help prevent tightly coupled and difficult-to-maintain systems.

---

### Separation of Domain and Implementation

The domain model describes what the platform manages rather than how it is technically implemented.

For example, Learner is a domain concept.

The eventual technical implementation could use Salesforce, an external identity provider, a custom application, or multiple connected systems.

Those implementation decisions are outside the scope of this document.

The domain model should remain stable even if the underlying technology changes.

---

### Explicit Relationships

Important relationships between domain concepts should be understandable and intentional.

For example:

- A Learning Path organizes Learning Modules.
- A Learning Module structures Learning Content.
- Learning Content supports Learning Objectives.
- Assessments validate understanding.
- Learners generate Progress and Assessment Results.
- Projects allow learners to apply knowledge.

Explicit relationships provide a foundation for future data, service, API, and module design.

---

### Support for Evolution

The initial domain model should provide sufficient structure without attempting to predict every future platform requirement.

The model may evolve as the platform gains new capabilities.

However, changes to core concepts should be deliberate because they may affect multiple areas of the platform.

---

# Core Domain Overview

The Salesforce Learning Platform can initially be organized into six primary domains:

1. Learning Structure
2. Learning Content
3. Learning Experience
4. Assessment and Knowledge Validation
5. Learner Progress
6. Content Management

These domains group related concepts according to their primary responsibility.

---

## Domain Relationship Overview

```text
Learning Path
    |
    ├── organizes Learning Modules
    |
    └── defines learning progression


Learning Module
    |
    └── structures Learning Content


Learning Content
    |
    ├── supports Learning Objectives
    ├── may include Exercises
    ├── may be validated by Assessments
    ├── may support Projects
    ├── has Lifecycle Status
    ├── has Version information
    └── has Metadata


Learner
    |
    ├── has Progress
    ├── has Assessment Results
    └── participates in Projects
```

This diagram represents conceptual relationships rather than mandatory technical relationships.

For example, the eventual implementation does not require every relationship to be represented by a direct database relationship.

---

# Learning Structure Domain

The Learning Structure domain defines how learning is organized.

Its primary purpose is to provide learners with a logical and understandable progression through related subjects.

The main concepts within this domain are:

- Learning Path
- Learning Module
- Learning Objective
- Learning Dependency

---

## Learning Path

A Learning Path represents a structured learning journey.

It organizes related Learning Modules into a meaningful progression.

A Learning Path may represent:

- A technical specialization
- A professional role
- A platform capability
- A skill progression
- A certification preparation journey
- A structured curriculum

Examples may include:

- Salesforce Developer Learning Path
- Lightning Web Components Learning Path
- Salesforce Administrator Learning Path
- API Integration Learning Path

A Learning Path defines the broader learning journey.

It does not need to contain all instructional material directly.

Instead, it provides structure by organizing related Learning Modules and defining an intended progression.

---

## Learning Module

A Learning Module represents a logical grouping of related learning material.

Modules divide a broader Learning Path into manageable areas of study.

For example:

```text
Salesforce Developer Learning Path
    |
    ├── Platform Fundamentals
    |
    ├── Data Modeling
    |
    ├── Apex Development
    |
    └── Lightning Web Components
```

A Learning Module may organize:

- Learning Content
- Exercises
- Assessments
- Projects
- Supporting Resources

The exact technical implementation of a Learning Module is not defined by this domain model.

The important principle is that the module provides a meaningful organizational boundary for related learning material.

---

## Learning Objective

A Learning Objective defines what a learner should understand or be able to do after completing a learning experience.

Learning Objectives provide an important connection between:

- Learning Content
- Exercises
- Assessments
- Projects
- Learner Progress

For example:

```text
Learning Objective:

Understand the lifecycle of a Lightning Web Component
and identify appropriate lifecycle hooks for a given scenario.
```

Learning Objectives help ensure that learning activities have a clear purpose.

They also provide a basis for determining whether assessments and practical activities are validating the intended knowledge or skill.

---

## Learning Dependency

A Learning Dependency represents a relationship where one learning resource should be understood before progressing to another.

For example:

```text
JavaScript Fundamentals
        |
        ↓
Lightning Web Components
        |
        ↓
Advanced LWC Patterns
```

Dependencies may represent:

- Required prerequisites
- Recommended preparation
- Sequential learning
- Conceptual dependencies

A dependency does not automatically mean that the platform must block access.

The future platform may support different dependency behaviors depending on learner experience requirements.

---

# Learning Content Domain

The Learning Content domain represents the instructional material provided to learners.

Its purpose is to communicate knowledge, explain concepts, provide examples, and support skill development.

Learning Content may include:

- Technical documentation
- Conceptual explanations
- Tutorials
- Examples
- Exercises
- Reference material
- Supporting resources

A Learning Content item may be associated with one or more Learning Modules.

The domain model should not assume that all content belongs permanently to a single module because reusable content may support multiple learning experiences.

---

## Learning Content Relationships

Learning Content may have relationships with:

- Learning Modules
- Learning Objectives
- Assessments
- Exercises
- Projects
- Other Learning Content
- Dependencies
- Lifecycle Status
- Versions
- Metadata

Conceptually:

```text
Learning Content
    |
    ├── supports Learning Objectives
    |
    ├── is organized by Learning Modules
    |
    ├── may have dependencies
    |
    ├── may include or reference Exercises
    |
    ├── may be validated by Assessments
    |
    ├── may support Projects
    |
    ├── has Lifecycle Status
    |
    ├── has Version information
    |
    └── has Metadata
```

These relationships allow learning content to participate in multiple areas of the platform without requiring the content itself to own every responsibility.

---

# Learning Experience Domain

The Learning Experience domain represents activities through which learners interact with knowledge and apply what they learn.

The primary concepts include:

- Exercise
- Project
- Learning Activity
- Learning Resource

---

## Exercise

An Exercise provides a focused opportunity for a learner to apply a specific concept or skill.

Exercises are generally smaller in scope than projects.

For example:

```text
Learning Content:
Understanding Apex Triggers

        |
        ↓

Exercise:
Create a trigger that updates a related record
when a specific condition occurs.
```

An Exercise may support one or more Learning Objectives.

The future platform may track exercise completion, attempts, results, or other relevant information depending on the learner progress model.

---

## Project

A Project represents a larger practical learning experience.

Projects may combine knowledge from multiple Learning Modules or Learning Content items.

For example:

```text
Learning Path:
Salesforce Developer
        |
        ├── Data Modeling
        ├── Apex Development
        └── Lightning Web Components
                |
                ↓
Project:
Build a Customer Management Application
```

Projects allow learners to demonstrate practical application across multiple concepts.

The detailed project framework is defined separately in the Project-Based Learning Framework.

---

## Learning Activity

A Learning Activity is a conceptual representation of an action that contributes to the learning experience.

Examples may include:

- Reading learning content
- Completing an exercise
- Taking an assessment
- Completing a project
- Reviewing supporting material

This concept may become useful if the platform requires a common model for representing different learner interactions.

At the current stage, Learning Activity is a conceptual abstraction rather than a mandatory implementation entity.

---

# Assessment and Knowledge Validation Domain

The Assessment and Knowledge Validation domain represents how learner understanding and knowledge may be evaluated.

The primary concepts include:

- Assessment
- Assessment Item
- Assessment Result
- Knowledge Validation

---

## Assessment

An Assessment evaluates a learner's understanding of one or more Learning Objectives.

Assessments may include different forms of validation depending on platform requirements.

Examples may include:

- Knowledge questions
- Scenario-based questions
- Practical tasks
- Project evaluation
- Other structured validation activities

An Assessment should have a clear relationship with the knowledge or Learning Objectives it is intended to validate.

---

## Assessment Item

An Assessment Item represents an individual unit within an Assessment.

Depending on the assessment type, an item may represent:

- A question
- A scenario
- A practical task
- A validation requirement

The detailed structure of Assessment Items is intentionally outside the scope of this conceptual domain model.

---

## Assessment Result

An Assessment Result represents the outcome of a learner's assessment attempt or evaluation.

It may eventually include information such as:

- Completion state
- Score
- Outcome
- Attempt information
- Completion date

The exact structure should be defined later according to assessment, reporting, and learner progress requirements.

---

# Learner Progress Domain

The Learner Progress domain represents the learner's relationship with learning resources and activities over time.

The primary concepts include:

- Learner
- Progress
- Completion
- Assessment Result
- Project Participation

---

## Learner

A Learner represents a person participating in learning activities through the platform.

The Learner concept may eventually connect with:

- Identity
- Authentication
- Profile information
- Access permissions
- Learning activity
- Progress
- Assessment Results
- Project participation

The Learner concept should remain separate from the technical identity system used to authenticate an individual.

Authentication answers:

> Who is attempting to access the platform?

The Learner domain answers:

> Who is participating in the learning experience?

These concepts may eventually refer to the same individual, but they represent different architectural concerns.

---

## Progress

Progress represents a learner's advancement through a learning structure or activity.

Progress may eventually be associated with:

- Learning Paths
- Learning Modules
- Learning Content
- Exercises
- Projects
- Assessments

For example:

```text
Learner
    |
    ↓
Learning Path Progress
    |
    ├── Module 1: Complete
    |
    ├── Module 2: In Progress
    |
    └── Module 3: Not Started
```

The detailed rules for calculating and maintaining progress are defined separately in the Learner Progress Tracking Model.

---

# Content Management Domain

The Content Management domain represents the information and processes required to manage learning resources over time.

The primary concepts include:

- Content Lifecycle
- Content Version
- Content Metadata
- Content Ownership
- Content Relationships

---

## Content Lifecycle

Content Lifecycle represents the current operational state of a learning resource.

The lifecycle may include states such as:

```text
Draft
  ↓
In Review
  ↓
Approved
  ↓
Published
  ↓
Under Maintenance
  ↓
Archived
```

Lifecycle management helps distinguish active learning material from incomplete, outdated, or historical resources.

The detailed lifecycle model is defined separately in the Content Lifecycle and Status Management documentation.

---

## Content Version

Content Version represents a meaningful revision of learning material.

Versioning provides a higher-level understanding of how content has evolved.

For example:

```text
Version 1.0.0
Initial published version

        ↓

Version 1.1.0
Added new examples and learning material

        ↓

Version 1.1.1
Corrected references and minor inaccuracies
```

Content versions should represent meaningful states rather than every individual editing action.

Detailed versioning rules are defined separately in the Learning Content Versioning Strategy.

---

## Content Metadata

Content Metadata describes information about a learning resource that helps the platform organize, discover, classify, and manage it.

Metadata may include:

- Title
- Description
- Topic
- Skill level
- Learning Objectives
- Dependencies
- Lifecycle Status
- Version
- Content Owner
- Related Learning Paths

The exact metadata structure may evolve as the platform grows.

---

# Core Entity Responsibilities

The following table summarizes the primary responsibility of each core concept.

| Core Concept | Primary Responsibility |
|---|---|
| Learning Path | Defines a structured learning journey |
| Learning Module | Organizes related learning material |
| Learning Content | Provides instructional knowledge |
| Learning Objective | Defines expected learner understanding or capability |
| Learning Dependency | Represents prerequisite or recommended relationships |
| Exercise | Provides focused practical application |
| Project | Provides broader practical application |
| Assessment | Validates learner understanding |
| Assessment Item | Represents an individual unit of assessment |
| Assessment Result | Records the outcome of assessment activity |
| Learner | Represents a participant in the learning platform |
| Progress | Represents advancement through learning activities |
| Content Lifecycle | Represents the operational state of content |
| Content Version | Represents meaningful content evolution |
| Content Metadata | Provides descriptive and management information |

This responsibility model should guide future architecture and implementation decisions.

---

# Conceptual Relationship Model

The following diagram provides a broader view of the core domain relationships.

```text
                         ┌─────────────────┐
                         │     Learner     │
                         └────────┬────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
        ┌──────────┐      ┌────────────────┐    ┌─────────────┐
        │ Progress │      │Assessment Result│    │   Project   │
        └──────────┘      └────────┬───────┘    └─────────────┘
                                   │
                                   ▼
                            ┌──────────────┐
                            │  Assessment  │
                            └──────┬───────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Learning Objective │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ Learning Content │
                         └─────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
             ┌────────────┐ ┌──────────────┐ ┌─────────────┐
             │  Exercise  │ │Content Version│ │   Metadata  │
             └────────────┘ └──────────────┘ └─────────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │Content Lifecycle │
                          └──────────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │ Learning Module  │
                         └─────────┬────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │  Learning Path   │
                         └──────────────────┘
```

This diagram represents conceptual relationships only.

It should not be interpreted as a database schema, object model, or mandatory service architecture.

---

# Domain Boundaries

The core domain model intentionally separates concepts according to their primary responsibility.

For example:

- Learning Structure is responsible for organizing the learning journey.
- Learning Content is responsible for instructional material.
- Assessment is responsible for knowledge validation.
- Learner Progress is responsible for recording advancement.
- Content Management is responsible for maintaining learning resources over time.

This separation helps prevent unrelated responsibilities from becoming tightly coupled.

Future platform modules should respect these conceptual boundaries unless there is a deliberate architectural reason to introduce a controlled dependency.

---

# What This Domain Model Does Not Define

This document does not define:

- Salesforce object structures
- Database schemas
- API contracts
- Application services
- UI components
- Authentication mechanisms
- Authorization rules
- Detailed permission models
- Integration implementations
- Data storage technologies
- Event structures
- Deployment architecture

These decisions belong to later stages of platform architecture.

The purpose of this document is to establish the conceptual foundation before implementation-specific decisions are made.

---

# Relationship to Other Architecture Documents

This domain model should be considered alongside the following platform documentation:

- Platform Architecture Principles
- Platform Module Boundaries
- Data Ownership and Source of Truth Principles
- Platform Integration Principles
- Authentication and Authorization Principles
- Platform Roles and Permission Model
- API and Service Interaction Principles
- Learner Progress Tracking Model
- Assessment and Knowledge Validation Framework
- Project-Based Learning Framework
- Content Lifecycle and Status Management
- Learning Content Versioning Strategy
- Content Relationships and Dependency Model

Each document addresses a different architectural concern.

The Core Domain Model provides the shared conceptual vocabulary that connects these concerns.

---

# Future Evolution

As the Salesforce Learning Platform evolves, the domain model may expand to include additional concepts such as:

- Skills
- Competencies
- Certifications
- Badges
- Recommendations
- Learning Plans
- Organizations
- Teams
- Instructors
- Mentors
- Content Contributors
- Reviewers
- Notifications
- Learning Analytics

New concepts should be introduced when they represent a clear domain responsibility rather than simply mirroring a technical implementation detail.

Changes to core concepts should also consider their impact on:

- Existing content
- Learner progress
- Assessments
- APIs
- Integrations
- Permissions
- Reporting
- Platform modules

---

# Architectural Guidance

The Core Domain Model should serve as a reference point for future architectural decisions.

Before introducing a new entity, service, module, or data structure, the following questions should be considered:

1. Which domain does this responsibility belong to?
2. Does an existing concept already represent this responsibility?
3. Is a new concept genuinely required?
4. What relationships will the new concept introduce?
5. Who should own the concept and its data?
6. Will the concept affect learner progress, permissions, content, or integrations?
7. Is the concept a business domain concern or merely an implementation detail?

Applying these questions consistently will help maintain a coherent domain model as the platform grows.

---

## Conclusion

The Core Domain Model establishes a shared conceptual foundation for the Salesforce Learning Platform.

The primary concepts are centered around:

- Structuring learning
- Managing instructional content
- Supporting practical learning experiences
- Validating knowledge
- Tracking learner progress
- Maintaining content over time

The model intentionally remains independent of specific technologies and implementation approaches.

This allows the Salesforce Learning Platform to evolve while maintaining a consistent understanding of its most important concepts and their responsibilities.

Future architecture, data modeling, APIs, modules, integrations, permissions, and learner experiences should use this domain model as a foundational reference and evolve it deliberately as new platform requirements emerge.

---

## References

The concepts in this document are informed by established software architecture and domain modeling practices. These references provide additional background for readers who want to explore the principles in greater depth.

### Martin Fowler — Domain Model

Martin Fowler defines the Domain Model pattern as an object model that represents the business domain and incorporates both behavior and data.

Reference:

Martin Fowler, *Patterns of Enterprise Application Architecture — Domain Model*  
https://martinfowler.com/eaaCatalog/domainModel.html

This reference supports the distinction between the conceptual business domain and the technical implementation of a system.

### Martin Fowler — Domain-Driven Design

Domain-Driven Design emphasizes building software around a well-developed understanding of the business domain, its concepts, rules, and relationships.

Reference:

Martin Fowler, *Domain-Driven Design*  
https://martinfowler.com/bliki/DomainDrivenDesign.html

This provides background for identifying the core concepts and relationships that make up the Salesforce Learning Platform domain model.

### C4 Model — Software Architecture Abstractions

The C4 model provides a structured way to describe software architecture using hierarchical abstractions, including software systems, containers, components, and code.

Reference:

Simon Brown, *The C4 Model for Visualising Software Architecture*  
https://c4model.com/

Additional reference:

Simon Brown, *C4 Model Abstractions*  
https://c4model.com/abstractions

The C4 model is relevant to this document because it reinforces the importance of defining architecture at different levels of abstraction without prematurely mixing conceptual domain concerns with detailed implementation decisions.

### Martin Fowler — Presentation, Domain, and Data Layering

Separating presentation concerns, domain logic, and data access is a widely used architectural approach for managing complexity and reducing unnecessary coupling between different responsibilities.

Reference:

Martin Fowler, *Presentation-Domain-Data Layering*  
https://martinfowler.com/bliki/PresentationDomainDataLayering.html

This reference supports the separation between the platform's conceptual domain model and future implementation-specific architectural layers.

---

## Reference Usage

These references are provided as architectural background and supporting material.

This document does not prescribe the direct adoption of any specific framework, architectural pattern, implementation methodology, or technology.

The Salesforce Learning Platform domain model should continue to evolve based on the actual requirements, capabilities, relationships, and operational needs of the platform.