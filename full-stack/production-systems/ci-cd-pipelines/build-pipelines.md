# 🏗️ Build Pipelines

## Turning Source Code Into a Deployable Artifact

The "build" stage of a CI/CD pipeline is where raw source code is transformed into something
actually *deployable* — installing dependencies, compiling/bundling code, and (commonly) building a
Docker image, per [Writing Dockerfiles](../docker-and-containerization/writing-dockerfiles.md),
earlier in this domain.

## A Real Build Job

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install dependencies
        run: npm install
      - name: Build application
        run: npm run build
      - name: Build Docker image
        run: docker build -t my-app:${{ github.sha }} .
```

Each step runs in sequence: checking out the code, installing dependencies, running whatever build
process the application uses (bundling frontend assets, compiling TypeScript), and finally building
a Docker image tagged with the specific commit SHA — giving every build a precise, traceable
identifier.

## Why Tag Images With the Commit SHA

```
${{ github.sha }} → the EXACT commit that produced this image

my-app:latest → ambiguous - WHICH commit does "latest" actually
                 refer to, right now, at this moment?
```

Tagging a build with its exact commit SHA (rather than only a generic tag like `latest`) directly
supports the debugging discipline already established in
[logging-every-step-of-the-pipeline.md](../../artificial-intelligence/multi-agent-architecture-concerns/logging-every-step-of-the-pipeline.md) —
if a specific deployed version misbehaves, its exact source code is immediately, unambiguously
identifiable from the image tag alone.

## Caching Dependencies for Faster Builds

```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
```

Just as [Docker's layer caching](../docker-and-containerization/docker-images-and-containers.md)
avoids redundant work on unchanged dependencies, a CI pipeline can cache installed dependencies
between runs — keyed by a hash of the lockfile, so the cache is only reused when dependencies
genuinely haven't changed, and correctly invalidated the moment they do.

## Failing Fast on a Broken Build

```
A build step that FAILS should stop the pipeline IMMEDIATELY -
subsequent steps (tests, deployment) should NEVER run against
code that didn't even successfully build.
```

This is a deliberately simple but important principle: a CI pipeline's steps run in sequence
specifically so a failure at any stage halts everything downstream — there's no value in running
tests against an application that failed to build in the first place, and doing so would only waste
time and obscure the real, root problem.

## Common Mistakes

- Tagging every build image as `latest` with no traceable identifier back to the specific commit
  that produced it, making it impossible to know exactly what's actually running in a given
  environment.
- Skipping dependency caching entirely, needlessly re-downloading and reinstalling unchanged
  dependencies on every single pipeline run.
- Configuring a pipeline to continue running subsequent steps even after an earlier step has
  already failed, wasting compute time on work that can't possibly succeed.

## ➡️ Next

Continue to [automated-testing.md](automated-testing.md) to see the testing stage that runs against
a successfully built application before it's ever considered for deployment.
