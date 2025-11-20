# Book Taxonomy Matrix

**3-Tier Cascading Hierarchy for Intelligent Book Selection**

Reference Implementation: `Document Generation_Validation Scripts/book_taxonomy.py`

---

## Tier Structure

```
ARCHITECTURE SPINE (Tier 1)
    ↓ cascades to
IMPLEMENTATION (Tier 2)
    ↓ cascades to
ENGINEERING PRACTICES (Tier 3)
```

---

## Tier 1: Architecture Spine Books

Foundational architectural patterns and principles.

| Book | Primary Focus | Relevance Weight | Cascades To |
|------|--------------|------------------|-------------|
| **Architecture Patterns with Python** | DDD, Event-Driven Architecture, Repository Pattern | 1.2 | • Building Python Microservices with FastAPI<br>• Python Architecture Patterns |
| **Building Microservices** | Microservices architecture, organizational patterns | 1.1 | • Microservices Up and Running<br>• Python Microservices Development |
| **Microservice Architecture** | Academic theory, formal design patterns | 1.0 | • Architecture Patterns with Python<br>• Python Architecture Patterns |
| **Python Architecture Patterns** | Python-specific architectural patterns | 1.1 | • Fluent Python 2nd<br>• Python Essential Reference 4th |

### Tier 1 Keyword Triggers

**Architecture Patterns with Python**:
- domain, aggregate, repository, unit of work, service layer
- event, message bus, dependency injection, adapter, port
- bounded context, entity, value object, architecture
- persistence, orm, database, transaction, testing
- hexagonal, clean architecture, domain-driven design

**Building Microservices**:
- microservice, service, distributed, resilience, scalability
- deployment, monitoring, observability, circuit breaker
- api gateway, service mesh, containerization, docker
- orchestration, communication, rest, grpc, messaging
- kafka, rabbitmq, fault tolerance, load balancing

**Microservice Architecture**:
- architecture, pattern, design, structure, component
- module, interface, abstraction, coupling, cohesion
- separation of concerns, single responsibility, dependency
- layered, modular, composition, decomposition

**Python Architecture Patterns**:
- pattern, architecture, design, mvc, mvvm, clean code
- solid, refactoring, testability, maintainability
- extensibility, plugin, framework, library, package
- structure, organization, best practices

---

## Tier 2: Implementation Books

Practical application of architectural concepts.

| Book | Primary Focus | Relevance Weight | Cascades To |
|------|--------------|------------------|-------------|
| **Building Python Microservices with FastAPI** | FastAPI framework, async Python, API development | 1.0 | • Microservice APIs Using Python Flask FastAPI<br>• Python Distilled |
| **Microservice APIs Using Python Flask FastAPI** | Comparative API frameworks (Flask, FastAPI) | 1.0 | • Python Cookbook 3rd<br>• Fluent Python 2nd |
| **Python Microservices Development** | Building microservices with Python | 1.0 | • Building Microservices<br>• Python Essential Reference 4th |
| **Microservices Up and Running** | Operational microservices patterns | 0.9 | • Building Microservices<br>• Python Microservices Development |

### Tier 2 Keyword Triggers

**Building Python Microservices with FastAPI**:
- fastapi, async, await, asyncio, api, rest, endpoint
- router, dependency, validation, pydantic, schema
- openapi, swagger, authentication, authorization, jwt
- middleware, cors, websocket, background tasks, testing

**Microservice APIs Using Python Flask FastAPI**:
- flask, fastapi, api, blueprint, route, decorator
- request, response, middleware, extension, plugin
- template, jinja, sqlalchemy, migration, testing
- deployment, wsgi, asgi, gunicorn, uvicorn

**Python Microservices Development**:
- microservice, service, distributed, communication, rpc
- messaging, queue, celery, redis, docker, kubernetes
- deployment, scaling, monitoring, logging, tracing
- debugging, performance, optimization, caching

**Microservices Up and Running**:
- operations, deployment, devops, ci/cd, pipeline
- container, orchestration, monitoring, alerting, logging
- metrics, observability, reliability, availability
- incident, postmortem, sre, kubernetes, helm

---

## Tier 3: Engineering Practices Books

Python language fundamentals and best practices.

| Book | Primary Focus | Relevance Weight | Cascades To |
|------|--------------|------------------|-------------|
| **Fluent Python 2nd** | Advanced Pythonic patterns, protocols, metaprogramming | 1.2 | • Python Distilled<br>• Python Essential Reference 4th |
| **Python Distilled** | Concise best practices, core concepts | 1.1 | • Python Essential Reference 4th<br>• Python Cookbook 3rd |
| **Python Cookbook 3rd** | Recipe-based practical solutions | 1.0 | • Fluent Python 2nd<br>• Python Distilled |
| **Python Essential Reference 4th** | Authoritative language reference | 1.0 | • Python Distilled<br>• Fluent Python 2nd |
| **Python Data Analysis 3rd** | Data analysis with pandas, NumPy | 0.8 | • Python Cookbook 3rd |
| **Learning Python Ed6** | Comprehensive Python tutorial (primary text) | 0.5 | • Python Distilled<br>• Fluent Python 2nd |

### Tier 3 Keyword Triggers

**Fluent Python 2nd**:
- pythonic, idiomatic, protocol, abc, metaclass, descriptor
- decorator, context manager, generator, iterator, coroutine
- async, await, type hint, annotation, special method
- `__init__`, `__call__`, `__enter__`, `__exit__`, property
- classmethod, staticmethod, dataclass, comprehension

