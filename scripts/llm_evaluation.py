#!/usr/bin/env python3
"""
LLM Evaluation Script for Keyword Extraction Quality
=====================================================

Sends extraction outputs to multiple LLMs for quality evaluation.
Aggregates and compares assessments across models.

API Keys are loaded from environment variables (via .env file):
    - DEEPSEEK_API_KEY: DeepSeek API key
    - GEMINI_API_KEY: Google Gemini API key  
    - ANTHROPIC_API_KEY: Anthropic Claude API key
    - OPENAI_API_KEY: OpenAI API key

Usage:
    python llm_evaluation.py --output-dir outputs/extraction_test_current_*
    python llm_evaluation.py --compare baseline current
    python llm_evaluation.py --models deepseek gemini claude
    python llm_evaluation.py --fetch-models all
    python llm_evaluation.py --test-connection
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

# Rate limiting configuration
API_CALL_DELAY_SECONDS = 3  # Delay between API calls to avoid rate limits
API_TIMEOUT_SECONDS = 300   # 5 minute timeout for large prompts with complex analysis

# Retry configuration for rate limits
MAX_RETRIES = 3              # Maximum number of retry attempts
INITIAL_RETRY_DELAY = 10     # Initial delay in seconds before first retry
MAX_RETRY_DELAY = 120        # Maximum delay between retries (2 minutes)
RETRY_BACKOFF_FACTOR = 2     # Exponential backoff multiplier

# String constants to avoid duplication (SonarQube S1192)
CONTENT_TYPE_JSON = "application/json"
MODEL_GEMINI_FLASH = "gemini-2.5-flash"
MODEL_CLAUDE_OPUS = "claude-opus-4.5"
MODEL_CLAUDE_SONNET = "claude-sonnet-4.5"
MODEL_GPT = "gpt-5.1"
JSON_CODE_BLOCK = "```json"

# API URL constants (S1192 - duplicated 4 times)
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"

# Evaluation system prompt (S1192 - duplicated 3+ times)
EVALUATION_SYSTEM_PROMPT = (
    "You are an expert at evaluating NLP extraction quality. "
    "You MUST respond with valid JSON only. Do not include markdown code blocks, "
    "explanations, or any text before or after the JSON object. "
    "Start your response with { and end with }."
)

# Error message constants (S1192 - duplicated multiple times)
ERROR_FAILED_TO_PARSE_JSON = "Failed to parse JSON"
ERROR_RATE_LIMITED = "Rate limited (429) - too many requests"
ERROR_AUTH_FAILED = "Authentication failed (401) - check API key"

# Keyword constants for test data (S1192 - duplicated 4 times)
KEYWORD_STATIC_ANALYSIS = "static analysis"

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Optional: Google GenerativeAI SDK for Gemini
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@dataclass
class LLMConfig:
    """Configuration for an LLM provider."""
    name: str
    base_url: str
    api_key: str | None
    model: str
    headers: dict[str, str]


# =============================================================================
# HELPER FUNCTIONS FOR COGNITIVE COMPLEXITY REDUCTION (S3776)
# Pattern: CODING_PATTERNS_ANALYSIS.md Category 2 - Extract Method
# =============================================================================


def _handle_http_error(e: httpx.HTTPStatusError) -> dict[str, Any]:
    """
    Handle HTTP errors for API calls with consistent error messages.
    
    Extracts error handling from call_deepseek, call_gemini, etc. to reduce complexity.
    """
    if e.response.status_code == 429:
        return {"error": ERROR_RATE_LIMITED}
    elif e.response.status_code == 401:
        return {"error": ERROR_AUTH_FAILED}
    else:
        return {"error": f"HTTP {e.response.status_code}: {str(e)[:100]}"}


def _save_debug_response(content: str, provider: str) -> Path:
    """
    Save debug response to file for troubleshooting failed JSON parsing.
    
    Returns path to the debug file.
    """
    debug_file = PROJECT_ROOT / "outputs" / "evaluation" / f"debug_{provider}_{datetime.now().strftime('%H%M%S')}.txt"
    debug_file.parent.mkdir(parents=True, exist_ok=True)
    with open(debug_file, "w") as f:
        f.write(content)
    return debug_file


def _call_gemini_sdk(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """
    Call Gemini API using the Python SDK.
    
    Extracted from call_gemini() to reduce cognitive complexity.
    """
    if not GENAI_AVAILABLE or genai is None:
        return {"error": "Gemini SDK not available"}
    
    try:
        genai.configure(api_key=config.api_key)
        model = genai.GenerativeModel(config.model)
        
        full_prompt = f"You are an expert at evaluating NLP extraction quality. Always respond with valid JSON only, no markdown code blocks.\n\n{prompt}"
        response = model.generate_content(full_prompt)
        content = response.text
        
        # Use robust JSON extraction
        parsed = extract_json_from_response(content)
        if parsed is not None:
            return parsed
        
        # Save debug file
        debug_file = _save_debug_response(content, "gemini")
        return {"error": ERROR_FAILED_TO_PARSE_JSON, "raw_response": content[:1000], "debug_file": str(debug_file)}
            
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return {"error": "Rate limited (429) - quota exceeded"}
        elif "401" in error_msg or "invalid" in error_msg.lower():
            return {"error": "Authentication failed - check API key"}
        return {"error": f"Gemini SDK error: {error_msg[:100]}"}


def _call_gemini_rest(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """
    Call Gemini API using REST API fallback.
    
    Extracted from call_gemini() to reduce cognitive complexity.
    """
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are an expert at evaluating NLP extraction quality. Always respond with valid JSON only, no markdown code blocks.\n\n{prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 4000
        }
    }
    
    try:
        with httpx.Client(timeout=API_TIMEOUT_SECONDS) as client:
            response = client.post(
                config.base_url,
                headers=config.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract content from Gemini response
            content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            if not content:
                return {"error": "Empty response from Gemini", "raw_response": str(result)[:500]}
            
            # Parse JSON from response
            try:
                if JSON_CODE_BLOCK in content:
                    content = content.split(JSON_CODE_BLOCK)[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return {"error": ERROR_FAILED_TO_PARSE_JSON, "raw_response": content[:500]}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s"}
    except httpx.HTTPStatusError as e:
        return _handle_http_error(e)
    except Exception as e:
        return {"error": f"Gemini error: {str(e)[:100]}"}


def _calculate_retry_delay(attempt: int, error_msg: str) -> float:
    """
    Calculate retry delay with exponential backoff.
    
    Extracted from call_llm_with_retry() to reduce cognitive complexity.
    
    Args:
        attempt: Current retry attempt (0-indexed)
        error_msg: Error message that may contain retry-after header info
    
    Returns:
        Delay in seconds before next retry
    """
    import re
    
    # Base delay with exponential backoff
    delay = min(
        INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** attempt),
        MAX_RETRY_DELAY
    )
    
    # Extract retry-after header if available
    if "retry after" in error_msg.lower():
        match = re.search(r'retry after (\d+)', error_msg.lower())
        if match:
            suggested_delay = int(match.group(1))
            delay = max(delay, suggested_delay)
    
    return delay


def _load_profile_aggregates(eval_dir: Path, profiles: list[str], suffixes: dict[str, str]) -> dict[str, Any]:
    """
    Load aggregate files for all profiles.
    
    Extracted from run_chunked_comparative_evaluation() to reduce complexity.
    
    Returns:
        Dictionary of profile name -> aggregate data
    """
    aggregates = {}
    
    print("\n📂 Loading aggregates...")
    for profile in profiles:
        suffix = suffixes[profile]
        agg_file = eval_dir / f"aggregate_{suffix}.json"
        
        if agg_file.exists():
            with open(agg_file) as f:
                aggregates[profile] = json.load(f)
            print(f"  ✅ {suffix}: Loaded")
        else:
            print(f"  ❌ {suffix}: Not found")
    
    return aggregates


def _calculate_consensus(evaluations: dict[str, Any], models_used: list[str]) -> dict[str, Any]:
    """
    Calculate consensus recommendation from model evaluations.
    
    Extracted from run_chunked_comparative_evaluation() to reduce complexity.
    
    Returns:
        Consensus dictionary with best_for_production, votes, agreement_ratio
    """
    recommendations = {}
    for model in models_used:
        eval_result = evaluations[model]
        rec = eval_result.get("recommendation", {})
        best = rec.get("best_for_production", "")
        if best:
            recommendations[best.lower()] = recommendations.get(best.lower(), 0) + 1
    
    if not recommendations:
        return {}
    
    consensus = max(recommendations, key=recommendations.get)
    return {
        "best_for_production": consensus,
        "votes": recommendations,
        "agreement_ratio": recommendations[consensus] / len(models_used)
    }


def _test_deepseek_connection(_api_key: str) -> dict[str, Any]:
    """
    Test DeepSeek API connection.
    
    Extracted from test_api_connections() to reduce complexity.
    
    Args:
        _api_key: API key (unused - models fetched via environment variable).
    """
    print("\n  DeepSeek:")
    try:
        models = list_deepseek_models()
        if models and "error" not in models[0]:
            for m in models:
                if "id" in m:
                    print(f"    ✅ Model: {m['id']}")
                if "note" in m:
                    print(f"    ℹ️  {m['note']}")
            return {"status": "connected", "models": models}
        else:
            print(f"    ⚠️  {models[0].get('error', 'Unknown error')}")
            return {"status": "error", "error": models[0].get("error", "Unknown")}
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return {"status": "error", "error": str(e)}


def _test_gemini_connection(_api_key: str) -> dict[str, Any]:
    """
    Test Gemini API connection.
    
    Extracted from test_api_connections() to reduce complexity.
    
    Args:
        _api_key: API key (unused - models fetched via environment variable).
    """
    print("\n  Gemini:")
    try:
        models = list_gemini_models()
        if models and "error" not in models[0]:
            print(f"    ✅ Connected - {len(models)} models available")
            for m in models[:3]:
                name = m.get("name", m.get("display_name", "Unknown"))
                print(f"       - {name}")
            if len(models) > 3:
                print(f"       ... and {len(models) - 3} more")
            return {"status": "connected", "model_count": len(models)}
        else:
            print(f"    ⚠️  {models[0].get('error', 'Unknown error')}")
            return {"status": "error", "error": models[0].get("error", "Unknown")}
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return {"status": "error", "error": str(e)}


def _test_anthropic_connection(api_key: str) -> dict[str, Any]:
    """
    Test Anthropic (Claude) API connection.
    
    Extracted from test_api_connections() to reduce complexity.
    """
    print("\n  Anthropic (Claude):")
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                "https://api.anthropic.com/v1/models",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01"
                }
            )
            if response.status_code == 200:
                print("    ✅ Connected")
                return {"status": "connected"}
            else:
                print(f"    ⚠️  HTTP {response.status_code}")
                return {"status": "error", "code": response.status_code}
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return {"status": "error", "error": str(e)}


def _test_openai_connection(api_key: str) -> dict[str, Any]:
    """
    Test OpenAI API connection.
    
    Extracted from test_api_connections() to reduce complexity.
    """
    print("\n  OpenAI:")
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            if response.status_code == 200:
                data = response.json()
                model_count = len(data.get("data", []))
                print(f"    ✅ Connected - {model_count} models available")
                return {"status": "connected", "model_count": model_count}
            else:
                print(f"    ⚠️  HTTP {response.status_code}")
                return {"status": "error", "code": response.status_code}
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return {"status": "error", "error": str(e)}


def _process_evaluation_chunk(
    chunk_num: int, 
    chunk_questions: list[tuple], 
    aggregates: dict[str, Any],
    model: str,
    config: LLMConfig
) -> dict[str, Any]:
    """
    Process a single evaluation chunk.
    
    Extracted from run_chunked_evaluation() to reduce complexity.
    """
    print(f"      📦 Chunk {chunk_num}/3 (Q{chunk_questions[0][0][-1]}-Q{chunk_questions[-1][0][-2:]})...", end=" ", flush=True)
    
    prompt = create_chunked_prompt(aggregates, chunk_questions, chunk_num)
    
    # Add delay between chunks
    if chunk_num > 1:
        time.sleep(API_CALL_DELAY_SECONDS)
    
    result = call_llm_with_retry(model, config, prompt)
    
    if "error" in result:
        print(f"❌ {result['error'][:40]}")
    else:
        print("✅")
    
    return result


def get_llm_configs() -> dict[str, LLMConfig]:
    """
    Get LLM configurations from environment variables.
    
    API keys are loaded from environment variables (set in .env file):
        - DEEPSEEK_API_KEY
        - GEMINI_API_KEY
        - ANTHROPIC_API_KEY
        - OPENAI_API_KEY
    
    Configured Models:
        - Claude Opus 4.5, Claude Sonnet 4.5
        - GPT-5.1, GPT-5, GPT-5 Mini, GPT-5 Nano
        - Gemini 3 Pro, Gemini 2.5 Flash
        - DeepSeek V3, DeepSeek R1
    """
    configs = {}
    
    # DeepSeek V3 and R1 (Open-Source)
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if deepseek_key:
        configs["deepseek-v3"] = LLMConfig(
            name="DeepSeek V3",
            base_url="https://api.deepseek.com/chat/completions",
            api_key=deepseek_key,
            model="deepseek-chat",  # V3 is the current deepseek-chat
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "Authorization": f"Bearer {deepseek_key}"
            }
        )
        configs["deepseek-r1"] = LLMConfig(
            name="DeepSeek R1",
            base_url="https://api.deepseek.com/chat/completions",
            api_key=deepseek_key,
            model="deepseek-reasoner",  # R1 is deepseek-reasoner
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "Authorization": f"Bearer {deepseek_key}"
            }
        )
    
    # Gemini 3 Pro and Gemini 2.5 Flash (Gemini 3 Flash not yet available)
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        configs["gemini-3-pro"] = LLMConfig(
            name="Gemini 3 Pro",
            base_url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent?key={gemini_key}",
            api_key=gemini_key,
            model="gemini-3-pro-preview",
            headers={
                "Content-Type": CONTENT_TYPE_JSON
            }
        )
        configs[MODEL_GEMINI_FLASH] = LLMConfig(
            name="Gemini 2.5 Flash",
            base_url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}",
            api_key=gemini_key,
            model=MODEL_GEMINI_FLASH,
            headers={
                "Content-Type": CONTENT_TYPE_JSON
            }
        )
    
    # Claude Opus 4.5 and Claude Sonnet 4.5
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if anthropic_key:
        configs[MODEL_CLAUDE_OPUS] = LLMConfig(
            name="Claude Opus 4.5",
            base_url="https://api.anthropic.com/v1/messages",
            api_key=anthropic_key,
            model="claude-opus-4-5-20251101",
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01"
            }
        )
        configs[MODEL_CLAUDE_SONNET] = LLMConfig(
            name="Claude Sonnet 4.5",
            base_url="https://api.anthropic.com/v1/messages",
            api_key=anthropic_key,
            model="claude-sonnet-4-5-20250929",
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01"
            }
        )
    
    # OpenAI GPT-5.1, GPT-5, GPT-5-mini, GPT-5-nano
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_key:
        configs[MODEL_GPT] = LLMConfig(
            name="GPT-5.1",
            base_url=OPENAI_CHAT_COMPLETIONS_URL,
            api_key=openai_key,
            model=MODEL_GPT,
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "Authorization": f"Bearer {openai_key}"
            }
        )
        configs["gpt-5"] = LLMConfig(
            name="GPT-5",
            base_url=OPENAI_CHAT_COMPLETIONS_URL,
            api_key=openai_key,
            model="gpt-5",
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "Authorization": f"Bearer {openai_key}"
            }
        )
        configs["gpt-5-mini"] = LLMConfig(
            name="GPT-5 Mini",
            base_url=OPENAI_CHAT_COMPLETIONS_URL,
            api_key=openai_key,
            model="gpt-5-mini",
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "Authorization": f"Bearer {openai_key}"
            }
        )
        configs["gpt-5-nano"] = LLMConfig(
            name="GPT-5 Nano",
            base_url=OPENAI_CHAT_COMPLETIONS_URL,
            api_key=openai_key,
            model="gpt-5-nano",
            headers={
                "Content-Type": CONTENT_TYPE_JSON,
                "Authorization": f"Bearer {openai_key}"
            }
        )
    
    return configs


def create_evaluation_prompt(extraction_data: dict[str, Any], context: str = "") -> str:
    """Create the evaluation prompt for LLMs."""
    
    # Extract key data
    keywords = extraction_data.get("keywords", [])[:30]
    concepts = extraction_data.get("concepts", [])[:20]
    related_chapters = extraction_data.get("related_chapters", [])[:10]
    
    prompt = f"""You are evaluating the quality of automated keyword extraction for a technical book chapter.

