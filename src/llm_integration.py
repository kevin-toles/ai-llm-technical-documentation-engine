#!/usr/bin/env python3
"""
llm_integration.py - LLM Integration Layer for Chapter Generator

This module provides AUTOMATED LLM API integration for semantic analysis.
NO user interaction required - uses API calls to OpenAI/Anthropic/local models.

Integration Points:
1. Semantic concept extraction (vs keyword matching)
2. Cross-reference validation (vs set intersection)
3. Summary composition (vs templates)
4. Pre-validation compliance checks

Usage:
    Set environment variable: OPENAI_API_KEY or ANTHROPIC_API_KEY
    The chapter generator calls these functions which make API requests automatically.
"""

print("[llm_integration] Module loading started", flush=True)

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple, Optional
from datetime import datetime
from enum import Enum

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[llm_integration] Environment variables loaded", flush=True)
except ImportError:
    print("[llm_integration] dotenv not available, using system env only", flush=True)

print("[llm_integration] Basic imports done", flush=True)

# Try to import LLM clients
try:
    print("[llm_integration] Attempting openai import...", flush=True)
    import openai
    OPENAI_AVAILABLE = True
    print("[llm_integration] openai imported successfully", flush=True)
except ImportError:
    print("[llm_integration] openai not available", flush=True)
    OPENAI_AVAILABLE = False

try:
    print("[llm_integration] Attempting anthropic import...", flush=True)
    import anthropic
    ANTHROPIC_AVAILABLE = True
    print("[llm_integration] anthropic imported successfully", flush=True)
except ImportError:
    print("[llm_integration] anthropic not available", flush=True)
    ANTHROPIC_AVAILABLE = False

print("[llm_integration] Module loading complete", flush=True)

# Display configuration on import
if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
    print(f"[llm_integration] ✓ Anthropic configured - Model: {model}", flush=True)
elif os.getenv("ANTHROPIC_API_KEY"):
    print("[llm_integration] ⚠ Anthropic API key found but anthropic module not installed", flush=True)
else:
    print("[llm_integration] ⚠ No Anthropic API key found in environment", flush=True)

# OpenAI disabled for now
if os.getenv("OPENAI_API_KEY"):
    print("[llm_integration] ℹ OpenAI API key found but provider disabled (using Anthropic)", flush=True)


# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # anthropic, openai, or local
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")  # Claude Sonnet 4.5
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")  # Disabled for now
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))  # Low temp for factual analysis
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "8192"))  # Max tokens for response (Claude Sonnet 4.5 limit)

# Enable detailed API logging (set to False to disable)
ENABLE_API_LOGGING = os.getenv("ENABLE_API_LOGGING", "true").lower() == "true"

# API call counter
_api_call_count = 0


# ============================================================================
# Sprint 1 Critical Fixes (per REFACTORING_PLAN.md)
# ============================================================================

class FinishReason(Enum):
    """
    Enum for LLM finish_reason values.
    
    Per REFACTORING_PLAN.md section 1.3:
    - Provides type safety for finish_reason validation
    - Covers all possible Anthropic API stop_reason values
    
    Reference: Anthropic API docs - Message.stop_reason field
    """
    END_TURN = "end_turn"           # Normal completion
    MAX_TOKENS = "max_tokens"       # Hit token limit (truncation)
    STOP_SEQUENCE = "stop_sequence" # Hit custom stop sequence
    TOOL_USE = "tool_use"           # Tool/function call (not used in our case)


def _validate_json_response(response_text: str, finish_reason: str) -> Tuple[bool, Optional[str]]:
    """
    Validate JSON response completeness and structure.
    
    Per REFACTORING_PLAN.md section 1.1:
    - Validates finish_reason (must be "end_turn")
    - Validates JSON syntax
    - Validates structure for Phase 1 responses
    - Validates required fields
    
    Args:
        response_text: Raw LLM response text
        finish_reason: Stop reason from API response
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if response is complete and valid
        - error_message: None if valid, description if invalid
    
    Example:
        >>> is_valid, error = _validate_json_response('[{"book_title": "Test"}]', "end_turn")
    """
    # Check finish_reason first
    if finish_reason != FinishReason.END_TURN.value:
        return False, f"Incomplete response: {finish_reason}"
    
    # Attempt to parse JSON
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    
    # Validate structure (for Phase 1 responses)
    if isinstance(parsed, list):
        # Phase 1: Array of content requests
        for idx, item in enumerate(parsed):
            if not isinstance(item, dict):
                return False, f"Item {idx} is not a dict"
            
            required_fields = ["book_title", "chapter", "reason"]
            missing = [f for f in required_fields if f not in item]
            if missing:
                return False, f"Item {idx} missing fields: {missing}"
    
    return True, None


