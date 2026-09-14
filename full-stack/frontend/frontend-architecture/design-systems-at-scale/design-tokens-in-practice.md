# Design Tokens in Practice

## Beyond a Single CSS File

[design-systems-and-design-tokens.md](../../css/css-core-fundamentals/design-systems-and-design-tokens.md)
showed design tokens as CSS custom properties in a `:root` block — sufficient for one web app. A
real product organization is often **multi-platform**: the same brand color needs to reach a web
app's CSS, a React Native or iOS app, and possibly a design tool like Figma — all staying in sync
as the brand evolves. A single CSS file can't serve any target but CSS.

## A Platform-Agnostic Source of Truth

```json
{
  "color": {
    "primary": { "$value": "#1a73e8", "$type": "color" },
    "danger": { "$value": "#d93025", "$type": "color" }
  },
  "spacing": {
    "md": { "$value": "16px", "$type": "dimension" }
  }
}
```

The **W3C Design Tokens Community Group (DTCG)** format is exactly this: a vendor-neutral JSON
structure for describing tokens, decoupled from any one platform's syntax. The idea is a single
source of truth that generates every platform's actual output, instead of maintaining the same
values by hand in several disconnected formats.

## Transforming One Source Into Many Outputs

```
tokens.json  →  (build step)  →  tokens.css       (CSS custom properties)
                              →  Colors.swift      (iOS)
                              →  colors.xml        (Android)
                              →  tokens.js         (JS/React Native)
```

A token-transformation pipeline reads the platform-neutral JSON and generates each platform's own
native format automatically — a CSS custom properties file for the web app (feeding directly into
the pattern from
[design-systems-and-design-tokens.md](../../css/css-core-fundamentals/design-systems-and-design-tokens.md)),
a Swift file of color constants for iOS, and so on. Changing the brand's primary color means
editing exactly one JSON value and re-running the build — every platform picks up the change
automatically, with no risk of one platform's copy drifting out of sync with another's.

## Design Tool Integration

Modern design tools (Figma, Sketch, Adobe) increasingly support the same DTCG token format
directly, meaning a designer changing a color in Figma can, with the right tooling, be the same
source of truth that generates the engineering team's CSS — collapsing what used to be a manual,
error-prone "designer hands off a color hex code, engineer types it into code" step into one shared
system both sides read from.

## Common Mistakes

- Maintaining hand-written, parallel copies of the same token values across web, iOS, and Android
  codebases — exactly the "typed in a dozen places" problem
  [design-systems-and-design-tokens.md](../../css/css-core-fundamentals/design-systems-and-design-tokens.md)
  warns against, just spread across platforms instead of files.
- Treating the token-transformation pipeline as a one-time setup rather than an ongoing part of the
  design system's release process — new and changed tokens need to flow through it every time.
- Assuming a multi-platform token pipeline is necessary for every project — a single web app with
  no native mobile counterpart is often genuinely well served by plain CSS custom properties alone,
  per this module's README knowledge check.

## Next

Continue to [consistency-at-scale.md](consistency-at-scale.md) to see how a design system stays
correct as both the product and the number of consuming teams grow.
