# 🤖 Artificial Intelligence Engineering

## 📚 Overview

These modules are about building applications on large language models: calling model APIs, getting output a program can rely on, letting a model use tools, retrieving your own data to ground answers (RAG), and building and evaluating agents. The first module needs no programming background. Code examples are in JavaScript and Python, and [Schema Validation with Zod](schema-validation-with-zod/README.md) builds on the backend's REST API Design.

## 🧭 The Learning Path

Work through the modules in this order. The last column names the earlier modules each one relies on, so you can also start partway through; links point to modules in other areas.

| # | Module | What it covers | Builds on |
|---|--------|----------------|-----------|
| 1 | [Understanding AI Fundamentals](understanding-ai-fundamentals/README.md) | AI, machine learning, and deep learning, and how a model learns; no code | Nothing: no programming or AI background needed |
| 2 | [How LLMs Actually Work](how-llms-actually-work/README.md) | Tokens, context windows, temperature, and why models hallucinate | AI Fundamentals |
| 3 | [Calling LLM APIs Properly](calling-llm-apis-properly/README.md) | Request structure, token costs, context limits, and handling rate limits | How LLMs Work |
| 4 | [Prompt Engineering Fundamentals](prompt-engineering-fundamentals/README.md) | Clear instructions, examples, step-by-step reasoning, and predictable output formats | Calling LLM APIs |
| 5 | [Structured Output in AI Systems](structured-output-in-ai-systems/README.md) | Why free-text output breaks programs, and how schema-constrained output helps | Prompt Engineering |
| 6 | [Generating JSON Responses from LLMs](generating-json-responses-from-llms/README.md) | Native JSON output, schema-based prompting, tool calls for extraction, and validation | Structured Output |
| 7 | [Schema Validation with Zod for AI Responses](schema-validation-with-zod/README.md) | Zod schemas for model output, safe parsing, failure policies, and retries | Generating JSON, [REST API Design](../backend/rest-api-design/README.md) |
| 8 | [Function Calling and Tool Calling](function-calling-tool-calling/README.md) | Letting a model call your functions while your code enforces the business rules | Generating JSON, Prompt Engineering, Schema Validation with Zod |
| 9 | [Streaming AI Responses](streaming-responses/README.md) | Server-Sent Events, showing partial output, streaming UX, and streaming tool calls | Generating JSON, Schema Validation with Zod, Function Calling |
| 10 | [Error Handling in AI Applications](error-handling-in-ai-applications/README.md) | Broken output, timeouts, layered retries, and logging failures | Schema Validation with Zod, Calling LLM APIs, Streaming Responses |
| 11 | [Understanding Embeddings](understanding-embeddings/README.md) | Embedding vectors, similarity search, and chunking | How LLMs Work |
| 12 | [Integrating Vector Databases](integrating-vector-databases/README.md) | Indexes, approximate nearest-neighbor search, and metadata filters, including per-tenant access | Embeddings, Function Calling |
| 13 | [Building a RAG Pipeline](building-a-rag-pipeline/README.md) | Retrieval-augmented generation, ending in a document question-and-answer system | Embeddings, Vector Databases, Generating JSON, Schema Validation with Zod |
| 14 | [Evaluating AI Systems](evaluating-ai-systems/README.md) | Catching hallucinations, confidence scores, retrieval metrics, and observability | RAG Pipeline, Error Handling |
| 15 | [Understanding AI Agents](understanding-ai-agents/README.md) | Workflows or agents, the agent loop, and when an agent is worth it | Function Calling, Error Handling |
| 16 | [Agent Design Patterns](agent-design-patterns/README.md) | Planner and executor, researcher and writer, critic and refiner, and routing | AI Agents, Function Calling |
| 17 | [LangChain in Practice](langchain-practical/README.md) | Prompt templates, chains, tools, memory, and agents in LangChain | AI Agents, Agent Design Patterns, Function Calling |
| 18 | [Building a Multi-Agent Workflow](building-a-multi-agent-workflow/README.md) | Two complete multi-stage pipelines, one for text and one for images | Agent Design Patterns, AI Agents, Schema Validation with Zod |
| 19 | [Multi-Agent Architecture Concerns](multi-agent-architecture-concerns/README.md) | Latency, cost, debugging, shared state, logging, and when it pays off | AI Agents, Agent Design Patterns, Multi-Agent Workflow |
| 20 | [Engineering WITH AI](engineering-with-ai/README.md) | Directing AI coding tools and reviewing the code they write | AI Agents, Schema Validation with Zod |

## ➡️ Start Here

Begin with [Understanding AI Fundamentals](understanding-ai-fundamentals/README.md). If you already know what a model is and how it learns, start with [How LLMs Actually Work](how-llms-actually-work/README.md). After the last module, the course continues with [Production Systems](../production-systems/README.md).