## Context
{context}

## Extracted Data

### Keywords (first 30):
{json.dumps(keywords, indent=2)}

### Key Concepts (first 20):
{json.dumps(concepts, indent=2)}

### Related Chapters (first 10):
{json.dumps(related_chapters, indent=2)}

## Evaluation Criteria

Please evaluate on a scale of 1-10 for each criterion:

1. **Keyword Quality** (1-10): Are keywords relevant, specific, and diverse? Do they avoid redundant variants (e.g., "model" vs "models")?

2. **Concept Coverage** (1-10): Do the concepts capture the main themes of the chapter? Are they appropriately abstract?

3. **Navigation Utility** (1-10): Would these keywords and related chapters help a reader navigate the book effectively?

4. **Deduplication Quality** (1-10): Are there redundant or near-duplicate terms? Rate higher if terms are unique and diverse.

5. **Cross-Reference Value** (1-10): Do the related chapters make sense? Would a reader find value in following these connections?

## Response Format

Respond with JSON only:
```json
{{
  "scores": {{
    "keyword_quality": <1-10>,
    "concept_coverage": <1-10>,
    "navigation_utility": <1-10>,
    "deduplication_quality": <1-10>,
    "cross_reference_value": <1-10>
  }},
  "overall_score": <1-10>,
  "strengths": ["<strength 1>", "<strength 2>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>"],
  "specific_issues": ["<issue 1>", "<issue 2>"],
  "recommendations": ["<recommendation 1>", "<recommendation 2>"]
}}
```
"""
    return prompt


def call_deepseek(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """
    Call DeepSeek API.
    
    API endpoint: https://api.deepseek.com/chat/completions
    Model: deepseek-chat (V3) or deepseek-reasoner (R1)
    
    Refactored per S3776 to use helper functions for error handling.
    """
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 8192,  # DeepSeek max is 8192
        "stream": False  # Non-stream mode per docs
    }
    
    try:
        with httpx.Client(timeout=API_TIMEOUT_SECONDS) as client:
            response = client.post(
                config.base_url,
                headers=config.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Use robust JSON extraction
            parsed = extract_json_from_response(content)
            if parsed is not None:
                return parsed
            
            # Save debug file using helper
            debug_file = _save_debug_response(content, "deepseek")
            return {"error": ERROR_FAILED_TO_PARSE_JSON, "raw_response": content[:1000], "debug_file": str(debug_file)}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s - model may need more time"}
    except httpx.HTTPStatusError as e:
        return _handle_http_error(e)
    except Exception as e:
        return {"error": f"DeepSeek error: {str(e)[:100]}"}


def call_gemini(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """
    Call Gemini API using the Python SDK if available, otherwise REST API.
    
    SDK: google-generativeai
    Model: gemini-3-pro-preview or gemini-2.5-flash
    
    Refactored per S3776 to delegate to helper functions.
    """
    # Try SDK first (preferred method)
    if GENAI_AVAILABLE and genai is not None:
        return _call_gemini_sdk(config, prompt)
    
    # Fallback to REST API
    return _call_gemini_rest(config, prompt)


def _try_direct_json_parse(content: str) -> dict[str, Any] | None:
    """
    Strategy 1: Try direct JSON parse.
    
    Extracted from extract_json_from_response() to reduce complexity (S3776).
    """
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def _try_extract_from_json_block(content: str) -> dict[str, Any] | None:
    """
    Strategy 2: Extract from ```json ... ``` blocks.
    
    Extracted from extract_json_from_response() to reduce complexity (S3776).
    """
    if JSON_CODE_BLOCK not in content:
        return None
    try:
        json_part = content.split(JSON_CODE_BLOCK)[1].split("```")[0]
        return json.loads(json_part.strip())
    except (json.JSONDecodeError, IndexError):
        return None


def _try_extract_from_code_block(content: str) -> dict[str, Any] | None:
    """
    Strategy 3: Extract from ``` ... ``` blocks.
    
    Extracted from extract_json_from_response() to reduce complexity (S3776).
    """
    if "```" not in content:
        return None
    try:
        json_part = content.split("```")[1].split("```")[0]
        return json.loads(json_part.strip())
    except (json.JSONDecodeError, IndexError):
        return None


def _try_extract_by_braces(content: str) -> dict[str, Any] | None:
    """
    Strategy 4: Find JSON object by matching braces.
    
    Extracted from extract_json_from_response() to reduce complexity (S3776).
    """
    start_idx = content.find("{")
    if start_idx == -1:
        return None
    
    # Find matching closing brace
    brace_count = 0
    end_idx = start_idx
    for i, char in enumerate(content[start_idx:], start_idx):
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    if end_idx <= start_idx:
        return None
    
    try:
        return json.loads(content[start_idx:end_idx])
    except json.JSONDecodeError:
        return None


def extract_json_from_response(content: str) -> dict[str, Any] | None:
    """
    Extract JSON from LLM response, handling various formats.
    
    Tries multiple strategies in order:
    1. Direct JSON parse
    2. Extract from ```json ... ``` blocks
    3. Extract from ``` ... ``` blocks
    4. Find JSON object boundaries { ... }
    """
    content = content.strip()
    
    # Try each strategy in order until one succeeds
    strategies = [
        _try_direct_json_parse,
        _try_extract_from_json_block,
        _try_extract_from_code_block,
        _try_extract_by_braces,
    ]
    
    for strategy in strategies:
        result = strategy(content)
        if result is not None:
            return result
    
    return None


def call_claude(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """Call Claude API (Opus 4.5 or Sonnet 4.5)."""
    payload = {
        "model": config.model,
        "max_tokens": 16000,  # Increased for complex evaluation response
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "system": EVALUATION_SYSTEM_PROMPT
    }
    
    try:
        with httpx.Client(timeout=API_TIMEOUT_SECONDS) as client:
            response = client.post(
                config.base_url,
                headers=config.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            content = result["content"][0]["text"]
            
            # Try robust JSON extraction
            parsed = extract_json_from_response(content)
            if parsed is not None:
                return parsed
            
            # Save raw response for debugging
            debug_file = PROJECT_ROOT / "outputs" / "evaluation" / f"debug_claude_{datetime.now().strftime('%H%M%S')}.txt"
            debug_file.parent.mkdir(parents=True, exist_ok=True)
            with open(debug_file, "w") as f:
                f.write(f"Model: {config.model}\n")
                f.write(f"Response length: {len(content)}\n")
                f.write("="*80 + "\n")
                f.write(content)
            
            return {"error": ERROR_FAILED_TO_PARSE_JSON, "raw_response": content[:1000], "debug_file": str(debug_file)}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s"}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            return {"error": ERROR_RATE_LIMITED}
        elif e.response.status_code == 401:
            return {"error": ERROR_AUTH_FAILED}
        elif e.response.status_code == 529:
            return {"error": "API overloaded (529) - try again later"}
        else:
            return {"error": f"HTTP {e.response.status_code}: {str(e)[:100]}"}
    except Exception as e:
        return {"error": f"Claude error: {str(e)[:100]}"}


def call_openai(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """Call OpenAI API (GPT-5.1, GPT-5, gpt-5-mini, gpt-5-nano)."""
    # GPT-5.x models don't support temperature parameter and use max_completion_tokens
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "max_completion_tokens": 32000  # GPT-5.x uses max_completion_tokens, not max_tokens
    }
    
    try:
        with httpx.Client(timeout=API_TIMEOUT_SECONDS) as client:
            response = client.post(
                config.base_url,
                headers=config.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Use robust JSON extraction
            parsed = extract_json_from_response(content)
            if parsed is not None:
                return parsed
            
            # Save debug file
            debug_file = PROJECT_ROOT / "outputs" / "evaluation" / f"debug_openai_{datetime.now().strftime('%H%M%S')}.txt"
            debug_file.parent.mkdir(parents=True, exist_ok=True)
            with open(debug_file, "w") as f:
                f.write(content)
            return {"error": ERROR_FAILED_TO_PARSE_JSON, "raw_response": content[:1000], "debug_file": str(debug_file)}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s"}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            # Extract retry-after if available
            retry_after = e.response.headers.get("retry-after", "unknown")
            return {"error": f"Rate limited (429) - retry after {retry_after}s"}
        elif e.response.status_code == 401:
            return {"error": ERROR_AUTH_FAILED}
        elif e.response.status_code == 503:
            return {"error": "Service unavailable (503) - try again later"}
        else:
            return {"error": f"HTTP {e.response.status_code}: {str(e)[:100]}"}
    except Exception as e:
        return {"error": f"OpenAI error: {str(e)[:100]}"}


def evaluate_with_llm(llm_name: str, extraction_data: dict[str, Any], context: str = "") -> dict[str, Any]:
    """Evaluate extraction output with a specific LLM."""
    configs = get_llm_configs()
    
    if llm_name not in configs:
        available = list(configs.keys())
        return {"error": f"LLM '{llm_name}' not configured. Available: {available}"}
    
    config = configs[llm_name]
    prompt = create_evaluation_prompt(extraction_data, context)
    
    print(f"  🤖 Calling {config.name}...")
    
    # Route to appropriate API handler based on config key
    if llm_name.startswith("deepseek"):
        return call_deepseek(config, prompt)
    elif llm_name.startswith("gemini"):
        return call_gemini(config, prompt)
    elif llm_name.startswith("claude"):
        return call_claude(config, prompt)
    elif llm_name.startswith("gpt"):
        return call_openai(config, prompt)
    else:
        return {"error": f"No handler for {llm_name}"}


def load_extraction_output(output_path: Path) -> dict[str, Any]:
    """Load extraction output from a directory or file."""
    if output_path.is_file():
        with open(output_path) as f:
            return json.load(f)
    
    # Look for enriched metadata files
    patterns = ["*_enriched.json", "*_LLM_ENHANCED.json", "*.json"]
    
    for pattern in patterns:
        files = list(output_path.glob(pattern))
        if files:
            # Use most recent
            latest = max(files, key=lambda p: p.stat().st_mtime)
            print(f"  📂 Loading: {latest.name}")
            with open(latest) as f:
                return json.load(f)
    
    return {"error": f"No JSON files found in {output_path}"}


def run_evaluation(output_path: str, models: list[str] | None = None) -> dict[str, Any]:
    """Run evaluation on extraction output with specified models."""
    path = Path(output_path)
    
    if not path.exists():
        # Try to find matching directory
        outputs_dir = PROJECT_ROOT / "outputs"
        matches = list(outputs_dir.glob(output_path.replace("*", "**")))
        if matches:
            path = max(matches, key=lambda p: p.stat().st_mtime)
        else:
            return {"error": f"Path not found: {output_path}"}
    
    print(f"\n📊 Loading extraction output: {path}")
    extraction_data = load_extraction_output(path)
    
    if "error" in extraction_data:
        return extraction_data
    
    # Default models
    if models is None:
        models = ["deepseek", "gemini"]  # Default to available models
    
    # Get context from extraction data
    context = f"Book: {extraction_data.get('book_title', 'Unknown')}\n"
    context += f"Chapter: {extraction_data.get('chapter_title', 'Unknown')}"
    
    # Run evaluations
    results = {
        "source_path": str(path),
        "evaluation_date": datetime.now().isoformat(),
        "models_used": models,
        "evaluations": {}
    }
    
    print("\n🔍 Running LLM evaluations...")
    
    for model in models:
        result = evaluate_with_llm(model, extraction_data, context)
        results["evaluations"][model] = result
        
        if "error" not in result:
            score = result.get("overall_score", "N/A")
            print(f"     {model}: Overall score = {score}/10")
        else:
            print(f"     {model}: Error - {result.get('error', 'Unknown')[:50]}")
    
    # Calculate aggregate if we have valid scores
    valid_scores = []
    for model, eval_result in results["evaluations"].items():
        if "overall_score" in eval_result:
            valid_scores.append(eval_result["overall_score"])
    
    if valid_scores:
        results["aggregate"] = {
            "average_score": sum(valid_scores) / len(valid_scores),
            "min_score": min(valid_scores),
            "max_score": max(valid_scores),
            "models_responded": len(valid_scores)
        }
        print(f"\n📈 Aggregate: {results['aggregate']['average_score']:.1f}/10 average")
    
    # Save results
    output_file = PROJECT_ROOT / "outputs" / f"llm_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Results saved: {output_file}")
    
    return results


def compare_profiles(profile1: str, profile2: str, models: list[str] | None = None) -> dict[str, Any]:
    """Compare two extraction profiles using LLM evaluation."""
    outputs_dir = PROJECT_ROOT / "outputs"
    
    # Find outputs for each profile
    def find_output(profile: str) -> Path | None:
        matches = list(outputs_dir.glob(f"extraction_test_{profile}_*"))
        if matches:
            return max(matches, key=lambda p: p.stat().st_mtime)
        return None
    
    out1 = find_output(profile1)
    out2 = find_output(profile2)
    
    if not out1 or not out2:
        missing = []
        if not out1:
            missing.append(profile1)
        if not out2:
            missing.append(profile2)
        return {"error": f"Missing outputs for profiles: {missing}"}
    
    print(f"\n🔄 Comparing profiles: {profile1} vs {profile2}")
    
    # Evaluate each
    results1 = run_evaluation(str(out1), models)
    results2 = run_evaluation(str(out2), models)
    
    comparison = {
        "profile1": profile1,
        "profile2": profile2,
        "results1": results1,
        "results2": results2,
        "comparison_date": datetime.now().isoformat()
    }
    
    # Calculate winner
    if "aggregate" in results1 and "aggregate" in results2:
        score1 = results1["aggregate"]["average_score"]
        score2 = results2["aggregate"]["average_score"]
        
        comparison["winner"] = profile1 if score1 > score2 else profile2
        comparison["score_difference"] = abs(score1 - score2)
        
        print(f"\n🏆 Winner: {comparison['winner']} (by {comparison['score_difference']:.1f} points)")
    
    return comparison


def _extract_terms_from_items(items: list, term_key: str) -> list[str]:
    """
    Extract term strings from a list of dict or string items.
    
    Extracted from extract_evaluation_summary() to reduce complexity (S3776).
    
    Args:
        items: List of dicts or strings containing terms.
        term_key: Key to extract from dict items (e.g., "term", "concept").
        
    Returns:
        List of extracted term strings.
    """
    terms = []
    for item in items:
        if isinstance(item, dict):
            terms.append(item.get(term_key, item.get("keyword", "")))
        else:
            terms.append(str(item))
    return terms


def _create_chapter_summary(ch: dict[str, Any]) -> dict[str, Any]:
    """
    Create a summary dict for a single chapter.
    
    Extracted from extract_evaluation_summary() to reduce complexity (S3776).
    """
    ch_keywords = ch.get("keywords", [])
    ch_concepts = ch.get("concepts", [])
    ch_related = ch.get("related_chapters", [])
    
    return {
        "chapter": ch.get("chapter_number", ch.get("number", 0)),
        "title": ch.get("title", ""),
        "keywords_count": len(ch_keywords),
        "concepts_count": len(ch_concepts),
        "related_chapters_count": len(ch_related),
        "sample_keywords": [kw.get("term", kw) if isinstance(kw, dict) else kw for kw in ch_keywords[:5]],
        "sample_concepts": [c.get("concept", c) if isinstance(c, dict) else c for c in ch_concepts[:3]],
        "sample_related": [
            {"book": r.get("book", ""), "chapter": r.get("chapter", ""), "similarity": r.get("similarity", 0)}
            for r in ch_related[:3]
        ] if ch_related else []
    }


def extract_evaluation_summary(aggregate: dict[str, Any]) -> dict[str, Any]:
    """
    Extract only the essential data needed for LLM evaluation from full aggregate.
    
    This reduces payload from ~7MB to ~50KB per profile while keeping evaluation-relevant data.
    """
    source_book = aggregate.get("source_book", {})
    source_metadata = source_book.get("metadata", {}) if isinstance(source_book, dict) else {}
    chapters = source_metadata.get("chapters", [])
    
    # Collect all keywords and concepts from source book
    all_keywords = []
    all_concepts = []
    chapter_summaries = []
    
    for ch in chapters[:15]:  # First 15 chapters for evaluation
        ch_keywords = ch.get("keywords", [])
        ch_concepts = ch.get("concepts", [])
        
        # Extract terms using helper functions
        all_keywords.extend(_extract_terms_from_items(ch_keywords, "term"))
        all_concepts.extend(_extract_terms_from_items(ch_concepts, "concept"))
        
        # Create chapter summary
        chapter_summaries.append(_create_chapter_summary(ch))
    
    # Get unique keywords and concepts
    unique_keywords = list(set(all_keywords))
    unique_concepts = list(set(all_concepts))
    
    # Calculate stats
    stats = aggregate.get("statistics", {})
    
    return {
        "source_book": source_book.get("name", "Unknown") if isinstance(source_book, dict) else "Unknown",
        "statistics": {
            "total_books": stats.get("total_books", 0),
            "total_chapters": stats.get("total_chapters", 0),
            "companion_books": stats.get("companion_books", 0),
        },
        "extraction_summary": {
            "total_keywords_in_sample": len(all_keywords),
            "unique_keywords_in_sample": len(unique_keywords),
            "keyword_diversity_ratio": len(unique_keywords) / len(all_keywords) if all_keywords else 0,
            "total_concepts_in_sample": len(all_concepts),
            "unique_concepts_in_sample": len(unique_concepts),
        },
        "sample_keywords": unique_keywords[:100],  # Top 100 unique keywords
        "sample_concepts": unique_concepts[:50],   # Top 50 unique concepts
        "chapter_analysis": chapter_summaries,
    }


def create_comparative_prompt(aggregates: dict[str, dict[str, Any]]) -> str:
    """
    Create a rigorous navigation-based evaluation prompt.
    
    The LLM acts as a NAVIGATOR testing discoverability, NOT as an expert evaluator.
    It searches the aggregates and reports what is/isn't discoverable.
    """
    
    # Define the 18 system design questions with focus areas
    questions = [
        ("Q1", "Scalable LLM code understanding system", 
         ["chunking", "embeddings", "retrieval", "indexing", "grounding", "hallucination"]),
        ("Q2", "Agentic coding assistant with safe code changes",
         ["sandboxing", KEYWORD_STATIC_ANALYSIS, "verification", "diff", "rollback", "guardrails"]),
        ("Q3", "LLM batch processing for multi-GB datasets",
         ["map-reduce", "chunk", "orchestration", "persistent state", "quality gates", "metadata"]),
        ("Q4", "Multi-model orchestrator across providers",
         ["routing", "retry", "backoff", "cost", "degradation", "parallelism", "normalization"]),
        ("Q5", "Fully local fallback system",
         ["local inference", "Qwen", "Llama", "GGUF", "quantization", "offline", "on-device"]),
        ("Q6", "LLM agent for infrastructure automation",
         ["tool schema", "IAM", "guardrails", "traceability", "intent classification", "verification"]),
        ("Q7", "Multi-agent collaboration framework",
         ["choreography", "handoff", "arbitration", "termination", "confidence", "roles"]),
        ("Q8", "Hallucination prevention in agentic systems",
         ["grounding", "schema validation", "safety rails", "log-probability", "self-test"]),
        ("Q9", "100GB+ document indexing system",
         ["distributed", "HNSW", "IVF", "vector pruning", "hot storage", "cold storage", "partial update"]),
        ("Q10", "Secure multi-tenant fine-tuning",
         ["data boundary", "encryption", "isolation", "gradients", "audit", "tenant"]),
        ("Q11", "70B model inference latency reduction",
         ["KV cache", "speculative decoding", "MoE", "distillation", "flash-attention", "quantization"]),
        ("Q12", "Diagnosing confident but incorrect LLM outputs",
         ["retrieval eval", "likelihood", "consistency", "chain-of-thought", "benchmark"]),
        ("Q13", "Safety guardrails for code-writing agents",
         [KEYWORD_STATIC_ANALYSIS, "sandboxing", "unit test", "rollback", "anomaly detection", "approval"]),
        ("Q14", "Jailbreak detection system",
         ["classifier", "intent detection", "safety model", "perplexity", "pattern"]),
        ("Q15", "Resume-job description matching system",
         ["skill embedding", "requirement extraction", "scoring", "rewriting", "ensemble"]),
        ("Q16", "LLM-powered refactoring engine",
         ["AST", "snippet embedding", "per-file isolation", "diff-only", "self-review"]),
        ("Q17", "Code-to-architecture diagram microservice",
         ["static parsing", "call graph", "summarization", "Mermaid", "PlantUML", "JSON schema"]),
        ("Q18", "Knowledge graph from technical textbooks",
         ["metadata extraction", "taxonomy", "semantic alignment", "cross-book", "deduplication", "guideline"]),
    ]
    
    # Build questions section
    questions_text = ""
    for qid, title, focus_areas in questions:
        questions_text += f"\n{qid}: \"{title}\"\n"
        questions_text += f"    Focus areas to search: {focus_areas}\n"
    
    prompt = f"""You are a KNOWLEDGE GRAPH NAVIGATOR testing the discoverability of technical concepts.

