# 🏛️ Facade Pattern

## The Problem: a Genuinely Complex Subsystem

```python
# WITHOUT Facade - the CALLER must know and correctly orchestrate
# EVERY step of a genuinely complex subsystem
video_converter = VideoConverter()
codec = CodecFactory.extract(video_file)
bitrate_reader = BitrateReader.read(video_file, codec)
audio_mixer = AudioMixer()
result = video_converter.convert(bitrate_reader, audio_mixer.fix(video_file))
```

```
Correctly using a genuinely complex subsystem (here, video
conversion) requires the caller to understand MULTIPLE internal
classes, in the RIGHT order, with the right parameters - real,
significant knowledge the caller shouldn't NEED to have just to
accomplish one simple, high-level goal.
```

## The Pattern

```python
class VideoConversionFacade:
    def convert(self, filename: str, target_format: str):
        codec = CodecFactory.extract(filename)
        bitrate_reader = BitrateReader.read(filename, codec)
        audio = AudioMixer().fix(filename)
        return VideoConverter().convert(bitrate_reader, audio, target_format)
```

```python
facade = VideoConversionFacade()
facade.convert("holiday.mp4", "avi")   # ONE simple call - the
                                          # caller never needs to know
                                          # ANY of the subsystem's
                                          # internal classes exist
```

A **Facade** provides a simple, unified interface hiding a genuinely complex subsystem's internal
detail — the caller interacts with *one* simple method, while the facade itself handles correctly
orchestrating every internal step underneath.

## Facade vs. Adapter: a Genuinely Common Point of Confusion

```
ADAPTER: makes an EXISTING interface look like a DIFFERENT one -
  solves an INCOMPATIBILITY problem, wrapping typically ONE object

FACADE: provides a SIMPLER interface to a COMPLEX subsystem - solves
  a COMPLEXITY problem, typically wrapping MANY objects together
```

Both patterns "wrap" something, which is exactly why they're easy to conflate — but they solve
genuinely different problems: Adapter is about making two things *compatible*, Facade is about
making something *simpler to use*, regardless of compatibility.

## A Real Use Case: a Payment Processing SDK

```
Processing a real payment might genuinely involve: validating the
card, checking fraud signals, contacting the payment network,
handling currency conversion, and logging the transaction - a
Facade exposes ONE method, processPayment(amount, card), hiding
this entire internal orchestration from every calling application.
```

This is a genuinely common, practical real-world pattern — most third-party SDKs are, in effect,
Facades: a simple, small public surface hiding substantial internal complexity the SDK's own
maintainers handle so the SDK's users don't have to.

## The Facade Doesn't Prevent Direct Subsystem Access

```
A Facade provides a SIMPLER path for the common case - it does
NOT prevent code that genuinely needs finer control from still
reaching the underlying subsystem classes DIRECTLY, when that
genuinely deeper control is actually needed.
```

This is a genuinely important, often-overlooked nuance — a well-designed Facade is an *additional*,
simpler entry point, not necessarily the *only* one; code with genuinely advanced needs can still
bypass it when the simplified interface doesn't cover a specific, real requirement.

## Common Mistakes

- Adding so much logic directly into the Facade itself that it becomes its own complex subsystem,
  defeating the simplification it was meant to provide.
- Confusing Facade's "simplify a complex subsystem" goal with Adapter's "translate an incompatible
  interface" goal — the two patterns solve genuinely different problems despite both "wrapping"
  something.
- Making the Facade the *only* way to reach the subsystem when some genuinely advanced use cases
  legitimately need finer-grained, direct access.

## ➡️ Next

Continue to [proxy-pattern.md](proxy-pattern.md) to see a pattern that also wraps an object, but
for a genuinely different purpose: controlling access to it.
