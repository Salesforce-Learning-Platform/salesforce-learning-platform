# Platform Information Architecture

## Purpose

This document defines the high-level information architecture for the Salesforce Learning Platform.

Information architecture describes how the platform's major areas, learning resources, and supporting information are organized and connected.

The purpose of this model is to establish a conceptual structure that helps learners, contributors, and future platform capabilities navigate and understand the relationships between different types of information.

This document does not define visual design, page layouts, navigation components, or technical implementation.

---

## Information Architecture Principles

The platform information architecture should follow several core principles:

- Information should be organized according to its purpose and relationship to other content.
- Learners should be able to understand where they are within the learning structure.
- Related learning resources should be discoverable.
- Navigation should support both structured learning and direct exploration.
- Foundational concepts should connect clearly to advanced content.
- The structure should remain scalable as the amount of learning content grows.
- Content organization should not depend solely on a specific user interface or technical implementation.

---

## High-Level Platform Structure

The Salesforce Learning Platform may be organized into the following conceptual areas:

- Platform Home
- Learning Catalog
- Learning Paths
- Topics and Modules
- Assessments
- Projects and Practical Learning
- Supporting Resources
- Learner Progress
- Contributor and Content Management

These areas represent logical information domains rather than a required navigation structure.

---

## Platform Home

The Platform Home provides an entry point into the learning environment.

Its purpose may include helping users:

- Understand the purpose of the platform.
- Discover available learning areas.
- Continue existing learning activities.
- Access recommended or relevant content.
- Navigate toward structured learning paths or individual topics.

The exact presentation of the Platform Home is not defined at this stage.

---

## Learning Catalog

The Learning Catalog represents the broader collection of available learning content.

Content within the catalog may be organized using information such as:

- Subject area.
- Technology.
- Skill level.
- Content type.
- Learning objective.
- Related learning path.
- Prerequisites.

The catalog should support discovery without requiring learners to follow a predefined sequence.

---

## Learning Paths

Learning Paths represent structured sequences of learning content.

A learning path may connect:

- Foundational topics.
- Intermediate modules.
- Advanced concepts.
- Exercises.
- Assessments.
- Practical projects.

Learning paths provide guided progression, while individual content items may also remain accessible independently.

A single learning resource may belong to more than one learning path where appropriate.

---

## Topics and Modules

Topics and modules represent individual units of learning content.

A topic may cover a broader subject area, while modules may provide focused learning within that subject.

For example:

Salesforce Development

↓

Lightning Web Components

↓

Component Fundamentals

↓

Component Communication

↓

Advanced Patterns

The exact hierarchy may vary depending on the subject and learning structure.

Topics and modules should be connected through clearly defined relationships where dependencies or prerequisites exist.

---

## Assessments

Assessments represent resources used to evaluate learner understanding.

Assessments may be associated with:

- Individual modules.
- Groups of related topics.
- Learning path milestones.
- Practical projects.

Assessment information should remain connected to the learning objectives and content it is intended to evaluate.

The detailed assessment framework is defined separately.

---

## Projects and Practical Learning

Projects provide opportunities for learners to apply knowledge in practical scenarios.

Projects may connect multiple areas of learning and may require completion of specific prerequisites.

The information architecture should allow projects to be associated with:

- Relevant topics.
- Learning paths.
- Required skills.
- Supporting resources.
- Assessments where applicable.

Projects should be discoverable both as part of structured learning and as independent practical experiences where appropriate.

---

## Supporting Resources

Supporting resources provide additional information that helps learners understand or apply a topic.

Examples may include:

- Reference material.
- Documentation.
- Examples.
- Guides.
- External resources.
- Supplementary explanations.

Supporting resources should maintain a clear relationship with the learning content they support.

They should not replace the primary learning structure unless explicitly intended to function as standalone learning content.

---

## Learner Progress

The information architecture should provide a conceptual location for learner progress information.

Progress may relate to:

- Completed modules.
- Current learning activities.
- Learning path progress.
- Assessment results.
- Project completion.
- Learning milestones.

The detailed model for progress tracking is defined separately.

This area represents the learner's relationship with the platform's learning content rather than a separate category of learning material.

---

## Contributor and Content Management

As the platform evolves, contributors may require areas for managing learning content.

These conceptual areas may support:

- Content creation.
- Draft management.
- Review activities.
- Publication.
- Maintenance.
- Version tracking.
- Archival.

Contributor and content management information should remain distinct from the learner-facing learning experience where appropriate.

The specific workflow and technical implementation are intentionally not defined in this document.

---

## Content Relationships

Information architecture depends on relationships between different resources.

A learning resource may have relationships such as:

- Prerequisite.
- Next recommended topic.
- Related topic.
- Part of a learning path.
- Supports a project.
- Associated assessment.
- Supporting resource.

These relationships allow the platform to represent learning as a connected structure rather than a collection of isolated documents.

The detailed relationship and dependency model is defined separately.

---

## Conceptual Navigation Model

The platform should support multiple ways of moving through information.

A learner may navigate through:

### Structured Navigation

Following a defined learning path from one learning resource to the next.

### Exploratory Navigation

Discovering topics through categories, search, related content, or recommendations.

### Contextual Navigation

Moving between directly related resources based on prerequisites, dependencies, assessments, projects, or supporting material.

These navigation approaches may coexist without requiring a single learning method.

---

## Conceptual Information Hierarchy

The platform may be understood through the following high-level hierarchy:

Salesforce Learning Platform

├── Learning Catalog
│   ├── Topics
│   │   ├── Modules
│   │   ├── Exercises
│   │   ├── Assessments
│   │   └── Supporting Resources
│
├── Learning Paths
│   ├── Foundations
│   ├── Intermediate Learning
│   ├── Advanced Learning
│   └── Projects
│
├── Projects and Practical Learning
│
├── Learner Progress
│
└── Content Management
    ├── Draft
    ├── Review
    ├── Publication
    ├── Maintenance
    └── Archive

This hierarchy represents a conceptual model and may evolve as the platform architecture develops.

---

## Scalability Considerations

The information architecture should support future growth without requiring major restructuring of existing content.

As the platform expands, it may include:

- Additional technologies.
- New learning domains.
- More specialized learning paths.
- Expanded assessment models.
- Larger project collections.
- Contributor communities.
- New methods of content discovery.

The structure should therefore support expansion through relationships, metadata, categorization, and reusable content organization.

---

## Relationship to User Experience

Information architecture provides the underlying structure that supports the user experience.

User experience principles determine how learners interact with and move through the platform.

Information architecture determines how the underlying information is organized and related.

These concerns are connected but should remain conceptually distinct.

---

## Future Evolution

As the Salesforce Learning Platform evolves, the information architecture may later include:

- Advanced search capabilities.
- Personalized recommendations.
- Dynamic learning path generation.
- Skill-based content organization.
- Knowledge graphs.
- Adaptive navigation.
- Role-based content views.
- AI-assisted content discovery.

These capabilities are not defined as current platform requirements.

This document establishes the conceptual information architecture that can guide future platform design, content organization, navigation, and technical implementation.