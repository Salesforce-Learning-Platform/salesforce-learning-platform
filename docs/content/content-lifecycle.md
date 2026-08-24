# Content Lifecycle and Status Management

## Purpose

This document defines how learning content moves through the Salesforce Learning Platform from initial creation to long-term maintenance or retirement.

A content lifecycle provides a consistent way to understand the current state of a learning resource, control when content is available to learners, and ensure that outdated or incomplete material is not presented as current guidance.

The lifecycle applies to learning content across the platform, including technical topics, conceptual documentation, learning paths, projects, exercises, assessments, and supporting resources.

---

## Lifecycle Overview

Each content item progresses through a defined lifecycle:

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

## Status Definitions

### Draft

Draft content is actively being created or revised.

Content in this state may be incomplete, experimental, or undergoing significant structural changes. Draft material should not be treated as finalized learning guidance.

Typical activities include:

- Creating the initial structure
- Writing learning material
- Adding examples and explanations
- Defining metadata
- Adding references and supporting resources
- Revising content based on feedback

A draft may move to review once it is sufficiently complete for evaluation.

### In Review

Content enters the review state when it is ready for structured evaluation.

The review process checks whether the content meets the platform's established standards for:

- Technical accuracy
- Clarity and readability
- Structural consistency
- Learning objectives
- Metadata completeness
- Appropriate references
- Alignment with related learning content

Review may result in approval or a request for changes.

Content requiring substantial changes returns to the Draft state.

### Approved

Approved content has successfully passed the required review process.

Approval confirms that the content is considered suitable for publication according to the standards defined for the platform.

Approved content may still require final publication activities, such as integration into a learning path, repository organization, or release preparation.

Approval does not prevent future updates.

### Published

Published content is considered available as an active learning resource.

Content in this state should be:

- Complete
- Reviewed
- Structurally consistent
- Appropriate for its intended audience
- Connected to relevant learning paths or related resources where applicable

Published content remains subject to maintenance and periodic review.

Publication represents the current active version of the learning material.

### Under Maintenance

Published content moves into Under Maintenance when updates, corrections, or improvements are required.

This may occur because of:

- Changes in technology
- Platform updates
- Incorrect or outdated information
- Broken examples or references
- Changes to recommended practices
- Improvements identified through content review

Depending on the significance of the change, the content may remain available while updates are prepared or may require a temporary restriction from active learning paths.

Once maintenance work is complete, the content should be reviewed before returning to Published status.

### Archived

Archived content is no longer maintained as an active learning resource.

Content may be archived when:

- The technology is no longer relevant
- The subject has been replaced
- The material is obsolete
- The content has been consolidated into another resource
- Continued maintenance is no longer justified

Archived content should remain identifiable as historical or inactive material where it is retained.

Archiving should not automatically mean deletion. Retention may be useful for historical reference, migration tracking, or understanding previous learning structures.

## Lifecycle Transitions

The primary lifecycle transitions are:

| Current Status | Possible Next Status |
|---|---|
| Draft | In Review |
| In Review | Draft, Approved |
| Approved | Published, Draft |
| Published | Under Maintenance, Archived |
| Under Maintenance | Draft, In Review, Published, Archived |
| Archived | Draft, Under Maintenance |

Reactivating archived content should require deliberate review because previously archived information may no longer meet current technical or learning standards.

## Status Ownership

Each content item should have a clearly understood owner or responsible contributor.

The responsible party is expected to:

- Maintain the accuracy of the content
- Respond to identified issues where appropriate
- Coordinate updates and reviews
- Ensure lifecycle status reflects the actual condition of the content

Ownership may change as the platform grows or as content responsibilities are distributed across contributors.

The lifecycle model does not require a specific organizational structure at this stage.

## Relationship to Versioning

Lifecycle status and content versioning represent different concepts.

Lifecycle status describes the current operational condition of a content item.

Versioning describes how changes to that content are identified and managed over time.

For example:

**Content:** LWC Fundamentals  
**Version:** 1.2  
**Status:** Published

Later:

**Content:** LWC Fundamentals  
**Version:** 1.3 (in progress)  
**Status:** Under Maintenance

Versioning rules are defined separately in the Learning Content Versioning Strategy.

## Relationship to Content Quality

A lifecycle status should communicate the maturity and operational condition of content, but it should not replace quality standards.

For example, moving content to Approved does not remove the need for future technical validation. Similarly, Published content may later require maintenance because technologies and recommended practices change.

The lifecycle works alongside:

- Content standards
- Content review guidelines
- Content metadata
- Learning path principles
- Content versioning
- Quality assurance processes

Together, these mechanisms provide a structured approach to managing learning content over time.

## Future Evolution

As the platform evolves, lifecycle management may later include additional capabilities such as:

- Automated review reminders
- Scheduled content audits
- Formal approval workflows
- Content ownership assignment
- Publication controls
- Deprecation notices
- Version history tracking
- Automated archival policies

These capabilities are intentionally not implemented or defined as platform requirements at this stage.

This document establishes the conceptual lifecycle model that future processes and technical systems can build upon.