def _handle_truncated_response(
    phase: str,
    messages: List[Dict],
    attempt: int,
    max_retries: int = 2
) -> Optional[str]:
    """
    Handle truncated responses with progressive constraint tightening.
    
    Per REFACTORING_PLAN.md section 1.1:
    - Phase 1: Retryable with progressive constraints (15 -> 10 -> 5 -> 3 books)
    - Phase 2: Not retryable (would lose actual content)
    - Max retries limit to prevent infinite loops
    
    Args:
        phase: "phase_1" or "phase_2"
        messages: API messages array (will be modified with constraints)
        attempt: Current retry attempt number (0-indexed)
        max_retries: Maximum number of retries allowed
        
    Returns:
        API response text if retry succeeded, None if cannot/should not retry
    
    Example:
        >>> result = _handle_truncated_response("phase_1", messages, attempt=0)
    """
    # Import here to avoid circular dependency
    from src.llm_integration import call_llm
    
    if phase == "phase_2":
        print("Phase 2 truncated - cannot retry (would lose content)", flush=True)
        return None
    
    if attempt >= max_retries:
        print(f"Max retries ({max_retries}) exceeded", flush=True)
        return None
    
    # Progressive limits: [10, 5, 3]
    limits = [10, 5, 3]
    new_limit = limits[min(attempt, len(limits) - 1)]
    
    print(f"Retry {attempt + 1}: Constraining to top {new_limit} books", flush=True)
    
    # Modify system message to add constraint
    constraint_msg = f"\n\nIMPORTANT: Limit requests to TOP {new_limit} most relevant books only."
    messages[0]["content"] += constraint_msg
    
    # Retry with modified messages (remove phase and _retry_attempt - not in signature)
    return call_llm(messages)


def _log_api_exchange(call_num: int, prompt: str, system_prompt: str, 
                      response: Optional[str], input_tokens: int, output_tokens: int, 
                      error: Optional[str] = None):
    """Log detailed API request/response to file for debugging."""
    if not ENABLE_API_LOGGING:
        return
    
    try:
        # Create logs directory if it doesn't exist
        log_dir = Path(__file__).parent.parent.parent / "logs" / "llm_api"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"api_call_{call_num:03d}_{timestamp}.json"
        
        # Format response text for logging
        response_text = None
        if response is not None:
            truncated = response[:5000]
            response_text = truncated + "..." if len(response) > 5000 else truncated
        
        log_data = {
            "call_number": call_num,
            "timestamp": datetime.now().isoformat(),
            "model": ANTHROPIC_MODEL,
            "request": {
                "system_prompt": system_prompt,
                "prompt": prompt[:5000] + ("..." if len(prompt) > 5000 else ""),  # Truncate for readability
                "prompt_length": len(prompt),
                "system_length": len(system_prompt) if system_prompt else 0
            },
            "response": {
                "text": response_text,
                "full_length": len(response) if response else 0,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            },
            "error": error
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"[LLM API] Logged to: {log_file.name}", flush=True)
        
    except Exception as e:
        print(f"[LLM API] Warning: Could not write API log: {e}", file=sys.stderr, flush=True)


def _log_request_details(call_num: int, prompt: str, system_prompt: Optional[str], max_tokens: int):
    """Log request details before making API call."""
    prompt_length = len(prompt)
    system_length = len(system_prompt) if system_prompt else 0
    estimated_input_tokens = (prompt_length + system_length) // 4
    
    print(f"\n[LLM API #{call_num}] Request: {estimated_input_tokens:,} estimated input tokens, {max_tokens:,} max output tokens", flush=True)
    if prompt_length > 100000:
        print(f"[LLM API #{call_num}] WARNING: Very large prompt ({prompt_length:,} chars)", flush=True)


def _log_response_details(call_num: int, response_text: str, input_tokens: int, output_tokens: int):
    """Log response details after receiving API response."""
    response_length = len(response_text)
    print(f"[LLM API #{call_num}] ✓ Response: {output_tokens:,} output tokens, {input_tokens:,} input tokens (actual)", flush=True)
    print(f"[LLM API #{call_num}] Response length: {response_length:,} chars", flush=True)