**Python Distilled**:
- function, class, method, module, package, import
- exception, iterator, generator, decorator, property
- closure, lambda, comprehension, context manager, type
- object, reference, memory, garbage collection, threading
- multiprocessing, async, testing, debugging

**Python Cookbook 3rd**:
- data structure, algorithm, string, text, number, file
- io, iteration, function, class, metaprogramming, module
- network, web, concurrency, testing, debugging, c extension
- recipe, pattern, idiom, technique, best practice

**Python Essential Reference 4th**:
- reference, specification, syntax, semantics, built-in
- standard library, function, class, module, type, object
- operator, expression, statement, exception, iterator
- generator, decorator, descriptor, metaclass, gc
- threading, multiprocessing, io, network, sys

**Python Data Analysis 3rd**:
- pandas, numpy, dataframe, series, array, matrix
- data, analysis, statistics, visualization, matplotlib
- plotting, cleaning, wrangling, transformation, aggregation
- groupby, merge, join, pivot, reshape, time series
- missing data, io, csv, excel, sql, hdf5

**Learning Python Ed6** *(Primary Text - Lower Weight)*:
- tutorial, learning, beginner, introduction, fundamental
- basic, core, concept, syntax, type, function, class
- module, exception, iterator, generator, decorator
- comprehension, object, variable, operator, statement

---

## Cascading Logic

### How Cascading Works

1. **Concept Matching**: System analyzes SonarQube issue/chapter concepts
2. **Relevance Scoring**: Each book scores 0.0-1.0 based on keyword overlap
3. **Tier Priority**: Architecture → Implementation → Practices
4. **Cascade Depth**: Includes related books (typically depth=1)

### Example Cascade Chains

```
Architecture Patterns with Python
    └─> Building Python Microservices with FastAPI
            └─> Microservice APIs Using Python Flask FastAPI
                    └─> Python Cookbook 3rd
                            └─> Fluent Python 2nd
```

```
Building Microservices
    ├─> Microservices Up and Running
    │       └─> Python Microservices Development
    └─> Python Microservices Development
            └─> Python Essential Reference 4th
```

---

## Usage in TDD Workflow

### Step 1: Book Taxonomy Analysis

Match SonarQube rule to keyword triggers:

**Example: S1172 (Unused Parameters)**
- Keywords: `function`, `parameter`, `argument`, `interface`
- Matches: Python Distilled (function, interface)
- Tier: ENGINEERING_PRACTICES
- Cascades: Python Essential Reference 4th, Python Cookbook 3rd

### Step 2: Guidelines Cross-Reference

Load guidelines for recommended books:
1. Primary match (highest relevance score)
2. Cascaded books (related concepts)
3. Tier-appropriate books (Architecture if design, Practices if syntax)

### Step 3: Annotation

Reference specific chapters/pages from selected books:
```python
# Reference: Python Distilled, Ch. 5 - Function Definitions
# Reference: Python Essential Reference 4th, p. 89 - Parameter passing
def process_jobs(self, filters: dict) -> List[Job]:
    """Duck typing pattern - minimal required parameters."""
    return await self._repository.get_all(filters)
```

---

## Selection Algorithm Parameters

```python
get_recommended_books(
    concepts: Set[str],           # From chapter/issue analysis
    min_relevance: float = 0.3,   # Threshold (0.0-1.0)
    include_cascades: bool = True, # Add related books
    max_books: int = 15           # Maximum recommendations
)
```

### Typical Configurations

**Architectural Issues** (S3776 Cognitive Complexity):
- `min_relevance=0.4` (higher threshold)
- Focus on Tier 1 books
- Cascade depth=2

**Implementation Issues** (S1172 Unused Parameters):
- `min_relevance=0.3` (standard)
- Focus on Tier 3 books
- Cascade depth=1

**Language Feature Issues** (S1192 String Duplication):
- `min_relevance=0.2` (lower for broader match)
- Focus on Tier 3 books
- Cascade depth=1

---

## Book Registry

Total: **15 books** across 3 tiers

- **Tier 1 (Architecture Spine)**: 4 books
- **Tier 2 (Implementation)**: 4 books
- **Tier 3 (Engineering Practices)**: 6 books
- **Primary Text**: Learning Python Ed6 (0.5 weight - lower since it's being annotated)

---

## Integration Points

### With `interactive_llm_system_v3_hybrid_prompt.py`

```python
from book_taxonomy import get_recommended_books, BOOK_REGISTRY

# Get recommendations based on chapter concepts
recommended_books = get_recommended_books(
    concepts=chapter_concepts,
    min_relevance=0.3
)

# Load guidelines for each recommended book
for book_name in recommended_books:
    guidelines_file = f"PYTHON_GUIDELINES/{book_name}_GUIDELINES.md"
    # ... load and use
```

### With SonarQube Remediation

```python
# S1172: Unused parameters
issue_keywords = {"function", "parameter", "unused", "interface"}
books = get_recommended_books(issue_keywords, min_relevance=0.3)
# -> ["Python Distilled", "Python Essential Reference 4th", "Fluent Python 2nd"]
```

---

## Maintenance Notes

**Last Updated**: November 2025  
**Source**: `book_taxonomy.py` (506 lines)  
**Pattern**: Strategy + Template Method (GoF Design Patterns)  
**Architecture**: 3-tier cascading selection with relevance scoring

**To Update**:
1. Edit `book_taxonomy.py` BookRole definitions
2. Regenerate this markdown via `python book_taxonomy.py > taxonomy_output.txt`
3. Update cascading relationships if new books added
4. Adjust relevance weights based on real-world usage patterns
