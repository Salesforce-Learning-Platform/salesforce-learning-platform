# 🛠️ Using Tools and Memory Modules

## Defining a Tool With `@tool`

```python
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    return look_up_weather(location)  # your real implementation
```

LangChain's `@tool` decorator turns an ordinary Python function into a tool object — the function's
**docstring becomes the tool's description**, and its type hints become the argument schema. This
is exactly the same `name`/`description`/`input_schema` structure from
[what-is-tool-calling-and-why-it-matters.md](../function-calling-tool-calling/what-is-tool-calling-and-why-it-matters.md),
generated automatically from ordinary Python instead of written by hand as a JSON schema.

## Binding Tools to a Model

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-opus-5", max_tokens=1024)
model_with_tools = model.bind_tools([get_weather])

response = model_with_tools.invoke("What's the weather in San Francisco?")
print(response.tool_calls)
# [{'name': 'get_weather', 'args': {'location': 'San Francisco'}, 'id': '...'}]
```

`bind_tools()` attaches the tool definitions to the model, and the resulting response carries a
`tool_calls` list — LangChain's equivalent of the raw API's `tool_use` content blocks from
[what-is-tool-calling-and-why-it-matters.md](../function-calling-tool-calling/what-is-tool-calling-and-why-it-matters.md).
Executing the actual tool and feeding the result back is still the application's job, exactly as it
was with the raw API — LangChain standardizes the *interface*, not the underlying contract.

## Memory: Giving a Chain Conversation History

```python
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    def add_messages(self, messages): self.messages.extend(messages)
    def clear(self): self.messages = []

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain_with_memory = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

response = chain_with_memory.invoke(
    {"question": "What's Python?"},
    config={"configurable": {"session_id": "user-123"}},
)
```

`RunnableWithMessageHistory` wraps a chain to automatically load prior conversation turns before
each call and save the new exchange afterward, keyed by a `session_id` — the same fundamental idea
as manually appending to a `messages` list (as seen throughout earlier modules in this domain), now
handled automatically per-session.

## Memory Is Just Storage — It Doesn't Manage Itself

```
An in-memory store (InMemoryHistory, as above) works for a demo,
but for a REAL, long-running application, conversation history
needs a PERSISTENT backend (Redis, Postgres, MongoDB via
langchain-community) so history survives beyond one process's
memory.
```

This is directly the same lesson as
[caching-local-and-redis](../../backend/caching-local-and-redis/), covered earlier in this domain
for a different purpose — in-process storage is fine for development, but a real, multi-instance
application needs shared, persistent storage. A memory store that grows unbounded also needs the
same summarization/truncation discipline as
[token-budgeting-prompt-size-response-size-and-overflow-planning.md](../calling-llm-apis-properly/token-budgeting-prompt-size-response-size-and-overflow-planning.md)
already established — an ever-growing history eventually overflows the context window.

## Common Mistakes

- Writing a vague docstring on a `@tool`-decorated function, producing the exact same
  wrong-tool-selection problem covered in
  [letting-ai-decide-which-function-to-call.md](../function-calling-tool-calling/letting-ai-decide-which-function-to-call.md).
- Using an in-memory session store in production, silently losing all conversation history on every
  restart or across multiple server instances.
- Letting conversation history grow unbounded with no summarization or truncation strategy,
  eventually overflowing the model's context window.

## ➡️ Next

Continue to [working-with-agents.md](working-with-agents.md) to see LangChain's own implementation
of the full agentic loop, combining tools and reasoning together.
