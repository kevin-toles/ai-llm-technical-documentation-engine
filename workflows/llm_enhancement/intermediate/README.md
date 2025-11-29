# Statistical Pre-Filter Intermediate Files

This directory stores temporary JSON files from statistical pre-filtering (DOMAIN_AGNOSTIC Part 2).

**Purpose**: Cache YAKE keyword extraction and TF-IDF similarity rankings to avoid re-computation.

**Structure** (to be implemented):
```
workflows/llm_enhancement/intermediate/
├── statistical_prefilter/
│   ├── chapter_1_candidates.json  # Ranked candidate chapters
│   ├── chapter_2_candidates.json
│   └── ...
└── .gitkeep
```

**TTL**: 7 days (cheap to regenerate but slow)

**Format**: See `StatisticalPrefilterOutput` in DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md

**See**: DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md Part 2 (JSON Interchange Format)
