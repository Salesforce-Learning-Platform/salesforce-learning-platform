# 🔤 What Are Tokens, and Why Everything Becomes Tokens

## The Smallest Unit an LLM Actually Processes

**Tokens** are the smallest individual units a language model actually works with — they can
correspond to whole words, sub-words, individual characters, or even raw bytes, depending on the
tokenizer. Before an LLM processes any text at all, that text is first **encoded** into a sequence
of tokens; the model never directly "sees" plain English words the way a person reading this
sentence does.

## Tokens Aren't Always Whole Words

```
"unbelievable" might tokenize as: "un" + "believ" + "able"
"hello"        might tokenize as: "hello"        (a single, common token)
```

A common, frequently-occurring word is often exactly one token. A less common or longer word often
splits into several smaller sub-word tokens. This is a deliberate design choice: representing
`"hello"` as one token is more data-efficient than three, while still letting the tokenizer handle
a genuinely novel or rare word by breaking it into smaller, previously-seen pieces rather than
failing outright.

## Roughly, Not Exactly, Words

For Claude specifically, one token corresponds to roughly 3.5 English characters on average — not a
fixed, predictable count, and it varies by language (a language with different character/word
structures tokenizes differently). This is why token count and word count are related but not
interchangeable — a rough rule of thumb, not an exact conversion.

## Why This Matters Practically, Not Just Academically

- **Pricing** — API usage for essentially every LLM provider is billed per token, covered fully in
  [calling-llm-apis-properly](../calling-llm-apis-properly/) — understanding tokens is directly
  tied to understanding real, actual cost.
- **Context window limits** — the maximum amount of text a model can consider at once (covered
  next, in
  [what-is-a-context-window-and-why-prompts-get-cut.md](what-is-a-context-window-and-why-prompts-get-cut.md))
  is measured in tokens, not words or characters.
- **Truncation behavior** — a response cut off mid-sentence is very often the model simply hitting
  its maximum output token limit, not a bug.

## Common Mistakes

- Assuming token count and word count are roughly interchangeable in every case — they're related,
  but genuinely vary based on the specific words, language, and tokenizer involved.
- Forgetting that tokens (not characters or words) are what's actually billed and counted against a
  context window — a cost or length estimate based on word count alone can be meaningfully off.
- Assuming every word is always exactly one token — longer, rarer, or non-English words frequently
  split into multiple tokens.

## ➡️ Next

Continue to
[what-is-a-context-window-and-why-prompts-get-cut.md](what-is-a-context-window-and-why-prompts-get-cut.md)
to see the direct, practical limit tokens impose on a single conversation.