## YOUR ROLE - READ CAREFULLY

You are NOT a domain expert giving opinions.
You are SIMULATING A USER who needs to find information using ONLY the aggregate data provided.
You CANNOT use your own knowledge - you can ONLY report what is DISCOVERABLE in the aggregates.

## CRITICAL RULES

1. DO NOT answer the system design questions yourself
2. DO NOT use your training knowledge to evaluate quality  
3. ONLY report what you can find by searching the provided sample_keywords and cross-references
4. Your job is to TEST NAVIGATION through the knowledge graph, not demonstrate expertise
5. Every claim must cite SPECIFIC DATA from the aggregates

## WHAT YOU MUST DO

For each aggregate (BASELINE, CURRENT, MODERATE, AGGRESSIVE), perform these analyses:

### ANALYSIS 1: Duplicate Detection
Scan the sample_keywords list for morphological variants:
- Find word groups that share the same stem (e.g., "model", "models", "modeling")
- Count how many duplicate groups exist
- BASELINE should have MORE duplicates (stem deduplication was OFF)
- Report the EXACT duplicate pairs you find in the data

### ANALYSIS 2: Noise Term Identification  
Count these noise categories in sample_keywords:
- Section markers: "introduction", "conclusion", "summary", "chapter", "section", "example"
- Generic terms: "approach", "method", "technique", "system", "process", "way"
List the EXACT noise terms you find.

