# 🔗 Building Chains and Prompt Templates

## Prompt Templates — Reusable, Parameterized Prompts

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Summarize the following {document_type} in {sentence_count} sentences:\n\n{content}"
)

formatted = prompt.invoke({
    "document_type": "support ticket",
    "sentence_count": "2",
    "content": "Customer reports their order #4821 arrived damaged...",
})
```

A `ChatPromptTemplate` is exactly what it sounds like: a prompt with named placeholders (`{document_
type}`, `{content}`), filled in with real values at call time. This is the same idea as an ordinary
Python f-string, but as a reusable, first-class object LangChain's other components can compose
with directly.

## A Chain: Composing a Prompt With a Model

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-opus-5", max_tokens=512)

chain = prompt | llm  # the pipe operator — LCEL in its simplest form

result = chain.invoke({
    "document_type": "support ticket",
    "sentence_count": "2",
    "content": "Customer reports their order #4821 arrived damaged...",
})
print(result.content)
```

The `|` (pipe) operator connects the prompt template's output directly into the model's input — a
**chain**. This is LangChain's actual core idea: components (`Runnable`s) that all share a common
interface, letting any two be connected this way. [overview-of-lcel-concepts.md](overview-of-lcel-concepts.md),
later in this module, formalizes exactly what makes this composition work.

## Adding an Output Parser

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"document_type": "support ticket", "sentence_count": "2", "content": "..."})
print(result)  # a plain string, not a wrapped response object
```

A third piece — an output parser — extracts just the plain text from the model's response object,
so the chain's final result is a simple string rather than requiring `.content` to be accessed
manually every time. This three-step shape (prompt → model → parser) is one of the most common
patterns in real LangChain code.

## Why This Matters: The Same Prompt, Reused Safely

```python
support_summary = chain.invoke({"document_type": "support ticket", "sentence_count": "2", "content": ticket_text})
review_summary = chain.invoke({"document_type": "product review", "sentence_count": "1", "content": review_text})
```

The real value of a template over an f-string built by hand: the *same*, already-tested chain
object can be reused across many different inputs without re-constructing the prompt logic each
time — directly parallel to
[writing-clear-instructions.md](../prompt-engineering-fundamentals/writing-clear-instructions.md)'s
clarity principle, now packaged as a reusable, testable unit rather than scattered string
concatenation throughout an application.

## System Prompts in a Template

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise technical writer. Never use filler phrases."),
    ("human", "{content}"),
])
```

A `ChatPromptTemplate` can include a structured system message alongside the user turn, exactly
mirroring the `system`/`user` role structure covered in
[message-roles-system-user-assistant.md](../calling-llm-apis-properly/message-roles-system-user-assistant.md)
— LangChain's template is a convenience wrapper around the same underlying message structure, not a
different concept.

## Common Mistakes

- Building a prompt manually with string concatenation inside application code repeatedly instead
  of a reusable `ChatPromptTemplate` object.
- Forgetting `StrOutputParser()` and then needing to manually call `.content` everywhere a chain's
  result is used.
- Assuming a chain automatically retries or validates its output — chains compose steps together,
  they don't add the error-handling discipline from
  [Error Handling in AI Applications](../error-handling-in-ai-applications/) on their own.

## ➡️ Next

Continue to
[using-tools-and-memory-modules.md](using-tools-and-memory-modules.md) to see how a chain connects
to real tools and remembers prior conversation turns.
