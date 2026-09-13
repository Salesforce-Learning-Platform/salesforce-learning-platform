# Inclusive Design Principles

## Accessibility Is Not One Checklist for One User

It's tempting to think of accessibility as a fixed checklist satisfying "screen reader users."
In reality, it covers a wide range of permanent, temporary, and situational conditions:

| Category | Permanent example | Temporary example | Situational example |
|---|---|---|---|
| Vision | Blindness | Recovering from eye surgery | Bright sunlight glare on a phone screen |
| Motor | A missing limb | A broken arm | Holding a baby with one arm |
| Hearing | Deafness | An ear infection | A loud, noisy environment |
| Cognitive | A learning disability | Sleep deprivation | Distracted, multitasking |

This framing (used widely in inclusive design practice) matters practically: designing captions
for deaf users also helps someone watching a video with the sound off in a public place; designing
clear, jargon-free instructions for someone with a cognitive disability also helps every user under
time pressure or stress. Accessibility work broadly benefits far more people than it might first
appear to target.

## WCAG's Four Principles

The [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG22/quickref/)
organize accessibility requirements under four principles, commonly remembered by the acronym
**POUR**:

- **Perceivable**: information must be presentable in ways every user can perceive (text
  alternatives for images, captions for video, sufficient color contrast).
- **Operable**: interface components must be operable by every user (full keyboard support, no
  content that flashes in a way that could trigger seizures).
- **Understandable**: content and operation must be understandable (clear language, predictable
  navigation, helpful error messages).
- **Robust**: content must work reliably across current and future assistive technologies (valid,
  semantic markup that parses correctly — tying directly back to this platform's HTML modules).

## Accessibility as a Practice, Not a Final Audit

The most reliable way to build accessible interfaces is to apply the practices in this module (and
[Semantic HTML and Browser Rendering](../semantic-html-and-browser-rendering/)) from the start —
semantic elements, correct labels, keyboard operability, and focus management — rather than
treating accessibility as a compliance pass applied to a finished product. Retrofitting
accessibility onto an already-built, deeply non-semantic interface is dramatically more expensive
than building it in from the beginning, and often surfaces structural problems that require
significant rework rather than a small fix.

## Common Mistakes

- Treating accessibility as "done" after a single automated scan — automated tools reliably catch
  only a fraction of real accessibility issues (missing keyboard support and confusing focus order,
  for example, are very hard to detect automatically).
- Designing for an imagined "typical user" rather than the actual range of permanent, temporary,
  and situational conditions real users experience.
- Deferring accessibility work to "after launch," when the cost of retrofitting is consistently
  higher than building it in from the start.

## Module Summary

Across this module: the first rule of ARIA is to prefer native HTML, since ARIA can describe a
role but never grants native keyboard behavior on its own (see
[aria-when-html-isnt-enough.md](aria-when-html-isnt-enough.md)); every interactive element and
dynamic UI change must remain fully keyboard-operable, with a visible focus indicator and
deliberate focus management (see
[keyboard-navigation-and-focus-management.md](keyboard-navigation-and-focus-management.md)); and
accessibility is best understood as designing for the full, varied range of human ability and
context — captured by WCAG's Perceivable/Operable/Understandable/Robust principles — built in from
the start rather than audited in at the end.
