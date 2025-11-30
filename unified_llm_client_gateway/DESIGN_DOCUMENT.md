# Unified LLM Client Gateway

## Design Document v0.1 (DRAFT)

**Status:** Under Discussion  
**Created:** 2025-11-30  
**Last Updated:** 2025-11-30

---

## 1. Overview

### 1.1 Vision

The Unified LLM Client Gateway is a reusable component that provides a single interface for interacting with multiple LLM providers. It is designed to be:

- **Embedded today** - Self-contained package within this repository
- **Extractable tomorrow** - Clean boundaries for moving to its own repository
- **Microservice-ready** - Architecture supports transition to HTTP/gRPC service

### 1.2 Problem Statement

Current challenges when working with multiple LLM providers:

1. **Fragmented APIs** - Each provider has different request/response formats
2. **Stateless calls** - No conversation history management, leading to repeated context in each call
3. **No parallelization** - Cannot easily fan-out requests to multiple providers
4. **Scattered resilience** - Retry logic, rate limiting handled ad-hoc in each project
5. **Token inefficiency** - Without conversation state, large prompts must be resent repeatedly

### 1.3 Goals

| Goal | Description |
|------|-------------|
| Unified Interface | Single API to call OpenAI, Anthropic, Google, DeepSeek |
| Conversation Management | Stateful sessions that maintain message history across calls |
| Parallel Execution | Fan-out same conversation to multiple providers simultaneously |
| Resilience | Centralized retry, rate-limit handling, circuit breakers |
| Token Efficiency | Send context once, ask follow-up questions without resending |
| Observability | Logging, metrics, token tracking (separate from observability_platform) |

---

## 2. Architecture

### 2.1 High-Level Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Unified LLM Client Gateway                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │   Gateway    │───▶│ Session Manager  │───▶│  Resilience   │  │
│  │  (Facade)    │    │ (Conversations)  │    │  (Retry/Rate) │  │
│  └──────────────┘    └──────────────────┘    └───────────────┘  │
│         │                     │                      │          │
│         ▼                     ▼                      ▼          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Provider Adapters                        ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       ││
│  │  │ Anthropic│ │  OpenAI  │ │  Google  │ │ DeepSeek │       ││
│  │  │ (Primary)│ │ (Primary)│ │          │ │          │       ││
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌──────────────┐    ┌──────────────────┐                       │
│  │    State     │    │   Observability  │                       │
│  │   Backend    │    │    (Internal)    │                       │
│  │ (Pluggable)  │    │                  │                       │
│  └──────────────┘    └──────────────────┘                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Responsibilities

#### Gateway (Facade)
- Entry point for all client interactions
- Routes requests to appropriate provider adapters
- Coordinates parallel execution across providers

#### Session Manager
- Creates and manages conversation sessions
- Maintains message history per session
- Supports multiple concurrent sessions

#### Resilience Layer
- Exponential backoff retry logic
- Per-provider rate limiting
- Circuit breaker pattern (future)
- Request queuing (future)

#### Provider Adapters
- Normalize provider-specific APIs to common interface
- Handle authentication per provider
- Translate requests/responses to common format

**Provider Priority:**
1. **Anthropic** (Primary) - Claude models
2. **OpenAI** (Primary) - GPT models  
3. **Google** - Gemini models
4. **DeepSeek** - DeepSeek models

#### State Backend
- Pluggable storage for conversation state
- **Phase 1:** In-memory (dict-based)
- **Phase 2:** Redis/Database (after extraction)

#### Observability (Internal)
- Separate from `observability_platform`
- Token usage tracking
- Request/response logging
- Latency metrics

---

## 3. Core Concepts

### 3.1 Conversation Session

A session represents a stateful conversation with an LLM:

```python
# Conceptual API (not final)
session = gateway.create_session(
    provider="anthropic",
    model="claude-sonnet-4-20250514",
    system_prompt="You are a helpful assistant..."
)

# First message - send context
response1 = session.send("Here is a large document: {data}")

# Follow-up - no need to resend context
response2 = session.send("Now answer question 1")
response3 = session.send("Now answer question 2")

# Get full history
history = session.get_messages()
```

### 3.2 Parallel Execution

Fan-out same conversation to multiple providers:

```python
# Conceptual API (not final)
results = gateway.parallel_execute(
    providers=["anthropic", "openai", "google", "deepseek"],
    messages=[
        {"role": "user", "content": "Here is data..."},
        {"role": "user", "content": "Evaluate this..."}
    ],
    # Each provider runs independently and in parallel
)

# results = {
#     "anthropic": {...response...},
#     "openai": {...response...},
#     "google": {...response...},
#     "deepseek": {...response...}
# }
```

### 3.3 Common Response Format

All providers return normalized responses:

