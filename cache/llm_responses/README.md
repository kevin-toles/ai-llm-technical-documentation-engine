# LLM Response Cache Directory

This directory will be used by the new cache system (DOMAIN_AGNOSTIC Part 2).

**Purpose**: Cache expensive LLM API responses to avoid repeat /bin/zsh.60/chapter costs.

**Structure** (to be implemented):
```
cache/llm_responses/
├── phase1_{content_hash}.json  # Metadata analysis (~10K tokens)
└── phase2_{content_hash}.json  # Content enhancement (~50K tokens)
```

**TTL**: 30 days (configurable)

**See**: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md Part 2
