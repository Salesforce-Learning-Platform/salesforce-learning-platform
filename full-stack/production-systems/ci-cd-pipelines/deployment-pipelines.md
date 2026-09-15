# 🚀 Deployment Pipelines

## The Final Stage: Actually Shipping the Build

After [build](build-pipelines.md) and [test](automated-testing.md) stages both succeed, a
deployment pipeline takes the resulting, verified artifact and actually gets it running on real
infrastructure — the automated equivalent of every manual `docker build` / `docker run` sequence
covered earlier in this domain.

## A Deployment Job, Depending on Prior Stages

```yaml
jobs:
  build:
    # ...(per build-pipelines.md)

  test:
    needs: build
    # ...(per automated-testing.md)

  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          docker push my-registry/my-app:${{ github.sha }}
          ssh deploy@prod-server "docker pull my-registry/my-app:${{ github.sha }} && \
            docker stop my-app && docker rm my-app && \
            docker run -d --name my-app my-registry/my-app:${{ github.sha }}"
```

`needs: [build, test]` guarantees the `deploy` job only runs *after* both prior stages have
genuinely succeeded — a direct, structural enforcement of "never deploy code that failed to build or
failed its tests." The `if: github.ref == 'refs/heads/main'` condition further restricts actual
deployment to only the `main` branch, so pushes to a feature branch build and test but never trigger
a real deployment.

## Pushing the Verified Image to a Registry First

```
docker push my-registry/my-app:${{ github.sha }}
```

This directly connects back to [Docker Architecture](../docker-and-containerization/docker-architecture.md),
earlier in this domain — the exact same commit-SHA-tagged image built and verified in the `build`
and `test` stages is pushed to a registry, ready to be pulled by the actual production server.

## Zero-Downtime Deployment: a Real Concern

```
A NAIVE deployment (stop old container, THEN start new one):
  → a real, visible GAP where the application is entirely down

A ROLLING or BLUE-GREEN deployment:
  → the NEW version starts and becomes healthy BEFORE the old
    version is removed, so there's NEVER a moment with zero
    running instances
```

For any application with real, active users, a deployment strategy that avoids even a brief total
outage matters — this is a genuinely practical concern most real deployment pipelines address, well
beyond the simplified stop-then-start example shown above.

## Rolling Back a Bad Deployment

```
Because EVERY deployed image is tagged with its exact commit SHA
(per build-pipelines.md), rolling back is simply: deploy the
PREVIOUS commit's already-built, already-tested image again.
```

This is the real, practical payoff of the commit-SHA tagging discipline established earlier in this
module — a rollback isn't a special, separate process requiring new work; it's exactly the same
deployment mechanism, just pointed at a known-good, previously-verified image instead of the newest
one.

## Common Mistakes

- Omitting `needs: [build, test]`, allowing a deployment to run even if an earlier stage in the same
  workflow actually failed.
- Deploying with a naive stop-then-start sequence for an application where even a brief, visible
  outage genuinely matters to real users.
- Having no clear, fast rollback path — discovering only *during* an active incident that reverting
  to a previous version isn't actually a well-tested, ready process.

## ➡️ Next

Continue to
[environment-based-deployments.md](environment-based-deployments.md) to see how this same pipeline
targets dev, staging, and production differently.