def _validate_response(call_num: int, response_text: str, prompt: str, system_prompt: Optional[str], 
                       input_tokens: int, output_tokens: int):
    """Validate response and log warnings."""
    if not response_text or len(response_text.strip()) == 0:
        print(f"[LLM API #{call_num}] ⚠️  WARNING: Empty response received!", file=sys.stderr, flush=True)
        _log_api_exchange(call_num, prompt, system_prompt, response_text, 
                        input_tokens, output_tokens, error="Empty response")
        return
    
    if response_text.startswith("I cannot") or response_text.startswith("I apologize"):
        print(f"[LLM API #{call_num}] ⚠️  WARNING: LLM refused or apologized - check prompt format", file=sys.stderr, flush=True)
        print(f"[LLM API #{call_num}] Response preview: {response_text[:200]}", file=sys.stderr, flush=True)
        _log_api_exchange(call_num, prompt, system_prompt, response_text, 
                        input_tokens, output_tokens, error="LLM refusal detected")


def _handle_anthropic_error(call_num: int, e: Exception, prompt: str, system_prompt: Optional[str]):
    """Handle Anthropic API errors."""
    error_msg = f"{type(e).__name__}: {str(e)}"
    print(f"\n❌ [LLM API #{call_num}] Anthropic API Error: {type(e).__name__}", file=sys.stderr, flush=True)
    print(f"   Error details: {str(e)}", file=sys.stderr, flush=True)
    if hasattr(e, 'status_code'):
        print(f"   HTTP Status: {e.status_code}", file=sys.stderr, flush=True)
    if hasattr(e, 'response'):
        print(f"   Response: {e.response}", file=sys.stderr, flush=True)
    
    _log_api_exchange(call_num, prompt, system_prompt, None, 0, 0, error=error_msg)


