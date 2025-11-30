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
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
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
    """
    configs = {}
    
    # DeepSeek - correct endpoint per docs: https://api.deepseek.com/chat/completions
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if deepseek_key:
        configs["deepseek"] = LLMConfig(
            name="DeepSeek Chat",
            base_url="https://api.deepseek.com/chat/completions",  # Correct endpoint (no /v1)
            api_key=deepseek_key,
            model="deepseek-chat",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {deepseek_key}"
            }
        )
        # Also add deepseek-reasoner as a separate option
        configs["deepseek-reasoner"] = LLMConfig(
            name="DeepSeek Reasoner",
            base_url="https://api.deepseek.com/chat/completions",
            api_key=deepseek_key,
            model="deepseek-reasoner",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {deepseek_key}"
            }
        )
    
    # Gemini - using SDK or REST API
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        configs["gemini"] = LLMConfig(
            name="Gemini 2.5 Flash",
            base_url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}",
            api_key=gemini_key,
            model="gemini-2.5-flash",  # Stable multimodal model
            headers={
                "Content-Type": "application/json"
            }
        )
    
    # Claude (Anthropic)
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if anthropic_key:
        configs["claude"] = LLMConfig(
            name="Claude Sonnet 4.5",
            base_url="https://api.anthropic.com/v1/messages",
            api_key=anthropic_key,
            model="claude-sonnet-4-20250514",
            headers={
                "Content-Type": "application/json",
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01"
            }
        )
    
    # OpenAI
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_key:
        configs["openai"] = LLMConfig(
            name="GPT-4o",
            base_url="https://api.openai.com/v1/chat/completions",
            api_key=openai_key,
            model="gpt-4o",
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
    Model: deepseek-chat
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
        with httpx.Client(timeout=60.0) as client:
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
                return {"error": "Failed to parse JSON", "raw_response": content}
                
    except Exception as e:
        return {"error": str(e)}


def call_gemini(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """
    Call Gemini API using the Python SDK if available, otherwise REST API.
    
    SDK: google-generativeai
    Model: gemini-pro (or other available models)
    """
    # Try SDK first (preferred method)
    if GENAI_AVAILABLE and genai is not None:
        try:
            genai.configure(api_key=config.api_key)
            model = genai.GenerativeModel(config.model)
            
            full_prompt = f"You are an expert at evaluating NLP extraction quality. Always respond with valid JSON.\n\n{prompt}"
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
                return {"error": "Failed to parse JSON", "raw_response": content}
                
        except Exception as e:
            return {"error": f"SDK error: {str(e)}"}
    
    # Fallback to REST API
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"You are an expert at evaluating NLP extraction quality. Always respond with valid JSON.\n\n{prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 2000
        }
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                config.base_url,
                headers=config.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract content from Gemini response
            content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # Parse JSON from response
            try:
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                return json.loads(content.strip())
            except json.JSONDecodeError:
                return {"error": "Failed to parse JSON", "raw_response": content}
                
    except Exception as e:
        return {"error": str(e)}


def call_claude(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """Call Claude API."""
    payload = {
        "model": config.model,
        "max_tokens": 2000,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "system": "You are an expert at evaluating NLP extraction quality. Always respond with valid JSON."
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
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
                return {"error": "Failed to parse JSON", "raw_response": content}
                
    except Exception as e:
        return {"error": str(e)}


def call_openai(config: LLMConfig, prompt: str) -> dict[str, Any]:
    """Call OpenAI API."""
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": "You are an expert at evaluating NLP extraction quality. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
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
                return {"error": "Failed to parse JSON", "raw_response": content}
                
    except Exception as e:
        return {"error": str(e)}


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
    
    if args.output_dir:
        run_evaluation(args.output_dir, args.models)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
