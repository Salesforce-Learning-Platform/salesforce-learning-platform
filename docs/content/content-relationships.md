# Content Relationships and Dependency Model

## Purpose

This document defines how learning content within the Salesforce Learning Platform can relate to, depend on, and connect with other learning resources.

Learning content should not be treated as a collection of isolated documents. Topics, exercises, projects, assessments, and learning paths may build upon one another. A clear relationship model helps maintain logical learning journeys and makes the impact of content changes easier to understand.

This model establishes the conceptual relationships between content items without defining a specific technical implementation.

---

## Relationship Principles

Content relationships should support a structured and understandable learning experience.

The relationship model is based on the following principles:

- Learning connections should have a clear purpose.
- Dependencies should be identifiable where they affect learner progression.
- Foundational content should be distinguishable from advanced content.
- Related resources should provide meaningful additional value.
- Content relationships should avoid unnecessary complexity.
- Changes to important content should consider dependent resources.

---

## Content Relationship Types

A learning resource may have one or more relationships with other content.

The primary relationship types are:

### Prerequisite

A prerequisite relationship indicates that learners should understand or complete one resource before progressing to another.

For example:

**JavaScript Fundamentals → Lightning Web Components**

The JavaScript Fundamentals resource provides foundational knowledge that may be required to understand Lightning Web Components effectively.

A prerequisite does not necessarily mean that learners must be technically blocked from accessing the next resource. The platform may later determine how prerequisite relationships are enforced.

---

### Related Content

Related content represents resources that are relevant to the same topic or learning objective but are not required dependencies.

For example:

**LWC Fundamentals ↔ Lightning Data Service**

A learner studying one topic may benefit from access to the other, even when neither resource is required for completion.

Related content should provide useful contextual connections without creating unnecessary navigation.

---

### Parent and Child

A parent-child relationship represents a structural hierarchy between learning resources.

For example:

**Salesforce Development**

→ Apex Fundamentals

→ Lightning Web Components

→ SOQL Fundamentals

The parent resource provides a broader grouping or context, while child resources represent more focused learning units.

This relationship may be used within learning paths, topic structures, modules, or other content organizations.

---

### Dependency

A dependency exists when one content item relies on another resource for accuracy, context, continuity, or learner understanding.

For example, an advanced exercise may depend on concepts introduced in a foundational module.

Dependencies should be reviewed when significant changes are made to the source content.

A dependency does not automatically require changes to related content. The impact should be evaluated based on the nature of the update.

---

### Continuation

A continuation relationship represents content that extends a previous learning experience.

For example:

**Apex Fundamentals → Advanced Apex Concepts**

The second resource continues the learning journey by building on concepts previously introduced.

Continuation relationships can help learners identify logical next steps.

---

### Supporting Resource

A supporting resource provides additional information, examples, references, or practical material for another content item.

Examples include:

- Reference documentation
- Code examples
- Exercises
- Checklists
- External learning resources
- Supporting diagrams

Supporting resources may improve understanding without being required for progression.

---

## Dependency Direction

Content dependencies should have a clear direction.

For example:

**Resource A → Resource B**

This indicates that Resource B depends on knowledge, context, or functionality provided by Resource A.

Understanding the direction of a dependency is important when evaluating the impact of content changes.

If Resource A undergoes a significant update, Resource B may need to be reviewed.

The reverse does not necessarily apply.

---

## Dependency Impact

When a significant change is made to a content item, related resources should be evaluated where appropriate.

Potential impact areas include:

- Prerequisite content
- Advanced modules
- Related exercises
- Assessments
- Learning paths
- Projects
- Supporting documentation
- Referenced examples

The level of review should be proportional to the significance of the change.

Minor corrections may not require dependency analysis, while major restructuring or technology changes may affect multiple related resources.

---

## Relationship Metadata

Content relationships may later be represented through structured metadata.

Potential relationship information may include:

- Related content identifier
- Relationship type
- Dependency direction
- Relationship status
- Version compatibility
- Notes or context

The exact metadata structure is not defined at this stage.

This document establishes the conceptual model that future content management processes or platform capabilities may use.

---

## Relationship Management

Relationships between learning resources should remain understandable and maintainable.

As the platform grows, content contributors should avoid creating relationships that do not provide a meaningful benefit to learners or maintainers.

Relationship management may include:

- Reviewing dependencies during major updates
- Removing obsolete relationships
- Adding relationships when new learning paths are created
- Updating references when content is archived
- Reviewing related content after significant restructuring

The goal is to maintain useful connections without creating an unnecessarily complex dependency network.

---

## Relationship to Content Lifecycle

Content relationships may change as content moves through its lifecycle.

For example:

- Draft content may have relationships that are still being defined.
- Published content should have reviewed relationships where dependencies affect learners.
- Content under maintenance may require related resources to be reviewed.
- Archived content may require relationships to be removed, redirected, or marked as historical.

Lifecycle changes do not automatically require every related resource to change status.

Each relationship should be evaluated according to its relevance and dependency impact.

---

## Relationship to Versioning

Versioning and content relationships are connected but represent different concerns.

Versioning identifies changes to an individual content resource over time.

Relationships identify how that resource connects with other learning content.

A major version change may require a review of dependent resources, while a minor or patch change may have little or no impact.

This allows dependency management to remain proportionate to the actual significance of a content update.

---

## Future Evolution

As the Salesforce Learning Platform evolves, the relationship model may later support capabilities such as:

- Automated dependency mapping
- Prerequisite validation
- Learning path generation
- Dependency impact analysis
- Visual relationship diagrams
- Content recommendation systems
- Version compatibility tracking
- Automated detection of broken relationships

These capabilities are not required at the current stage.

This document establishes the conceptual foundation for understanding how learning resources connect and depend on one another across the platform.