def call_llm(prompt: str, system_prompt: str = None, max_tokens: int = 2000) -> str:
    """
    Make automated LLM API call using Anthropic Claude (no user interaction). Refactored to reduce complexity.
    
    Args:
        prompt: User prompt
        system_prompt: Optional system prompt
        max_tokens: Maximum response tokens
    
    Returns:
        LLM response as string
    """
    global _api_call_count
    _api_call_count += 1
    call_num = _api_call_count
    
    # Try Anthropic Claude
    if LLM_PROVIDER == "anthropic" and ANTHROPIC_AVAILABLE:
        try:
            # Print confirmation on first call
            if call_num == 1:
                print(f"\n[LLM] Making API call with model: {ANTHROPIC_MODEL}", flush=True)
                if ENABLE_API_LOGGING:
                    print("[LLM] API logging enabled - saving to logs/llm_api/", flush=True)
            
            # Log request
            _log_request_details(call_num, prompt, system_prompt, max_tokens)
            
            # Make API call
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens if max_tokens <= LLM_MAX_TOKENS else LLM_MAX_TOKENS,
                temperature=LLM_TEMPERATURE,
                system=system_prompt if system_prompt else "You are a helpful assistant analyzing Python documentation.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract response
            response_text = response.content[0].text
            input_tokens = getattr(response.usage, 'input_tokens', 0)
            output_tokens = getattr(response.usage, 'output_tokens', 0)
            
            # Log response
            _log_response_details(call_num, response_text, input_tokens, output_tokens)
            _log_api_exchange(call_num, prompt, system_prompt, response_text, input_tokens, output_tokens)
            
            # Validate
            _validate_response(call_num, response_text, prompt, system_prompt, input_tokens, output_tokens)
            
            return response_text
            
        except anthropic.APIError as e:
            _handle_anthropic_error(call_num, e, prompt, system_prompt)
            raise
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"\n❌ [LLM API #{call_num}] Unexpected error calling Anthropic API: {type(e).__name__}", file=sys.stderr, flush=True)
            print(f"   Error details: {str(e)}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc()
            _log_api_exchange(call_num, prompt, system_prompt, None, 0, 0, error=error_msg)
            raise
    
    # OpenAI GPT-5 - DISABLED (using Anthropic)
    # if LLM_PROVIDER == "openai" and OPENAI_AVAILABLE:
    #     try:
    #         if not hasattr(call_llm, '_first_call_done'):
    #             print(f"\n[LLM] Making API call with model: {OPENAI_MODEL}", flush=True)
    #             call_llm._first_call_done = True
    #         
    #         client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    #         
    #         full_input = prompt
    #         if system_prompt:
    #             full_input = f"{system_prompt}\n\n{prompt}"
    #         
    #         response = client.responses.create(
    #             model=OPENAI_MODEL,
    #             input=full_input,
    #             reasoning={"effort": "high"},
    #             text={"verbosity": "medium"}
    #         )
    #         return response.output_text
    #     except Exception as e:
    #         print(f"  Warning: OpenAI API call failed: {e}", file=sys.stderr)
    
    # Fallback: return empty JSON to trigger fallback logic
    print("  Warning: No LLM provider available, using fallback logic", file=sys.stderr)
    return "{}"



def prompt_for_semantic_concepts(chapter_num: int, chapter_title: str, 
                                 page_range: Tuple[int, int],
                                 chapter_content: str,
                                 keyword_concepts: Set[str]) -> Dict[str, Any]:
    """
    AUTOMATED LLM semantic concept extraction (no user interaction).
    
    Args:
        chapter_num: Chapter number
        chapter_title: Chapter title
        page_range: (start_page, end_page)
        chapter_content: Full concatenated chapter text
        keyword_concepts: Concepts found via keyword matching (for comparison)
    
    Returns:
        Dictionary with verified and additional concepts
    """
    print(f"  LLM: Semantic concept extraction for Chapter {chapter_num}...")
    
    # Truncate content for API call (keep first 8000 chars for context)
    content_sample = chapter_content[:8000]
    if len(chapter_content) > 8000:
        content_sample += f"\n\n[... {len(chapter_content) - 8000} more characters ...]"
    
    prompt = f"""Analyze Chapter {chapter_num}: {chapter_title} (pages {page_range[0]}-{page_range[1]})

TASK: Perform semantic concept extraction

Keyword matching found these {len(keyword_concepts)} concepts:
{', '.join(sorted(keyword_concepts))}

Chapter content:
{content_sample}

Instructions:
1. VERIFY which keyword concepts are actually substantively covered (not just mentioned)
2. IDENTIFY major concepts the keywords missed (alternative terminology, implicit concepts)
3. FLAG false positives (keyword present but not a real concept)

Respond with ONLY a JSON object (no markdown, no explanation):
{{
  "verified_concepts": ["concept1", "concept2"],
  "additional_concepts": ["new_concept1"],
  "false_positives": ["false1"]
}}"""

    system_prompt = "You are an expert Python documentation analyst. Respond only with valid JSON."
    
    try:
        response = call_llm(prompt, system_prompt, max_tokens=1500)
        # Extract JSON from response (handle markdown code blocks)
        response = response.strip()
        if response.startswith("```"):
            # Remove markdown code fences
            lines = response.split("\n")
            response = "\n".join([l for l in lines if not l.startswith("```")])
        
        result = json.loads(response)
        print(f"  LLM: Verified {len(result.get('verified_concepts', []))}, found {len(result.get('additional_concepts', []))} new concepts")
        return result
    except Exception as e:
        print(f"  LLM: Error in semantic analysis: {e}", file=sys.stderr)
        return {
            "verified_concepts": list(keyword_concepts),
            "additional_concepts": [],
            "false_positives": []
        }


def prompt_for_cross_reference_validation(chapter_num: int,
                                         chapter_title: str,
                                         chapter_concepts: Set[str],
                                         keyword_matches: List[Dict[str, Any]],
                                         all_companion_books: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    AUTOMATED LLM cross-reference validation and semantic scanning (no user interaction).
    
    Phase 1: Validate keyword matches
    Phase 2: Scan ALL companion books for semantic matches
    
    Args:
        chapter_num: Chapter number
        chapter_title: Chapter title
        chapter_concepts: Verified concepts from primary chapter
        keyword_matches: List of candidate matches from keyword intersection
        all_companion_books: Dictionary of ALL companion book JSONs
    
    Returns:
        Dictionary with validated and additional matches
    """
    print(f"  LLM: Cross-reference validation for Chapter {chapter_num}...")
    
    # Build summary of keyword matches
    match_summary = []
    for i, m in enumerate(keyword_matches[:10], 1):
        match_summary.append(f"[{i}] {m['book']} p.{m['page']}: {', '.join(m.get('concepts', [])[:3])}")
    
    # Build companion book index
    book_index = []
    for book_name, book_data in all_companion_books.items():
        pages = book_data.get("pages", [])
        book_display = book_name.replace("_Content", "").replace("_", " ")
        book_index.append(f"{book_display}: {len(pages)} pages")
    
    prompt = f"""Analyze cross-references for Chapter {chapter_num}: {chapter_title}

PRIMARY CONCEPTS: {', '.join(sorted(list(chapter_concepts)[:20]))}

TASK 1: Validate {len(keyword_matches)} keyword matches
{chr(10).join(match_summary[:5])}

TASK 2: Scan ALL companion books for semantic matches
Available books:
{chr(10).join(book_index)}

Find pages that discuss the primary concepts using:
- Alternative terminology (e.g., "function" vs "callable", "list" vs "sequence")
- Implementation examples
- Architectural patterns
- Advanced coverage

Focus on matches that genuinely help understand the primary chapter.

Respond with ONLY a JSON object:
{{
  "validated_matches": [
    {{"book": "book_name", "page": 123, "concepts": ["concept1"], "content": "excerpt...", "annotation": "why valid"}}
  ],
  "additional_matches": [
    {{"book": "book_name", "page": 456, "concepts": ["concept2"], "content": "excerpt...", "how_found": "semantic match explanation"}}
  ],
  "false_positives": [
    {{"book": "book", "page": 789, "reason": "why excluded"}}
  ]
}}"""

    system_prompt = "You are a technical documentation analyst. Respond only with valid JSON."
    
    try:
        response = call_llm(prompt, system_prompt, max_tokens=3000)
        # Clean markdown if present
        response = response.strip()
        if response.startswith("```"):
            lines = response.split("\n")
            response = "\n".join([l for l in lines if not l.startswith("```")])
        
        result = json.loads(response)
        print(f"  LLM: Validated {len(result.get('validated_matches', []))}, found {len(result.get('additional_matches', []))} semantic matches")
        return result
    except Exception as e:
        print(f"  LLM: Error in cross-reference validation: {e}", file=sys.stderr)
        return {
            "validated_matches": keyword_matches[:5],
            "additional_matches": [],
            "false_positives": []
        }


def prompt_for_cross_reference_summary(concepts: List[str], 
                                       content: str, 
                                       relationship: str,
                                       book_name: str,
                                       page_num: int,
                                       max_length: int = 300) -> Dict[str, str]:
    """
    AUTOMATED LLM summary generation (no user interaction).
    
    Args:
        concepts: List of concepts to focus on
        content: Actual page content from companion book
        relationship: Type of relationship (implementation/architectural/advanced/reference)
        book_name: Name of the companion book
        page_num: Page number being summarized
        max_length: Maximum summary length
    
    Returns:
        Dictionary with summary and key points
    """
    print(f"  LLM: Summarizing {book_name} p.{page_num}...", end=" ")
    
    # Truncate content for API
    content_sample = content[:2000]
    if len(content) > 2000:
        content_sample += "..."
    
    prompt = f"""Summarize what this page says about: {', '.join(concepts[:3])}

Book: {book_name}
Page: {page_num}
Relationship: {relationship}

Page content:
{content_sample}

Create a 2-3 sentence summary (max {max_length} chars) of what THIS SPECIFIC PAGE says.
NO generic templates - actual content summary.

Respond with ONLY a JSON object:
{{
  "summary": "2-3 sentence summary of actual page content",
  "key_points": ["point 1", "point 2"]
}}"""

    system_prompt = "You are a technical documentation summarizer. Respond only with valid JSON."
    
    try:
        response = call_llm(prompt, system_prompt, max_tokens=500)
        # Clean markdown
        response = response.strip()
        if response.startswith("```"):
            lines = response.split("\n")
            response = "\n".join([l for l in lines if not l.startswith("```")])
        
        result = json.loads(response)
        print("✓")
        return result
    except Exception:
        print("✗ (using excerpt)", file=sys.stderr)
        # Fallback: extract from content
        return {
            "summary": content[:max_length].strip() + ("..." if len(content) > max_length else ""),
            "key_points": []
        }


if __name__ == "__main__":
    print("LLM Integration Module for Chapter Generator")
    print("=" * 70)
    print("\nAUTOMATED LLM API integration (no user interaction required)")
    print("\nConfiguration:")
    print(f"  LLM_PROVIDER: {LLM_PROVIDER}")
    print(f"  OpenAI available: {OPENAI_AVAILABLE}")
    print(f"  Anthropic available: {ANTHROPIC_AVAILABLE}")
    print("\nEnvironment variables:")
    print(f"  OPENAI_API_KEY: {'✓ Set' if os.getenv('OPENAI_API_KEY') else '✗ Not set'}")
    print(f"  ANTHROPIC_API_KEY: {'✓ Set' if os.getenv('ANTHROPIC_API_KEY') else '✗ Not set'}")
    print("\nIntegration points:")
    print("  1. prompt_for_semantic_concepts() - Automated semantic concept extraction")
    print("  2. prompt_for_cross_reference_validation() - Automated cross-reference validation")
    print("  3. prompt_for_cross_reference_summary() - Automated summary generation")
    print("\nSet USE_LLM_SEMANTIC_ANALYSIS=True in chapter_generator_v2.py to enable.")