### ANALYSIS 3: Cross-Reference Validation
For each chapter's sample_related entries:
- Read the source chapter title and the target book/chapter
- Determine: Does this connection make logical sense for navigation?
- Count valid vs invalid connections
- Give 2-3 specific examples of good AND bad cross-references

### ANALYSIS 4: Navigation Test (18 Questions)
For EACH question below, search the aggregate:

{questions_text}

For each question:
1. Search sample_keywords for the focus area terms
2. Report which terms are FOUND vs MISSING
3. Check if cross-references lead to relevant content
4. Score navigation success: 1-10 (based on % of focus areas discoverable)

## EXAMPLE OF CORRECT ANALYSIS (Follow This Pattern)

Question Q7: "Multi-agent collaboration framework"
Focus areas: ["choreography", "handoff", "arbitration", "termination", "confidence", "roles"]

BASELINE aggregate search:
```
sample_keywords scan:
  - "choreography" → NOT FOUND
  - "handoff" → NOT FOUND  
  - "arbitration" → NOT FOUND
  - "termination" → NOT FOUND
  - "confidence" → FOUND (appears in list)
  - "roles" → NOT FOUND
  - "agent" → FOUND (related term)
  - "multi-agent" → NOT FOUND

Cross-references checked:
  - No chapters with "agent" in title found
  
Focus areas found: 1/6 (17%)
Navigation score: 2/10
```

