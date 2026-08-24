# Learning Content Versioning Strategy

## Purpose

This document defines how changes to learning content are managed and identified over time.

Learning content evolves as technologies, platform capabilities, recommended practices, and learner requirements change. A versioning strategy provides a structured way to track meaningful changes while preserving clarity about which state of the content is current.

The strategy applies to learning modules, documentation, exercises, projects, assessments, learning paths, and other maintained learning resources.

---

## Versioning Principles

Content versioning should provide enough information to understand the significance of a change without creating unnecessary administrative overhead.

The versioning approach is based on the following principles:

- Changes should be traceable.
- Meaningful revisions should be identifiable.
- The current version should be clear.
- Significant changes should be distinguishable from minor corrections.
- Versioning should support content maintenance rather than complicate it.
- Historical changes should remain understandable where practical.

---

## Version Structure

Learning content may use a three-part version format:

**MAJOR.MINOR.PATCH**

For example: **2.4.1**

Each part represents a different level of change.

### Major Version

A major version represents a substantial change to the learning content.

Examples may include:

- Significant restructuring of the content.
- Major changes to learning objectives.
- Replacement of outdated concepts or technologies.
- Changes that alter the expected learner journey.
- Large-scale revisions to projects, exercises, or assessments.

Example: **1.0.0 → 2.0.0**

### Minor Version

A minor version represents a meaningful enhancement that does not fundamentally replace the existing learning resource.

Examples may include:

- Adding new sections.
- Expanding explanations.
- Adding relevant examples.
- Updating supporting material.
- Improving exercises or learning activities.

Example: **1.2.0 → 1.3.0**

### Patch Version

A patch version represents a limited correction or small improvement.

Examples may include:

- Correcting inaccurate information.
- Fixing broken references.
- Correcting typographical errors.
- Updating minor examples.
- Making small clarity improvements.

Example: **1.2.3 → 1.2.4**

---

## Initial Version

New content should begin with an identifiable initial version.

A newly published learning resource may use **1.0.0**.

Draft content does not necessarily require formal version increments for every editing session.

Version changes become relevant when a meaningful revision is prepared for review, publication, or maintenance tracking.

---

## Relationship to Content Lifecycle

Versioning and lifecycle status serve different purposes.

Versioning identifies the evolution of the content.

Lifecycle status identifies the current operational state of the content.

Example:

**Content:** Apex Fundamentals  
**Version:** 1.4.0  
**Status:** Published

During a major revision:

**Content:** Apex Fundamentals  
**Version:** 2.0.0  
**Status:** Under Maintenance

The content may move through different lifecycle states without requiring a version change, depending on whether the underlying learning material has changed.

---

## Version Change Guidelines

A version should be updated when a change is significant enough to affect the content itself or the learner experience.

The following guidance provides a general decision model:

| Type of Change | Suggested Version Update |
|---|---|
| Typographical correction | Patch |
| Broken link correction | Patch |
| Small clarification | Patch |
| New example or supporting section | Minor |
| Expanded learning objective | Minor |
| New exercise or assessment activity | Minor |
| Significant restructuring | Major |
| Major technology or platform change | Major |
| Complete replacement of learning approach | Major |

These guidelines provide consistency but should not prevent reasonable judgment where a change does not fit neatly into a single category.

---

## Version History

Where meaningful, maintained content should include a record of significant version changes.

A version history may contain:

- Version number
- Date of change
- Summary of the change
- Reason for the update

For example:

| Version | Change Summary |
|---|---|
| 1.0.0 | Initial published version |
| 1.1.0 | Added practical examples |
| 1.1.1 | Corrected broken references |
| 2.0.0 | Restructured content for an updated learning path |

The level of detail should remain proportional to the importance of the changes.

---

## Compatibility and Dependencies

Some learning content may depend on other resources, technologies, or platform capabilities.

When a significant version change affects related learning content, those dependencies should be reviewed.

For example, a major update to a foundational topic may require updates to:

- Advanced modules
- Related exercises
- Assessments
- Learning paths
- Project instructions
- Referenced examples

Versioning should therefore support dependency awareness without requiring every related resource to receive a version change automatically.

---

## Draft and Working Changes

Not every content modification requires an immediate version increment.

During active development, multiple edits may occur before a new version is established.

Version updates should represent meaningful states of the content rather than every individual editing action.

Git history can provide detailed change tracking, while content versions provide a higher-level view of changes that matter to learners and maintainers.

---

## Future Evolution

As the platform grows, versioning may later include additional capabilities such as:

- Automated version validation
- Structured changelogs
- Release notes
- Content compatibility indicators
- Version comparison tools
- Automated dependency impact analysis
- Deprecation and migration guidance

These capabilities are not required at the current stage.

This document establishes the conceptual versioning strategy that can guide future content management processes and platform capabilities.
