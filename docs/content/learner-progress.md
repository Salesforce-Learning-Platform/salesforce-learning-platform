# Learner Progress Tracking Model

## Purpose

This document defines the conceptual model for tracking learner progress across the Salesforce Learning Platform.

Learner progress should provide a clear representation of how individuals move through learning content, complete activities, and advance across broader learning paths.

The purpose of progress tracking is not limited to showing completion percentages. It should provide a meaningful view of a learner's current position, completed work, and remaining learning activities.

This document defines the conceptual model without prescribing a specific database structure, tracking mechanism, or technical implementation.

---

## Progress Tracking Principles

The learner progress model is based on the following principles:

- Progress should be understandable to learners.
- Completion states should have clear meaning.
- Progress should reflect meaningful learning activity where possible.
- Different content types may require different completion criteria.
- Progress should support learning paths and individual resources.
- Progress data should remain connected to the relevant learning content.
- Tracking should avoid implying knowledge mastery when only content completion has occurred.

---

## Core Progress States

A learner's interaction with a content item may be represented through several conceptual states.

### Not Started

The learner has not yet begun the content.

The resource may be available to the learner, but no meaningful learning activity has been recorded.

---

### In Progress

The learner has started the content but has not yet satisfied the defined completion criteria.

The learner may return to the content and continue from their previous point, depending on future platform capabilities.

---

### Completed

The learner has satisfied the completion criteria defined for the content.

Completion may represent different actions depending on the resource type.

For example:

- Reading a learning module
- Completing an exercise
- Finishing a project activity
- Reaching the end of a structured learning resource

Completion does not automatically indicate that the learner has demonstrated full knowledge or mastery.

---

### Requires Review

A learner may return to previously completed content when additional review is recommended or required.

This state may become relevant when:

- The content has changed significantly.
- A related assessment identifies a knowledge gap.
- A prerequisite requires refreshed understanding.
- The learner chooses to revisit the material.

The exact conditions for this state are not defined at this stage.

---

## Progress Across Content Types

Different learning resources may require different approaches to progress tracking.

### Learning Modules

Progress may reflect completion of sections, lessons, or defined learning activities.

### Exercises

Progress may depend on completion of the required task or submission of an expected outcome.

### Assessments

Progress may include assessment status, attempts, and outcomes where those capabilities are introduced.

### Projects

Progress may represent advancement through defined project milestones or deliverables.

### Learning Paths

Learning path progress may represent the combined progress across the resources included within that path.

The exact calculation model may vary based on the structure and purpose of each content type.

---

## Learning Path Progress

A learning path provides a broader view of progression across multiple learning resources.

For example:

**Salesforce Development Path**

- Apex Fundamentals — Completed
- SOQL Fundamentals — Completed
- Lightning Web Components — In Progress
- Advanced Apex — Not Started

The learner's overall progress may later be calculated from the completion state of the individual resources.

A future implementation may support different weighting models, but no specific calculation formula is defined at this stage.

---

## Progress and Assessments

Content completion and assessment outcomes should remain conceptually distinct.

For example, a learner may complete a module but not pass its associated assessment.

Similarly, a learner may demonstrate strong understanding without every interaction being recorded as completed.

Progress tracking should therefore avoid treating completion as equivalent to validated knowledge.

Assessment results may contribute to progression rules where appropriate, but the exact relationship will depend on future platform requirements.

---

## Progress and Content Changes

Changes to learning content may affect previously recorded learner progress.

The impact should depend on the significance of the update.

For example:

- A minor correction may not affect completion status.
- A new section may result in additional content being available without immediately removing previous completion.
- A major restructuring may require a review of how previous completion is represented.

The relationship between content versioning and learner progress may be refined as the platform evolves.

---

## Progress Records

A conceptual learner progress record may eventually include information such as:

- Learner identifier
- Content identifier
- Current progress state
- Completion status
- Date started
- Date completed
- Last activity date
- Related content version
- Assessment outcome where applicable

The exact data model is intentionally not defined at this stage.

---

## Learner Progress Visibility

Learners should eventually be able to understand their own progress without needing to interpret complex internal tracking information.

Future progress views may include:

- Current learning activity
- Completed resources
- Remaining resources
- Learning path progress
- Assessment outcomes
- Recommended next steps
- Content requiring review

The specific user interface and visualization approach are outside the scope of this document.

---

## Relationship to Content Lifecycle

Learner progress may interact with content lifecycle changes.

For example, when content is archived, previously recorded learner progress may need to remain historically understandable even if the content is no longer active.

When published content undergoes significant maintenance, the platform may later determine whether learners should be notified or whether completed progress requires review.

The lifecycle model does not currently define automatic progress changes.

---

## Future Evolution

As the Salesforce Learning Platform evolves, learner progress tracking may later support capabilities such as:

- Resume learning
- Progress synchronization across devices
- Learning streaks
- Milestone tracking
- Personalized recommendations
- Competency-based progression
- Progress analytics
- Learning reminders
- Content update notifications

These capabilities are not required at the current stage.

This document establishes the conceptual foundation for representing and managing learner progress across the Salesforce Learning Platform.