CURRENT aggregate search:
```
sample_keywords scan:
  - "choreography" → NOT FOUND
  - "handoff" → NOT FOUND
  - "arbitration" → NOT FOUND
  - "agent" → FOUND
  - "multi-agent" → FOUND
  - "coordination" → FOUND (related)
  
Focus areas found: 2/6 (33%)
Navigation score: 4/10
```

## REQUIRED JSON OUTPUT FORMAT

Respond with ONLY valid JSON (no markdown code blocks):

{{
  "analysis_1_duplicates": {{
    "baseline": {{
      "duplicate_groups_found": <number>,
      "examples": [["model", "models"], ["train", "training"], ...]
    }},
    "current": {{
      "duplicate_groups_found": <number>,
      "examples": [...]
    }},
    "moderate": {{...}},
    "aggressive": {{...}}
  }},
  
  "analysis_2_noise": {{
    "baseline": {{
      "noise_terms_found": ["introduction", "example", ...],
      "noise_count": <number>,
      "total_keywords": <number from sample_keywords length>
    }},
    "current": {{...}},
    "moderate": {{...}},
    "aggressive": {{...}}
  }},
  
  "analysis_3_cross_refs": {{
    "baseline": {{
      "total_checked": <number>,
      "valid": <number>,
      "invalid": <number>,
      "good_examples": [
        {{"from": "Ch5: X", "to": "Ch12: Y", "why_valid": "..."}}
      ],
      "bad_examples": [
        {{"from": "Ch3: A", "to": "Ch45: B", "why_invalid": "..."}}
      ]
    }},
    "current": {{...}},
    "moderate": {{...}},
    "aggressive": {{...}}
  }},
  
  "analysis_4_navigation": {{
    "Q1": {{
      "focus_areas": ["chunking", "embeddings", ...],
      "baseline": {{"found": [...], "missing": [...], "score": <1-10>}},
      "current": {{"found": [...], "missing": [...], "score": <1-10>}},
      "moderate": {{"found": [...], "missing": [...], "score": <1-10>}},
      "aggressive": {{"found": [...], "missing": [...], "score": <1-10>}},
      "best_profile": "<profile with highest score>"
    }},
    "Q2": {{...}},
    ... (all 18 questions)
  }},
  
  "summary": {{
    "navigation_totals": {{
      "baseline": <sum of all 18 Q scores>,
      "current": <sum>,
      "moderate": <sum>,
      "aggressive": <sum>
    }},
    "duplicate_comparison": {{
      "baseline_groups": <N>,
      "current_groups": <N>,
      "reduction_percent": "<X%>"
    }},
    "questions_won": {{
      "baseline": <count where baseline had highest score>,
      "current": <count>,
      "moderate": <count>,
      "aggressive": <count>
    }},
    "overall_recommendation": "<best profile>",
    "evidence": "<cite specific numbers: X navigation score, Y fewer duplicates, Z% noise>"
  }}
}}

## AGGREGATE DATA TO ANALYZE

"""
    
    # Add summarized data for each profile
    for profile in ["baseline", "current", "moderate", "aggressive"]:
        suffix = profile.upper()
        if suffix.lower() in aggregates or profile in aggregates:
            data = aggregates.get(profile, aggregates.get(suffix.lower(), {}))
            summary = extract_evaluation_summary(data)
            prompt += f"\n### {suffix} PROFILE\n"
            prompt += json.dumps(summary, indent=2)
            prompt += "\n"
    
    return prompt


# =============================================================================
# CHUNKED EVALUATION APPROACH
# =============================================================================
# This approach splits the 18 questions into 3 chunks of 6 questions each,
# sends each chunk to the LLM separately, merges the results locally,
# and then sends the merged scores for a final assessment.
# 
# Benefits:
#   - Smaller per-call token usage (~25KB vs 73KB)
#   - Lower timeout risk
#   - Better model context pressure management
#   - Final decision is more focused
# =============================================================================

# Define all 18 questions globally for reuse
EVALUATION_QUESTIONS = [
    ("Q1", "Scalable LLM code understanding system", 
     ["chunking", "embeddings", "retrieval", "indexing", "grounding", "hallucination"]),
    ("Q2", "Agentic coding assistant with safe code changes",
     ["sandboxing", KEYWORD_STATIC_ANALYSIS, "verification", "diff", "rollback", "guardrails"]),
    ("Q3", "LLM batch processing for multi-GB datasets",
     ["map-reduce", "chunk", "orchestration", "persistent state", "quality gates", "metadata"]),
    ("Q4", "Multi-model orchestrator across providers",
     ["routing", "retry", "backoff", "cost", "degradation", "parallelism", "normalization"]),
    ("Q5", "Fully local fallback system",
     ["local inference", "Qwen", "Llama", "GGUF", "quantization", "offline", "on-device"]),
    ("Q6", "LLM agent for infrastructure automation",
     ["tool schema", "IAM", "guardrails", "traceability", "intent classification", "verification"]),
    ("Q7", "Multi-agent collaboration framework",
     ["choreography", "handoff", "arbitration", "termination", "confidence", "roles"]),
    ("Q8", "Hallucination prevention in agentic systems",
     ["grounding", "schema validation", "safety rails", "log-probability", "self-test"]),
    ("Q9", "100GB+ document indexing system",
     ["distributed", "HNSW", "IVF", "vector pruning", "hot storage", "cold storage", "partial update"]),
    ("Q10", "Secure multi-tenant fine-tuning",
     ["data boundary", "encryption", "isolation", "gradients", "audit", "tenant"]),
    ("Q11", "70B model inference latency reduction",
     ["KV cache", "speculative decoding", "MoE", "distillation", "flash-attention", "quantization"]),
    ("Q12", "Diagnosing confident but incorrect LLM outputs",
     ["retrieval eval", "likelihood", "consistency", "chain-of-thought", "benchmark"]),
    ("Q13", "Safety guardrails for code-writing agents",
     [KEYWORD_STATIC_ANALYSIS, "sandboxing", "unit test", "rollback", "anomaly detection", "approval"]),
    ("Q14", "Jailbreak detection system",
     ["classifier", "intent detection", "safety model", "perplexity", "pattern"]),
    ("Q15", "Resume-job description matching system",
     ["skill embedding", "requirement extraction", "scoring", "rewriting", "ensemble"]),
    ("Q16", "LLM-powered refactoring engine",
     ["AST", "snippet embedding", "per-file isolation", "diff-only", "self-review"]),
    ("Q17", "Code-to-architecture diagram microservice",
     ["static parsing", "call graph", "summarization", "Mermaid", "PlantUML", "JSON schema"]),
    ("Q18", "Knowledge graph from technical textbooks",
     ["metadata extraction", "taxonomy", "semantic alignment", "cross-book", "deduplication", "guideline"]),
]


def create_chunked_prompt(aggregates: dict[str, dict[str, Any]], questions: list[tuple], chunk_num: int) -> str:
    """
    Create a prompt for a chunk of questions (Stage 1).
    
    Args:
        aggregates: The 4 profile aggregates
        questions: List of (qid, title, focus_areas) tuples for this chunk
        chunk_num: Which chunk this is (1, 2, or 3)
    
    Returns:
        Prompt string for this chunk
    """
    # Build questions section
    questions_text = ""
    for qid, title, focus_areas in questions:
        questions_text += f"\n{qid}: \"{title}\"\n"
        questions_text += f"    Focus areas to search: {focus_areas}\n"
    
    prompt = f"""You are a KNOWLEDGE GRAPH NAVIGATOR testing the discoverability of technical concepts.