```python
{
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514",
    "session_id": "sess_abc123",
    "message": {
        "role": "assistant",
        "content": "..."
    },
    "usage": {
        "input_tokens": 1500,
        "output_tokens": 500,
        "total_tokens": 2000
    },
    "latency_ms": 2340,
    "metadata": {
        "finish_reason": "stop",
        "request_id": "req_xyz789"
    }
}
```

---

## 4. Deployment Phases

### Phase 1: Embedded Package (Current Focus)

```
llm-document-enhancer/
├── unified_llm_client_gateway/
│   ├── __init__.py
│   ├── DESIGN_DOCUMENT.md
│   ├── README.md
│   ├── src/
│   │   ├── __init__.py
│   │   ├── gateway.py           # Main facade
│   │   ├── session.py           # Conversation session
│   │   ├── resilience.py        # Retry, rate limiting
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Abstract provider
│   │   │   ├── anthropic.py
│   │   │   ├── openai.py
│   │   │   ├── google.py
│   │   │   └── deepseek.py
│   │   └── state/
│   │       ├── __init__.py
│   │       ├── base.py          # Abstract state backend
│   │       └── memory.py        # In-memory implementation
│   ├── config/
│   │   └── settings.py
│   └── tests/
│       └── ...
```

**Usage:**
```python
from unified_llm_client_gateway import Gateway

gateway = Gateway()
session = gateway.create_session(provider="anthropic", model="claude-sonnet-4-20250514")
```

### Phase 2: Standalone Repository

- Extract to `kevin-toles/unified-llm-client-gateway`
- Add `pyproject.toml` for pip installation
- Can still be used as library

### Phase 3: Microservice

- Add FastAPI layer wrapping the Gateway class
- HTTP/gRPC endpoints
- Docker containerization
- Deploy locally or to cloud (similar to TPM repo pattern)

```
POST /sessions
POST /sessions/{session_id}/messages
GET  /sessions/{session_id}/history
POST /parallel
DELETE /sessions/{session_id}
```

---

## 5. Design Decisions (To Discuss)

### 5.1 Open Questions

| Question | Options | Current Thinking |
|----------|---------|------------------|
| **Async vs Sync** | Sync-first, async-first, or both? | TBD |
| **Streaming** | Support streaming responses? | Not in Phase 1 |
| **Error handling** | Exceptions vs Result objects? | TBD |
| **Config format** | .env, YAML, or Python config? | .env for consistency |
| **Dependency injection** | How to swap providers/backends? | Constructor injection |

### 5.2 Decisions Made

| Decision | Rationale |
|----------|-----------|
| Separate from observability_platform | Different concerns, independent extraction timelines |
| Anthropic & OpenAI as primary | Most commonly used, best supported |
| In-memory state first | Simplicity; Redis can be added later |
| Provider-agnostic session interface | Allows switching providers without client code changes |

---

## 6. Integration with Current Project

### 6.1 Replacing llm_evaluation.py Calls

**Before (current):**
```python
# Each call is independent, ~18K tokens every time
result1 = call_openai(config, massive_prompt_with_all_data)
result2 = call_anthropic(config, massive_prompt_with_all_data)
```

**After (with gateway):**
```python
# Parallel conversation-based evaluation
results = gateway.parallel_conversation(
    providers=["anthropic", "openai", "google", "deepseek"],
    conversation=[
        {"role": "user", "content": context_data},  # ~18K tokens, sent once per provider
        {"role": "user", "content": "Answer Q1-Q6"},  # ~500 tokens
        {"role": "user", "content": "Answer Q7-Q12"}, # ~500 tokens
        {"role": "user", "content": "Answer Q13-Q18"}, # ~500 tokens
        {"role": "user", "content": "Final recommendation"}, # ~500 tokens
    ]
)
# Total: ~20K tokens per provider instead of ~73K
# Plus: All 4 providers run in parallel
```

### 6.2 Token Savings Estimate

| Approach | Tokens per Provider | Total (10 models) |
|----------|---------------------|-------------------|
| Current (single call) | ~18K | ~180K |
| Current chunked (broken) | ~51K | ~510K |
| Gateway conversation | ~20K | ~200K |

**Benefit:** Gateway matches single-call token usage but enables follow-up questions without resending context.

---

## 7. Next Steps

1. [ ] Finalize design decisions (Section 5.1)
2. [ ] Define provider adapter interface
3. [ ] Implement core Gateway and Session classes
4. [ ] Implement Anthropic adapter (primary)
5. [ ] Implement OpenAI adapter (primary)
6. [ ] Add resilience layer
7. [ ] Integrate with llm_evaluation.py
8. [ ] Add remaining providers (Google, DeepSeek)

---

## 8. Discussion Notes

*Space for ongoing discussion points...*

### 2025-11-30

- Initial design document created
- User vision: Extractable package → standalone repo → microservice
- Keep separate from observability_platform
- All providers, with Anthropic and OpenAI as primary
- Full scope: conversation management + parallel execution + resilience

---

*This is a living document. Updates will be made as design discussions continue.*
