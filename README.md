# Salesforce Learning Platform

An open-source learning platform for developers building expertise in Salesforce, full-stack engineering, computer science foundations, and enterprise architecture.

## What You'll Find

The areas under [`full-stack/`](full-stack/) have content ready to read. The Salesforce, enterprise architecture, projects, and resources areas have their structure in place and are being filled in.

### Salesforce
Practical learning material covering:

- Apex
- Lightning Web Components
- OmniStudio
- Integrations
- Salesforce Development
- Architecture

### Frontend Engineering

Modern frontend concepts and practical development ([`full-stack/frontend/`](full-stack/frontend/)):

- HTML, CSS, and JavaScript
- TypeScript
- React, Next.js, and Vue.js
- Web Components
- Accessibility
- Performance
- Design Systems
- Testing
- Frontend Architecture

### Backend Engineering

Server-side development and data ([`full-stack/backend/`](full-stack/backend/)):

- Node.js and Express, from the first server to file handling and templates
- REST API design, documentation, and developer experience
- Authentication and authorization
- SQL, MongoDB, and database design and modeling
- Caching, real-time communication, and payments integration
- Backend architecture, testing, logging, and monitoring

### Artificial Intelligence Engineering

Building applications on large language models ([`full-stack/artificial-intelligence/`](full-stack/artificial-intelligence/)):

- How LLMs work, prompt engineering, and calling LLM APIs
- Structured output, function calling, schema validation, and streaming
- Embeddings, vector databases, and retrieval-augmented generation (RAG)
- Agents, agent design patterns, and multi-agent workflows
- Evaluating AI systems and handling their errors

### Computer Science Foundations

How computers work underneath the code ([`full-stack/computer-science-foundations/`](full-stack/computer-science-foundations/)):

- Operating systems: processes and threads, memory management, CPU scheduling, deadlocks and concurrency, file systems, and virtual memory ([section index](full-stack/computer-science-foundations/operating-systems/README.md))
- Database management systems: why databases exist, data modeling, the entity-relationship model, the relational model, normalization, and transactions, with database classification and optimization in preparation ([section index](full-stack/computer-science-foundations/database-management-systems/README.md))

### Data Structures and Algorithms

The core toolkit for solving problems efficiently ([`full-stack/data-structures-and-algorithms/`](full-stack/data-structures-and-algorithms/)):

- Time and space complexity
- Arrays, strings, linked lists, stacks, and queues
- Hashing, recursion, trees, binary search trees, heaps and priority queues, tries, and graphs
- Searching and sorting algorithms
- Dynamic programming and bit manipulation

### System Design

High-level and low-level design ([`full-stack/system-design/`](full-stack/system-design/)).

### Production Systems

Getting software into production and keeping it running ([`full-stack/production-systems/`](full-stack/production-systems/)):

- DevOps foundations, Docker, and CI/CD pipelines
- Cloud infrastructure, domains, DNS and SSL, and Nginx as a reverse proxy
- Logging, monitoring, and observability

### Web Security

How web applications are attacked and defended ([`full-stack/web-security/`](full-stack/web-security/)):

- The security mindset and security in practice
- Injection, cross-site scripting, CSRF, clickjacking, and server-side attacks
- Authentication attacks, cookies, CORS, and transport security

### Enterprise Architecture

Concepts and practices for designing scalable systems:

- System Design
- Application Architecture
- Integration Architecture
- Data Architecture
- Security
- API Design
- Design Patterns

### Projects

Production-focused projects designed to apply concepts across multiple technologies.

### Resources

Curated references including official documentation, Trailhead content, articles, videos, tools, and open-source repositories.

## Getting Started

Want to start learning right now? Pick the path that matches your goal:

- **Frontend engineering** (the area with the most content): [full-stack/frontend/](full-stack/frontend/) is a "start here" learning path that goes from Foundations through HTML, CSS, JavaScript, TypeScript, React, and Next.js to frontend architecture, in order.
- **How computers work:** the [Operating Systems section](full-stack/computer-science-foundations/operating-systems/README.md) starts with what an operating system is and builds up to scheduling, concurrency, file systems, and virtual memory.
- **Algorithms and data structures:** [full-stack/data-structures-and-algorithms/](full-stack/data-structures-and-algorithms/).
- **Backend, AI, production, system design, and web security:** the matching folders under [full-stack/](full-stack/).

## Repository Structure

```text
salesforce-learning-platform/
├── salesforce/            # Apex, LWC, OmniStudio, integrations, Salesforce architecture
├── full-stack/
│   ├── frontend/                        # HTML, CSS, JavaScript, TypeScript, React, Next.js, architecture
│   ├── backend/                         # Node.js, Express, databases, REST APIs, auth
│   ├── artificial-intelligence/         # LLM APIs, structured output, RAG, agents, evaluation
│   ├── computer-science-foundations/    # Operating systems, database management systems
│   ├── data-structures-and-algorithms/  # Complexity, core data structures, algorithms
│   ├── production-systems/              # Docker, CI/CD, cloud, networking, monitoring
│   ├── system-design/                   # High-level and low-level design
│   └── web-security/                    # Web attacks and defences
├── architecture/           # Enterprise architecture: system/application/data/API design, patterns
├── projects/                # Production-focused, multi-technology projects
├── resources/                 # Curated external references
└── docs/                        # Platform governance, content standards, and architecture docs
```
