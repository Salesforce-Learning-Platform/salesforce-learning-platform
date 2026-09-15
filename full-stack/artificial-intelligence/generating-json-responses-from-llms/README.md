# 🧾 Generating JSON Responses from LLMs

## Purpose

[Structured Output in AI Systems](../structured-output-in-ai-systems/) established *why* structured
output matters and *that* a genuine schema-constrained guarantee exists. This module gets concrete:
the actual mechanisms for generating JSON — native JSON mode, schema-based prompting as a portable
fallback, and tool calling as an alternative technique — plus validating what comes back before
trusting it.

## 🎯 Learning Objectives

- Use a model's native, schema-constrained JSON output mode.
- Guide a model toward structured output with schema-based prompting, when native support isn't
  used.
- Explain the basics of using tool calling specifically as a technique for extracting structured
  data.
- Validate a returned structure before using it, even when it was schema-constrained.

## 📋 Prerequisites

- [Structured Output in AI Systems](../structured-output-in-ai-systems/) — this module assumes the
  *why* is already understood, and focuses specifically on the *how*.

## 📂 Files in This Module

| File | Covers |
|---|---|
| [using-model-supported-json-mode-for-structured-outputs.md](using-model-supported-json-mode-for-structured-outputs.md) | Native, schema-constrained JSON output via `output_config.format` |
| [guiding-models-with-schema-based-prompting.md](guiding-models-with-schema-based-prompting.md) | Describing the desired schema directly in the prompt, as a portable fallback |
| [basics-of-tool-function-calling.md](basics-of-tool-function-calling.md) | Using tool calling as an alternative technique for structured data extraction |
| [validating-the-returned-structure-before-using-it.md](validating-the-returned-structure-before-using-it.md) | Why even guaranteed-valid JSON still needs business-rule validation |
| [building-structured-profile-analysis-data-with-scores-strengths-and-suggestions.md](building-structured-profile-analysis-data-with-scores-strengths-and-suggestions.md) | A complete, worked example tying every technique together |

## 🔍 When to Deep-Dive vs. Skim

Deep-dive
[validating-the-returned-structure-before-using-it.md](validating-the-returned-structure-before-using-it.md) —
it's a genuinely common misconception that schema-constrained output means validation is no longer
needed at all; understanding exactly what's still guaranteed and what isn't is essential before
trusting AI-generated data in a real application.

## ✅ Quick Knowledge Check

<details>
<summary>If a model's native JSON mode guarantees the response is valid JSON matching your schema, is Zod validation still worth running on it?</summary>

Yes — schema-constrained output guarantees the *shape* and *types* are correct, but not that the
*values* make real business sense (a `score` field that's technically a valid number but outside an
expected 0–100 range, for instance). See
[validating-the-returned-structure-before-using-it.md](validating-the-returned-structure-before-using-it.md).

</details>

<details>
<summary>Is tool calling only useful for letting an AI actually perform real actions?</summary>

Not only — tool calling (specifically with `strict: true`) can also be used purely as a technique
for extracting reliably structured data from a model, even when no real action is ever actually
taken. See [basics-of-tool-function-calling.md](basics-of-tool-function-calling.md).

</details>

## 📚 References

- Anthropic, [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

## ➡️ Continue Your Learning Path

Continue to the [Schema Validation with Zod module](../schema-validation-with-zod/) to build out
the validation layer this module's last two files already began applying.