## CHUNK {chunk_num} OF 3 - Questions {questions[0][0]} to {questions[-1][0]}

You are analyzing 4 extraction profiles to determine which produces better keyword navigation.
This is chunk {chunk_num}/3 - you are scoring questions {questions[0][0]}-{questions[-1][0]} only.

## CRITICAL RULES

1. DO NOT answer the system design questions yourself
2. ONLY report what you can find by searching the provided sample_keywords
3. For each question, search for the focus area terms in each profile's keywords
4. Score based on how many focus areas are DISCOVERABLE (found in keywords)

## QUESTIONS FOR THIS CHUNK

{questions_text}

## SCORING INSTRUCTIONS

For each question:
1. Search sample_keywords for each focus area term
2. Count: found vs missing terms
3. Score: (found / total) * 10, rounded to nearest integer

## REQUIRED JSON OUTPUT

Respond with ONLY valid JSON (no markdown):

{{
  "chunk": {chunk_num},
  "questions_evaluated": ["{questions[0][0]}", ..., "{questions[-1][0]}"],
  "scores": {{
    "{questions[0][0]}": {{
      "baseline": {{"found": [...], "missing": [...], "score": <1-10>}},
      "current": {{"found": [...], "missing": [...], "score": <1-10>}},
      "moderate": {{"found": [...], "missing": [...], "score": <1-10>}},
      "aggressive": {{"found": [...], "missing": [...], "score": <1-10>}}
    }},
    ... (all {len(questions)} questions in this chunk)
  }}
}}

## AGGREGATE DATA TO ANALYZE

"""
    
    # Add summarized data for each profile
    for profile in ["baseline", "current", "moderate", "aggressive"]:
        if profile in aggregates:
            summary = extract_evaluation_summary(aggregates[profile])
            prompt += f"\n### {profile.upper()} PROFILE\n"
            prompt += json.dumps(summary, indent=2)
            prompt += "\n"
    
    return prompt


def create_final_assessment_prompt(merged_scores: dict[str, Any]) -> str:
    """
    Create prompt for final assessment (Stage 2).
    
    Takes the merged scores from all 3 chunks and asks the LLM
    to make a final recommendation.
    
    Args:
        merged_scores: Combined scores from all chunks
    
    Returns:
        Prompt string for final assessment
    """
    prompt = f"""You are making a FINAL ASSESSMENT of 4 extraction profiles based on navigation test results.

## YOUR TASK

You have received evaluation scores from 18 system design questions.
Each question tested whether focus area keywords were discoverable in the knowledge graph.

Based on the scores below, determine which profile is BEST for production use.

## MERGED SCORES FROM ALL 18 QUESTIONS

{json.dumps(merged_scores, indent=2)}

## ANALYSIS REQUIRED

1. Calculate total navigation score for each profile (sum of all 18 question scores)
2. Count how many questions each profile "won" (had highest score)
3. Identify any patterns (which profiles excel at which question types?)
4. Make a final recommendation

## REQUIRED JSON OUTPUT

Respond with ONLY valid JSON (no markdown):

{{
  "totals": {{
    "baseline": <sum of 18 scores>,
    "current": <sum>,
    "moderate": <sum>,
    "aggressive": <sum>
  }},
  "questions_won": {{
    "baseline": <count where baseline had highest score>,
    "current": <count>,
    "moderate": <count>,
    "aggressive": <count>
  }},
  "analysis": {{
    "baseline_strengths": "<what types of questions baseline excels at>",
    "current_strengths": "<what current excels at>",
    "moderate_strengths": "<what moderate excels at>",
    "aggressive_strengths": "<what aggressive excels at>"
  }},
  "recommendation": {{
    "best_for_production": "<baseline|current|moderate|aggressive>",
    "confidence": "<high|medium|low>",
    "reasoning": "<2-3 sentences citing specific scores and patterns>"
  }}
}}
"""
    return prompt


def is_retryable_error(result: dict[str, Any]) -> bool:
    """Check if an error result is retryable (rate limit or temporary)."""
    if "error" not in result:
        return False
    
    error = result["error"].lower()
    retryable_patterns = [
        "429",
        "rate limit",
        "rate-limit",
        "too many requests",
        "overloaded",
        "529",
        "503",
        "service unavailable",
        "timeout",
        "quota exceeded",
    ]
    
    return any(pattern in error for pattern in retryable_patterns)


def call_llm_with_retry(model: str, config: "LLMConfig", prompt: str) -> dict[str, Any]:
    """
    Call an LLM with automatic retry on rate limits.
    
    Uses exponential backoff for retries.
    Refactored per S3776 to use _calculate_retry_delay helper.
    
    Args:
        model: Model key (e.g., "claude-opus-4.5", "gpt-5")
        config: LLMConfig for the model
        prompt: The prompt to send
    
    Returns:
        Parsed JSON response or error dict
    """
    last_result = None
    
    for attempt in range(MAX_RETRIES + 1):
        # Call the LLM
        result = call_llm(model, config, prompt)
        
        # Success - return immediately
        if "error" not in result:
            if attempt > 0:
                print(f" (succeeded on retry {attempt})")
            return result
        
        # Check if error is retryable
        if not is_retryable_error(result):
            return result
        
        last_result = result
        
        # Don't retry if we've exhausted attempts
        if attempt >= MAX_RETRIES:
            break
        
        # Use helper for delay calculation
        error_msg = result.get("error", "")
        delay = _calculate_retry_delay(attempt, error_msg)
        
        print(f"\n     ⚠️  {error_msg[:50]}...")
        print(f"     🔄 Retry {attempt + 1}/{MAX_RETRIES} in {delay}s...", end="", flush=True)
        time.sleep(delay)
    
    # All retries exhausted
    return {
        "error": f"Max retries ({MAX_RETRIES}) exceeded. Last error: {last_result.get('error', 'unknown')}",
        "retries_attempted": MAX_RETRIES,
        "last_result": last_result
    }


def call_llm(model: str, config: "LLMConfig", prompt: str) -> dict[str, Any]:
    """
    Route a prompt to the appropriate LLM handler.
    
    Args:
        model: Model key (e.g., "claude-opus-4.5", "gpt-5")
        config: LLMConfig for the model
        prompt: The prompt to send
    
    Returns:
        Parsed JSON response or error dict
    """
    if model.startswith("deepseek"):
        return call_deepseek(config, prompt)
    elif model.startswith("gemini"):
        return call_gemini(config, prompt)
    elif model.startswith("claude"):
        return call_claude(config, prompt)
    elif model.startswith("gpt"):
        return call_openai(config, prompt)
    else:
        return {"error": f"No handler for {model}"}


def _accumulate_profile_scores(
    merged: dict[str, Any],
    qid: str,
    profile_scores: dict[str, Any]
) -> None:
    """
    Accumulate scores for a single question into merged totals.
    
    Extracted from merge_chunk_results() to reduce complexity (S3776).
    
    Args:
        merged: The merged results dict to update.
        qid: Question ID.
        profile_scores: Scores dict for this question.
    """
    merged["all_scores"][qid] = profile_scores
    
    for profile in ["baseline", "current", "moderate", "aggressive"]:
        if profile in profile_scores:
            score = profile_scores[profile].get("score", 0)
            if isinstance(score, (int, float)):
                merged["profile_totals"][profile] += score


def merge_chunk_results(chunk_results: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Merge results from 3 chunks into a single scores dictionary.
    
    Args:
        chunk_results: List of 3 chunk result dicts
    
    Returns:
        Merged scores for all 18 questions
    """
    merged = {
        "all_scores": {},
        "profile_totals": {
            "baseline": 0,
            "current": 0,
            "moderate": 0,
            "aggressive": 0
        }
    }
    
    for chunk in chunk_results:
        if "error" in chunk:
            continue
        
        scores = chunk.get("scores", {})
        for qid, profile_scores in scores.items():
            _accumulate_profile_scores(merged, qid, profile_scores)
    
    return merged


