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
API_TIMEOUT_SECONDS = 120   # Increased timeout for larger prompts
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
                "Content-Type": "application/json",
                "Authorization": f"Bearer {deepseek_key}"
            }
        )
        configs["deepseek-r1"] = LLMConfig(
            name="DeepSeek R1",
            base_url="https://api.deepseek.com/chat/completions",
            api_key=deepseek_key,
            model="deepseek-reasoner",  # R1 is deepseek-reasoner
            headers={
                "Content-Type": "application/json",
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
                "Content-Type": "application/json"
            }
        )
        configs["gemini-2.5-flash"] = LLMConfig(
            name="Gemini 2.5 Flash",
            base_url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}",
            api_key=gemini_key,
            model="gemini-2.5-flash",
            headers={
                "Content-Type": "application/json"
            }
        )
    
    # Claude Opus 4.5 and Claude Sonnet 4.5
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if anthropic_key:
        configs["claude-opus-4.5"] = LLMConfig(
            name="Claude Opus 4.5",
            base_url="https://api.anthropic.com/v1/messages",
            api_key=anthropic_key,
            model="claude-opus-4-5-20251101",
            headers={
                "Content-Type": "application/json",
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01"
            }
        )
        configs["claude-sonnet-4.5"] = LLMConfig(
            name="Claude Sonnet 4.5",
            base_url="https://api.anthropic.com/v1/messages",
            api_key=anthropic_key,
            model="claude-sonnet-4-5-20250929",
            headers={
                "Content-Type": "application/json",
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01"
            }
        )
    
    # OpenAI GPT-5.1, GPT-5, GPT-5-mini, GPT-5-nano
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_key:
        configs["gpt-5.1"] = LLMConfig(
            name="GPT-5.1",
            base_url="https://api.openai.com/v1/chat/completions",
            api_key=openai_key,
            model="gpt-5.1",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_key}"
            }
        )
        configs["gpt-5"] = LLMConfig(
            name="GPT-5",
            base_url="https://api.openai.com/v1/chat/completions",
            api_key=openai_key,
            model="gpt-5",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_key}"
            }
        )
        configs["gpt-5-mini"] = LLMConfig(
            name="GPT-5 Mini",
            base_url="https://api.openai.com/v1/chat/completions",
            api_key=openai_key,
            model="gpt-5-mini",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_key}"
            }
        )
        configs["gpt-5-nano"] = LLMConfig(
            name="GPT-5 Nano",
            base_url="https://api.openai.com/v1/chat/completions",
            api_key=openai_key,
            model="gpt-5-nano",
            headers={
                "Content-Type": "application/json",
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
    """
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": "You are an expert at evaluating NLP extraction quality. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
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
            
            # Parse JSON from response
            try:
                # Handle markdown code blocks
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw_response": content[:500]}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s - model may need more time"}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            return {"error": "Rate limited (429) - too many requests"}
        elif e.response.status_code == 401:
            return {"error": "Authentication failed (401) - check API key"}
        else:
            return {"error": f"HTTP {e.response.status_code}: {str(e)[:100]}"}
    except Exception as e:
        return {"error": f"DeepSeek error: {str(e)[:100]}"}


def call_gemini(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """
    Call Gemini API using the Python SDK if available, otherwise REST API.
    
    SDK: google-generativeai
    Model: gemini-3-pro-preview or gemini-2.5-flash
    """
    # Try SDK first (preferred method)
    if GENAI_AVAILABLE and genai is not None:
        try:
            genai.configure(api_key=config.api_key)
            model = genai.GenerativeModel(config.model)
            
            full_prompt = f"You are an expert at evaluating NLP extraction quality. Always respond with valid JSON only, no markdown code blocks.\n\n{prompt}"
            response = model.generate_content(full_prompt)
            content = response.text
            
            # Parse JSON from response
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw_response": content[:500]}
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                return {"error": "Rate limited (429) - quota exceeded"}
            elif "401" in error_msg or "invalid" in error_msg.lower():
                return {"error": "Authentication failed - check API key"}
            return {"error": f"Gemini SDK error: {error_msg[:100]}"}
    
    # Fallback to REST API
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
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw_response": content[:500]}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s"}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            return {"error": "Rate limited (429) - too many requests"}
        elif e.response.status_code == 401:
            return {"error": "Authentication failed (401) - check API key"}
        else:
            return {"error": f"HTTP {e.response.status_code}: {str(e)[:100]}"}
    except Exception as e:
        return {"error": f"Gemini error: {str(e)[:100]}"}


def call_claude(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """Call Claude API (Opus 4.5 or Sonnet 4.5)."""
    payload = {
        "model": config.model,
        "max_tokens": 4000,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "system": "You are an expert at evaluating NLP extraction quality. Always respond with valid JSON only, no markdown code blocks."
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
            
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw_response": content[:500]}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s"}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            return {"error": "Rate limited (429) - too many requests"}
        elif e.response.status_code == 401:
            return {"error": "Authentication failed (401) - check API key"}
        elif e.response.status_code == 529:
            return {"error": "API overloaded (529) - try again later"}
        else:
            return {"error": f"HTTP {e.response.status_code}: {str(e)[:100]}"}
    except Exception as e:
        return {"error": f"Claude error: {str(e)[:100]}"}


def call_openai(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """Call OpenAI API (GPT-5.1, GPT-5, gpt-5.1-mini, gpt-5.1-nano)."""
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": "You are an expert at evaluating NLP extraction quality. Always respond with valid JSON only, no markdown code blocks."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4000
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
            
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw_response": content[:500]}
    
    except httpx.TimeoutException:
        return {"error": f"Timeout after {API_TIMEOUT_SECONDS}s"}
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            # Extract retry-after if available
            retry_after = e.response.headers.get("retry-after", "unknown")
            return {"error": f"Rate limited (429) - retry after {retry_after}s"}
        elif e.response.status_code == 401:
            return {"error": "Authentication failed (401) - check API key"}
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
    
    # Route to appropriate API handler
    if llm_name in ("deepseek", "deepseek-reasoner"):
        return call_deepseek(config, prompt)
    elif llm_name == "gemini":
        return call_gemini(config, prompt)
    elif llm_name == "claude":
        return call_claude(config, prompt)
    elif llm_name == "openai":
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
    
    print(f"\n🔍 Running LLM evaluations...")
    
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
        ch_related = ch.get("related_chapters", [])
        
        # Extract keyword terms
        for kw in ch_keywords:
            if isinstance(kw, dict):
                all_keywords.append(kw.get("term", kw.get("keyword", "")))
            else:
                all_keywords.append(str(kw))
        
        # Extract concept terms
        for concept in ch_concepts:
            if isinstance(concept, dict):
                all_concepts.append(concept.get("concept", ""))
            else:
                all_concepts.append(str(concept))
        
        # Chapter summary
        chapter_summaries.append({
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
        })
    
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
    Create a comparative evaluation prompt with summarized aggregates.
    
    Strategy B: Send all profiles to each LLM for direct comparison.
    Uses extracted summaries to keep prompt under 100KB.
    """
    prompt = """You are an expert NLP evaluator assessing keyword extraction quality for technical documentation cross-referencing.

## Task
You have been given extraction outputs from 4 different parameter configurations applied to the same source document. Evaluate each configuration SEQUENTIALLY (not in parallel) and provide an objective comparison.

## Configurations Provided
1. BASELINE: Original settings (stem deduplication OFF, top_n=10)
2. CURRENT: Enhanced settings (stem deduplication ON, top_n=20)
3. MODERATE: Expanded extraction (top_n=25, relaxed thresholds)
4. AGGRESSIVE: Maximum extraction (top_n=35, lowest thresholds)

## Evaluation Criteria (Score 1-10 for each configuration)

1. **Keyword Quality**: Relevance, specificity, technical accuracy
2. **Deduplication Effectiveness**: Absence of redundant variants (model/models/modeling)
3. **Concept Coverage**: Breadth and depth of main themes captured
4. **Cross-Reference Utility**: Value of related chapter connections for navigation
5. **Signal-to-Noise Ratio**: Meaningful terms vs. generic/noise terms

## Required Output Format

Respond with ONLY valid JSON (no markdown code blocks):

{
  "evaluation_timestamp": "<ISO timestamp>",
  "sequential_analysis": {
    "baseline": {
      "scores": {
        "keyword_quality": <1-10>,
        "deduplication_effectiveness": <1-10>,
        "concept_coverage": <1-10>,
        "cross_reference_utility": <1-10>,
        "signal_to_noise": <1-10>
      },
      "overall_score": <1-10>,
      "observations": ["<observation 1>", "<observation 2>"]
    },
    "current": {
      "scores": { ... },
      "overall_score": <1-10>,
      "observations": [...]
    },
    "moderate": {
      "scores": { ... },
      "overall_score": <1-10>,
      "observations": [...]
    },
    "aggressive": {
      "scores": { ... },
      "overall_score": <1-10>,
      "observations": [...]
    }
  },
  "comparative_ranking": [
    {"rank": 1, "profile": "<best>", "overall_score": <1-10>, "rationale": "..."},
    {"rank": 2, "profile": "...", "overall_score": <1-10>, "rationale": "..."},
    {"rank": 3, "profile": "...", "overall_score": <1-10>, "rationale": "..."},
    {"rank": 4, "profile": "<worst>", "overall_score": <1-10>, "rationale": "..."}
  ],
  "recommendation": {
    "best_for_production": "<profile>",
    "reasoning": "...",
    "tradeoffs": ["<tradeoff 1>", "<tradeoff 2>"]
  }
}

## Extraction Data (Summarized for Evaluation)

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
    
    # Load all aggregates
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
    
    if len(aggregates) != 4:
        return {"error": f"Missing aggregates. Found {len(aggregates)}/4. Run extraction first."}
    
    # Create comparative prompt
    prompt = create_comparative_prompt(aggregates)
    print(f"\n📝 Comparative prompt created ({len(prompt):,} chars)")
    
    # Default models for comparative evaluation (actual model names)
    if models is None:
        models = [
            "claude-opus-4.5", "claude-sonnet-4.5",
            "gpt-5.1", "gpt-5", "gpt-5-mini", "gpt-5-nano",
            "gemini-3-pro", "gemini-2.5-flash",
            "deepseek-v3", "deepseek-r1"
        ]
    
    configs = get_llm_configs()
    
    # Run evaluation with each LLM
    results = {
        "evaluation_type": "comparative",
        "timestamp": datetime.now().isoformat(),
        "profiles_evaluated": profiles,
        "models_used": [],
        "evaluations": {},
    }
    
    print("\n🔍 Running comparative LLM evaluations...")
    print(f"   Sending all 4 profiles to each LLM for comparison")
    print(f"   Using {API_CALL_DELAY_SECONDS}s delay between API calls to avoid rate limits\n")
    
    models_called = 0
    for model in models:
        if model not in configs:
            print(f"  ⚠️  {model}: Not configured (skipping)")
            continue
        
        # Add delay between API calls (except for the first one)
        if models_called > 0:
            print(f"     ⏳ Waiting {API_CALL_DELAY_SECONDS}s before next API call...")
            time.sleep(API_CALL_DELAY_SECONDS)
        
        config = configs[model]
        print(f"  🤖 [{models_called + 1}/{len(models)}] Calling {config.name} ({config.model})...")
        
        try:
            # Route to appropriate API handler based on provider
            if model.startswith("deepseek"):
                eval_result = call_deepseek(config, prompt)
            elif model.startswith("gemini"):
                eval_result = call_gemini(config, prompt)
            elif model.startswith("claude"):
                eval_result = call_claude(config, prompt)
            elif model.startswith("gpt"):
                eval_result = call_openai(config, prompt)
            else:
                eval_result = {"error": f"No handler for {model}"}
            
            results["evaluations"][model] = eval_result
            results["models_used"].append(model)
            models_called += 1
            
            if "error" not in eval_result:
                # Extract recommendation
                rec = eval_result.get("recommendation", {})
                best = rec.get("best_for_production", "N/A")
                print(f"     ✅ {model}: Recommends '{best}' for production")
            else:
                print(f"     ❌ {model}: Error - {eval_result.get('error', 'Unknown')[:80]}")
                
        except Exception as e:
            results["evaluations"][model] = {"error": str(e)}
            models_called += 1
            print(f"     ❌ {model}: Exception - {str(e)[:80]}")
    
    # Aggregate recommendations across LLMs
    if results["models_used"]:
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
    
    # Test DeepSeek
    print("\n🔌 Testing API Connections:")
    print("=" * 50)
    
    if env_keys["DEEPSEEK_API_KEY"]:
        print("\n  DeepSeek:")
        try:
            models = list_deepseek_models()
            if models and "error" not in models[0]:
                results["deepseek"] = {"status": "connected", "models": models}
                for m in models:
                    if "id" in m:
                        print(f"    ✅ Model: {m['id']}")
                    if "note" in m:
                        print(f"    ℹ️  {m['note']}")
            else:
                results["deepseek"] = {"status": "error", "error": models[0].get("error", "Unknown")}
                print(f"    ⚠️  {models[0].get('error', 'Unknown error')}")
        except Exception as e:
            results["deepseek"] = {"status": "error", "error": str(e)}
            print(f"    ❌ Error: {e}")
    else:
        results["deepseek"] = {"status": "no_key"}
        print("\n  DeepSeek: Skipped (no API key)")
    
    # Test Gemini
    if env_keys["GEMINI_API_KEY"]:
        print("\n  Gemini:")
        try:
            models = list_gemini_models()
            if models and "error" not in models[0]:
                # Show only first 5 models
                results["gemini"] = {"status": "connected", "model_count": len(models)}
                print(f"    ✅ Connected - {len(models)} models available")
                for m in models[:3]:
                    name = m.get("name", m.get("display_name", "Unknown"))
                    print(f"       - {name}")
                if len(models) > 3:
                    print(f"       ... and {len(models) - 3} more")
            else:
                results["gemini"] = {"status": "error", "error": models[0].get("error", "Unknown")}
                print(f"    ⚠️  {models[0].get('error', 'Unknown error')}")
        except Exception as e:
            results["gemini"] = {"status": "error", "error": str(e)}
            print(f"    ❌ Error: {e}")
    else:
        results["gemini"] = {"status": "no_key"}
        print("\n  Gemini: Skipped (no API key)")
    
    # Test Anthropic
    if env_keys["ANTHROPIC_API_KEY"]:
        print("\n  Anthropic (Claude):")
        try:
            # Simple test - just check if we can reach the API
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    "https://api.anthropic.com/v1/models",
                    headers={
                        "x-api-key": env_keys["ANTHROPIC_API_KEY"],
                        "anthropic-version": "2023-06-01"
                    }
                )
                if response.status_code == 200:
                    results["anthropic"] = {"status": "connected"}
                    print("    ✅ Connected")
                else:
                    results["anthropic"] = {"status": "error", "code": response.status_code}
                    print(f"    ⚠️  HTTP {response.status_code}")
        except Exception as e:
            results["anthropic"] = {"status": "error", "error": str(e)}
            print(f"    ❌ Error: {e}")
    else:
        results["anthropic"] = {"status": "no_key"}
        print("\n  Anthropic: Skipped (no API key)")
    
    # Test OpenAI
    if env_keys["OPENAI_API_KEY"]:
        print("\n  OpenAI:")
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {env_keys['OPENAI_API_KEY']}"}
                )
                if response.status_code == 200:
                    data = response.json()
                    model_count = len(data.get("data", []))
                    results["openai"] = {"status": "connected", "model_count": model_count}
                    print(f"    ✅ Connected - {model_count} models available")
                else:
                    results["openai"] = {"status": "error", "code": response.status_code}
                    print(f"    ⚠️  HTTP {response.status_code}")
        except Exception as e:
            results["openai"] = {"status": "error", "error": str(e)}
            print(f"    ❌ Error: {e}")
    else:
        results["openai"] = {"status": "no_key"}
        print("\n  OpenAI: Skipped (no API key)")
    
    print("\n" + "=" * 50)
    return results


def fetch_provider_models(provider: str) -> None:
    """Fetch and display available models from a specific provider."""
    print(f"\n📋 Fetching available models from {provider}...")
    print("=" * 60)
    
    if provider == "gemini":
        models = list_gemini_models()
        if models and "error" not in models[0]:
            for m in models:
                name = m.get("name", m.get("display_name", "Unknown"))
                desc = m.get("description", "")[:80]
                methods = m.get("supported_methods", m.get("supportedGenerationMethods", []))
                print(f"\n  📌 {name}")
                if desc:
                    print(f"     {desc}")
                if methods:
                    print(f"     Methods: {', '.join(methods[:3])}")
        else:
            print(f"  ⚠️  Error: {models[0].get('error', 'Unknown error')}")
    
    elif provider == "deepseek":
        models = list_deepseek_models()
        for m in models:
            if "note" in m:
                print(f"  ℹ️  {m['note']}")
                continue
            model_id = m.get("id", "Unknown")
            desc = m.get("description", m.get("object", ""))
            print(f"  📌 {model_id}: {desc}")
    
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
        help="Run Strategy B comparative evaluation (all 4 profiles to each LLM)"
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
    
    if args.output_dir:
        run_evaluation(args.output_dir, args.models)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
