# 🏗️ Infrastructure Basics: Infrastructure as Code

## The Manual Way, and Why It Breaks Down

```
Manually clicking through a cloud provider's dashboard to create
a server, configure networking, and set up a database:
  → works for ONE server, ONE time

Doing this reliably for MULTIPLE environments (dev, staging,
production), or recreating it after a failure, or letting a
TEAMMATE reproduce the exact same setup:
  → becomes genuinely error-prone and nearly impossible to do
    identically twice
```

Manual infrastructure setup has the same fundamental problem as manually editing a shared document
instead of using version control: no history, no review process, and no reliable way to reproduce
the exact same result twice.

## Infrastructure as Code (IaC): Infrastructure, Defined as a File

```hcl
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "learn-terraform"
  }
}
```

**Infrastructure as Code** means defining infrastructure — servers, networking, databases — in
version-controlled configuration files instead of manual, one-off dashboard clicks. This example, in
HashiCorp Configuration Language (HCL, used by Terraform, a widely-used IaC tool), declares exactly
one server with a specific machine image and instance size — the same file can be reviewed, versioned
in git, and run repeatedly to produce an identical result every time.

## The Three-Step Workflow

```
1. WRITE  → define the infrastructure resources in a configuration
            file
2. PLAN   → the tool shows exactly what it will create, change, or
            destroy, BEFORE anything actually happens
3. APPLY  → the tool executes those exact changes
```

The "plan" step is genuinely valuable on its own — it's the infrastructure equivalent of reviewing a
`git diff` before merging: a clear, explicit preview of exactly what will change, catching an
unintended or dangerous modification before it's actually applied.

## Why This Matters: Reproducibility and Review

```
WITHOUT IaC: "How was the production database server actually
  configured?" - often answerable only by someone who remembers,
  or by manually inspecting the live server

WITH IaC: the configuration file itself is the authoritative
  answer, reviewable in git history exactly like any other code
  change
```

This is the real, practical payoff: infrastructure configuration becomes something a team can
review, audit, and understand collectively — the same version-control discipline already applied to
application code throughout this repository, now extended to the infrastructure that code depends
on.

## Disaster Recovery, Made Tractable

```
A server crashes or is accidentally deleted:

WITHOUT IaC: rebuilding it means remembering (or reverse-
  engineering) every manual configuration step that was originally
  taken

WITH IaC: re-running "apply" against the same configuration file
  recreates the EXACT same infrastructure
```

This is a genuinely significant operational benefit beyond convenience — IaC turns "rebuild a lost
server" from a stressful, error-prone, memory-dependent task into running one already-tested,
version-controlled command.

## Common Mistakes

- Making a manual, undocumented change directly to a running server "just this once," creating a
  silent drift between the actual infrastructure and what the configuration file describes.
- Skipping the "plan" step and applying changes blindly, missing the chance to catch an unintended
  or dangerous modification before it actually happens.
- Treating infrastructure configuration files as a one-time setup task rather than an ongoing,
  version-controlled part of the codebase, reviewed and updated like any other code.

## ➡️ Next

Continue to [environment-management.md](environment-management.md) to see how these
infrastructure-as-code principles apply specifically to managing dev, staging, and production as
distinct, consistent environments.