def run_chunked_evaluation(model: str, aggregates: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """
    Run the chunked evaluation for a single model.
    
    Stage 1: 3 API calls with 6 questions each
    Stage 2: 1 API call for final assessment
    
    Refactored per S3776 to use _process_evaluation_chunk helper.
    
    Args:
        model: Model key to use
        aggregates: The 4 profile aggregates
    
    Returns:
        Complete evaluation result including final recommendation
    """
    configs = get_llm_configs()
    
    if model not in configs:
        return {"error": f"Model '{model}' not configured"}
    
    config = configs[model]
    
    # Split questions into 3 chunks of 6
    chunks = [
        EVALUATION_QUESTIONS[0:6],   # Q1-Q6
        EVALUATION_QUESTIONS[6:12],  # Q7-Q12
        EVALUATION_QUESTIONS[12:18], # Q13-Q18
    ]
    
    # Stage 1: Process each chunk using helper
    chunk_results = [
        _process_evaluation_chunk(i, chunk_questions, aggregates, model, config)
        for i, chunk_questions in enumerate(chunks, 1)
    ]
    
    # Check if we have enough successful chunks
    successful_chunks = [c for c in chunk_results if "error" not in c]
    if len(successful_chunks) < 2:
        return {"error": "Too many chunk failures", "chunk_results": chunk_results}
    
    # Merge chunk results
    merged = merge_chunk_results(chunk_results)
    
    # Stage 2: Final assessment
    print("      🎯 Final assessment...", end=" ", flush=True)
    time.sleep(API_CALL_DELAY_SECONDS)
    
    final_prompt = create_final_assessment_prompt(merged)
    final_result = call_llm_with_retry(model, config, final_prompt)
    
    if "error" in final_result:
        print(f"❌ {final_result['error'][:40]}")
    else:
        best = final_result.get("recommendation", {}).get("best_for_production", "N/A")
        print(f"✅ Recommends: {best.upper()}")
    
    return {
        "model": model,
        "approach": "chunked_evaluation",
        "stage1_chunks": chunk_results,
        "merged_scores": merged,
        "final_assessment": final_result,
        "recommendation": final_result.get("recommendation", {}) if "error" not in final_result else None
    }


def run_chunked_comparative_evaluation(models: list[str] | None = None) -> dict[str, Any]:
    """
    Run chunked comparative evaluation across multiple models.
    
    This is the main entry point for the new chunked approach.
    Refactored per S3776 to use _load_profile_aggregates and _calculate_consensus helpers.
    
    Args:
        models: List of model keys to use (defaults to all 10)
    
    Returns:
        Complete evaluation results with consensus
    """
    eval_dir = PROJECT_ROOT / "outputs" / "evaluation"
    profiles = ["baseline", "current", "moderate", "aggressive"]
    suffixes = {"baseline": "BASELINE", "current": "CURRENT", "moderate": "MODERATE", "aggressive": "AGGRESSIVE"}
    
    # Load all aggregates using helper
    aggregates = _load_profile_aggregates(eval_dir, profiles, suffixes)
    
    if len(aggregates) != 4:
        return {"error": f"Missing aggregates. Found {len(aggregates)}/4. Run extraction first."}
    
    # Default models
    if models is None:
        models = [
            MODEL_CLAUDE_OPUS, MODEL_CLAUDE_SONNET,
            MODEL_GPT, "gpt-5", "gpt-5-mini", "gpt-5-nano",
            "gemini-3-pro", MODEL_GEMINI_FLASH,
            "deepseek-v3", "deepseek-r1"
        ]
    
    configs = get_llm_configs()
    available_models = [m for m in models if m in configs]
    
    print("\n🔄 Running CHUNKED evaluation approach")
    print("   Strategy: 3 chunks × 6 questions + 1 final assessment = 4 calls per model")
    print(f"   Models: {len(available_models)}/{len(models)} available")
    print(f"   Total API calls: ~{len(available_models) * 4}")
    print()
    
    results = {
        "evaluation_type": "chunked_comparative",
        "timestamp": datetime.now().isoformat(),
        "approach": {
            "stage1": "3 chunks of 6 questions each (~25KB per call)",
            "stage2": "Final assessment from merged scores (~5KB)",
            "total_calls_per_model": 4
        },
        "profiles_evaluated": profiles,
        "models_used": [],
        "evaluations": {},
    }
    
    for i, model in enumerate(available_models, 1):
        print(f"  🤖 [{i}/{len(available_models)}] {model}")
        
        if i > 1:
            print(f"     ⏳ Waiting {API_CALL_DELAY_SECONDS}s before next model...")
            time.sleep(API_CALL_DELAY_SECONDS)
        
        eval_result = run_chunked_evaluation(model, aggregates)
        results["evaluations"][model] = eval_result
        
        if "error" not in eval_result:
            results["models_used"].append(model)
    
    # Calculate consensus using helper
    if results["models_used"]:
        consensus_result = _calculate_consensus(results["evaluations"], results["models_used"])
        if consensus_result:
            results["consensus"] = consensus_result
            print(f"\n📊 CONSENSUS: {consensus_result['best_for_production'].upper()}")
            print(f"   Votes: {consensus_result['votes']}")
            print(f"   Agreement: {consensus_result['agreement_ratio']:.0%}")
    
    # Save results
    output_file = eval_dir / f"llm_chunked_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Chunked evaluation saved: {output_file}")
    
    return results


def _load_aggregates_from_dir(eval_dir: Path) -> dict[str, Any]:
    """Load all aggregate files from evaluation directory.
    
    Reduces cognitive complexity by extracting the loading loop.
    
    Args:
        eval_dir: Directory containing aggregate JSON files
        
    Returns:
        Dictionary mapping profile names to their loaded data
    """
    aggregates = {}
    profiles = ["baseline", "current", "moderate", "aggressive"]
    suffixes = {"baseline": "BASELINE", "current": "CURRENT", "moderate": "MODERATE", "aggressive": "AGGRESSIVE"}
    
    print("\n📂 Loading aggregates...")
    for profile in profiles:
        suffix = suffixes[profile]
        agg_file = eval_dir / f"aggregate_{suffix}.json"
        
        if agg_file.exists():
            with open(agg_file) as f:
                aggregates[profile] = json.load(f)
            print(f"  ✅ {suffix}: Loaded")
        else:
            print(f"  ❌ {suffix}: Not found")
    
    return aggregates


def _call_model_api(model: str, config: Any, prompt: str) -> dict[str, Any]:
    """Route to appropriate API handler based on model provider.
    
    Reduces cognitive complexity by extracting provider routing logic.
    
    Args:
        model: Model identifier string
        config: Model configuration object
        prompt: Prompt text to send
        
    Returns:
        Evaluation result dictionary from the API
    """
    if model.startswith("deepseek"):
        return call_deepseek(config, prompt)
    if model.startswith("gemini"):
        return call_gemini(config, prompt)
    if model.startswith("claude"):
        return call_claude(config, prompt)
    if model.startswith("gpt"):
        return call_openai(config, prompt)
    return {"error": f"No handler for {model}"}


def _process_model_result(model: str, eval_result: dict[str, Any], results: dict[str, Any]) -> None:
    """Process and log the result from a single model evaluation.
    
    Reduces cognitive complexity by extracting result processing logic.
    
    Args:
        model: Model identifier string
        eval_result: Result dictionary from API call
        results: Main results dictionary to update
    """
    results["evaluations"][model] = eval_result
    
    if "error" not in eval_result:
        results["models_used"].append(model)
        rec = eval_result.get("recommendation", {})
        best = rec.get("best_for_production", "N/A")
        print(f"     ✅ {model}: Recommends '{best}' for production")
    else:
        print(f"     ❌ {model}: Error - {eval_result.get('error', 'Unknown')[:80]}")


def _aggregate_recommendations(results: dict[str, Any]) -> None:
    """Aggregate recommendations across LLMs to find consensus.
    
    Reduces cognitive complexity by extracting consensus aggregation.
    
    Args:
        results: Main results dictionary to update with consensus
    """
    if not results["models_used"]:
        return
        
    recommendations = {}
    for model, eval_result in results["evaluations"].items():
        if "recommendation" in eval_result:
            best = eval_result["recommendation"].get("best_for_production", "")
            if best:
                recommendations[best] = recommendations.get(best, 0) + 1
    
    if recommendations:
        consensus = max(recommendations, key=recommendations.get)
        results["consensus"] = {
            "best_for_production": consensus,
            "votes": recommendations,
            "agreement_ratio": recommendations[consensus] / len(results["models_used"])
        }
        print(f"\n📊 Consensus: {consensus.upper()} ({recommendations[consensus]}/{len(results['models_used'])} LLMs agree)")


def run_comparative_evaluation(models: list[str] | None = None) -> dict[str, Any]:
    """
    Run Strategy B comparative evaluation.
    
    Loads all 4 aggregates and sends them to each LLM for comparison.
    
    Default models (per test plan):
        - Claude Opus 4.5, Claude Sonnet 4.5
        - GPT-5.1, GPT-5, gpt-5.1-mini, gpt-5.1-nano
        - Gemini 3 Pro, Gemini 3 Flash
        - DeepSeek V3, DeepSeek R1
    """
    eval_dir = PROJECT_ROOT / "outputs" / "evaluation"
    
    # Load all aggregates using helper
    aggregates = _load_aggregates_from_dir(eval_dir)
    
    if len(aggregates) != 4:
        return {"error": f"Missing aggregates. Found {len(aggregates)}/4. Run extraction first."}
    
    # Create comparative prompt
    prompt = create_comparative_prompt(aggregates)
    print(f"\n📝 Comparative prompt created ({len(prompt):,} chars)")
    
    # Default models for comparative evaluation (actual model names)
    if models is None:
        models = [
            MODEL_CLAUDE_OPUS, MODEL_CLAUDE_SONNET,
            MODEL_GPT, "gpt-5", "gpt-5-mini", "gpt-5-nano",
            "gemini-3-pro", MODEL_GEMINI_FLASH,
            "deepseek-v3", "deepseek-r1"
        ]
    
    configs = get_llm_configs()
    
    # Initialize results structure
    results = {
        "evaluation_type": "comparative",
        "timestamp": datetime.now().isoformat(),
        "profiles_evaluated": ["baseline", "current", "moderate", "aggressive"],
        "models_used": [],
        "evaluations": {},
    }
    
    print("\n🔍 Running comparative LLM evaluations...")
    print("   Sending all 4 profiles to each LLM for comparison")
    print(f"   Using {API_CALL_DELAY_SECONDS}s delay between API calls to avoid rate limits\n")
    
    # Run evaluation for each configured model
    models_called = 0
    for model in models:
        if model not in configs:
            print(f"  ⚠️  {model}: Not configured (skipping)")
            continue
        
        if models_called > 0:
            print(f"     ⏳ Waiting {API_CALL_DELAY_SECONDS}s before next API call...")
            time.sleep(API_CALL_DELAY_SECONDS)
        
        config = configs[model]
        print(f"  🤖 [{models_called + 1}/{len(models)}] Calling {config.name} ({config.model})...")
        
        try:
            eval_result = _call_model_api(model, config, prompt)
            _process_model_result(model, eval_result, results)
            models_called += 1
        except Exception as e:
            results["evaluations"][model] = {"error": str(e)}
            models_called += 1
            print(f"     ❌ {model}: Exception - {str(e)[:80]}")
    
    # Aggregate recommendations using helper
    _aggregate_recommendations(results)
    
    # Save results
    output_file = eval_dir / f"llm_comparative_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Comparative evaluation saved: {output_file}")
    
    return results


def list_available_models() -> None:
    """List available LLM models based on configured API keys."""
    configs = get_llm_configs()
    
    # Check all possible providers
    all_providers = {
        "deepseek": ("DEEPSEEK_API_KEY", "DeepSeek Chat"),
        "deepseek-reasoner": ("DEEPSEEK_API_KEY", "DeepSeek Reasoner"),
        "gemini": ("GEMINI_API_KEY", "Gemini 2.5 Flash"),
        "claude": ("ANTHROPIC_API_KEY", "Claude Sonnet 4.5"),
        "openai": ("OPENAI_API_KEY", "GPT-4o"),
    }
    
    print("\n🤖 LLM Models Configuration:")
    print("=" * 60)
    print("\nSet API keys in your .env file:")
    print("  DEEPSEEK_API_KEY=your_key_here")
    print("  GEMINI_API_KEY=your_key_here")
    print("  ANTHROPIC_API_KEY=your_key_here")
    print("  OPENAI_API_KEY=your_key_here")
    print("\n" + "-" * 60)
    
    for name, (env_var, display_name) in all_providers.items():
        if name in configs:
            config = configs[name]
            key_preview = f"***{config.api_key[-4:]}" if config.api_key and len(config.api_key) > 4 else "***"
            print(f"  ✅ {name}: {config.name}")
            print(f"       Model: {config.model}")
            print(f"       Key: {key_preview}")
        else:
            print(f"  ❌ {name}: {display_name}")
            print(f"       Missing: {env_var}")
    
    print("\n" + "=" * 60)
    print("\nUse --test-connection to verify API access")
    print("Use --fetch-models [gemini|deepseek|all] to list available models")


def list_gemini_models() -> list[dict[str, Any]]:
    """
    List available Gemini models from Google's API.
    
    Uses the google-generativeai SDK to fetch the list of available models.
    Requires GEMINI_API_KEY environment variable.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    
    if not gemini_key:
        return [{"error": "GEMINI_API_KEY not set in environment"}]
    
    if GENAI_AVAILABLE and genai is not None:
        try:
            genai.configure(api_key=gemini_key)
            models = []
            for model in genai.list_models():
                models.append({
                    "name": model.name,
                    "display_name": model.display_name,
                    "description": getattr(model, 'description', 'N/A'),
                    "supported_methods": list(model.supported_generation_methods) if hasattr(model, 'supported_generation_methods') else []
                })
            return models
        except Exception as e:
            return [{"error": str(e)}]
    
    # Fallback to REST API
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url)
            response.raise_for_status()
            result = response.json()
            return result.get("models", [])
    except Exception as e:
        return [{"error": str(e)}]


def list_deepseek_models() -> list[dict[str, Any]]:
    """
    List available DeepSeek models.
    
    DeepSeek uses OpenAI-compatible API. This calls the /models endpoint
    to list available models.
    
    Requires DEEPSEEK_API_KEY environment variable.
    """
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
    
    if not deepseek_key:
        return [{"error": "DEEPSEEK_API_KEY not set in environment"}]
    
    # DeepSeek uses OpenAI-compatible API, try /models endpoint
    try:
        url = "https://api.deepseek.com/models"
        headers = {
            "Authorization": f"Bearer {deepseek_key}"
        }
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result.get("data", [])
    except httpx.HTTPStatusError as e:
        # Handle specific HTTP errors
        if e.response.status_code == 402:
            return [
                {"id": "deepseek-chat", "description": "General-purpose chat model", "status": "available"},
                {"id": "deepseek-reasoner", "description": "Reasoning model", "status": "available"},
                {"note": f"Models list retrieved. Account status: {e.response.status_code} (may need credits for API calls)"}
            ]
        return [{"error": f"HTTP {e.response.status_code}: {str(e)}"}]
    except Exception as e:
        # Return known models if API fails
        return [
            {"id": "deepseek-chat", "description": "General-purpose chat model"},
            {"id": "deepseek-reasoner", "description": "Reasoning model (R1)"},
            {"note": f"API error (models still available): {str(e)}"}
        ]


def test_api_connections() -> dict[str, dict[str, Any]]:
    """
    Test API connections for all configured providers.
    
    Refactored per S3776 to use per-provider helper functions.
    
    Returns connection status and available models for each provider.
    """
    results = {}
    
    # Check environment variables
    env_keys = {
        "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY", ""),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    }
    
    print("\n🔐 API Key Status:")
    print("=" * 50)
    for key_name, key_value in env_keys.items():
        if key_value:
            masked = f"***{key_value[-4:]}" if len(key_value) > 4 else "***"
            print(f"  ✅ {key_name}: {masked}")
        else:
            print(f"  ❌ {key_name}: NOT SET")
    
    print("\n🔌 Testing API Connections:")
    print("=" * 50)
    
    # Test each provider using helper functions
    if env_keys["DEEPSEEK_API_KEY"]:
        results["deepseek"] = _test_deepseek_connection(env_keys["DEEPSEEK_API_KEY"])
    else:
        results["deepseek"] = {"status": "no_key"}
        print("\n  DeepSeek: Skipped (no API key)")
    
    if env_keys["GEMINI_API_KEY"]:
        results["gemini"] = _test_gemini_connection(env_keys["GEMINI_API_KEY"])
    else:
        results["gemini"] = {"status": "no_key"}
        print("\n  Gemini: Skipped (no API key)")
    
    if env_keys["ANTHROPIC_API_KEY"]:
        results["anthropic"] = _test_anthropic_connection(env_keys["ANTHROPIC_API_KEY"])
    else:
        results["anthropic"] = {"status": "no_key"}
        print("\n  Anthropic: Skipped (no API key)")
    
    if env_keys["OPENAI_API_KEY"]:
        results["openai"] = _test_openai_connection(env_keys["OPENAI_API_KEY"])
    else:
        results["openai"] = {"status": "no_key"}
        print("\n  OpenAI: Skipped (no API key)")
    
    print("\n" + "=" * 50)
    return results


def _fetch_gemini_models() -> None:
    """Fetch and display Gemini models.
    
    Reduces cognitive complexity by extracting Gemini-specific logic.
    """
    models = list_gemini_models()
    if not models or "error" in models[0]:
        print(f"  ⚠️  Error: {models[0].get('error', 'Unknown error') if models else 'No models returned'}")
        return
    
    for m in models:
        name = m.get("name", m.get("display_name", "Unknown"))
        desc = m.get("description", "")[:80]
        methods = m.get("supported_methods", m.get("supportedGenerationMethods", []))
        print(f"\n  📌 {name}")
        if desc:
            print(f"     {desc}")
        if methods:
            print(f"     Methods: {', '.join(methods[:3])}")


def _fetch_deepseek_models() -> None:
    """Fetch and display DeepSeek models.
    
    Reduces cognitive complexity by extracting DeepSeek-specific logic.
    """
    models = list_deepseek_models()
    for m in models:
        if "note" in m:
            print(f"  ℹ️  {m['note']}")
            continue
        model_id = m.get("id", "Unknown")
        desc = m.get("description", m.get("object", ""))
        print(f"  📌 {model_id}: {desc}")


def fetch_provider_models(provider: str) -> None:
    """Fetch and display available models from a specific provider."""
    print(f"\n📋 Fetching available models from {provider}...")
    print("=" * 60)
    
    if provider == "gemini":
        _fetch_gemini_models()
    elif provider == "deepseek":
        _fetch_deepseek_models()
    else:
        print(f"  ⚠️  Provider '{provider}' not supported for model listing")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluate extraction quality using multiple LLMs"
    )
    
    parser.add_argument(
        "--output-dir",
        help="Path to extraction output directory"
    )
    
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=("PROFILE1", "PROFILE2"),
        help="Compare two extraction profiles"
    )
    
    parser.add_argument(
        "--comparative",
        action="store_true",
        help="Run Strategy B comparative evaluation (all 4 profiles to each LLM) - single large prompt"
    )
    
    parser.add_argument(
        "--chunked",
        action="store_true",
        help="Run CHUNKED comparative evaluation (3 chunks + final assessment) - recommended approach"
    )
    
    parser.add_argument(
        "--models",
        nargs="+",
        choices=["deepseek", "deepseek-reasoner", "gemini", "claude", "openai"],
        help="LLM models to use for evaluation"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List configured LLM models"
    )
    
    parser.add_argument(
        "--fetch-models",
        choices=["gemini", "deepseek", "all"],
        help="Fetch available models from a provider's API"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test API connections for all configured providers"
    )
    
    args = parser.parse_args()
    
    if args.test_connection:
        test_api_connections()
        return
    
    if args.list_models:
        list_available_models()
        return
    
    if args.fetch_models:
        if args.fetch_models == "all":
            fetch_provider_models("gemini")
            fetch_provider_models("deepseek")
        else:
            fetch_provider_models(args.fetch_models)
        return
    
    if args.compare:
        compare_profiles(args.compare[0], args.compare[1], args.models)
        return
    
    if args.comparative:
        run_comparative_evaluation(args.models)
        return
    
    if args.chunked:
        run_chunked_comparative_evaluation(args.models)
        return
    
    if args.output_dir:
        run_evaluation(args.output_dir, args.models)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
