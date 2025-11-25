#!/usr/bin/env python3
"""
integrate_llm_enhancements.py - V2 Interactive Metadata-First

Integrate LLM-generated enhancements using the interactive metadata-first approach.
This version uses two-phase analysis for efficient token usage and smarter analysis.

V2 Changes:
- Uses AnalysisOrchestrator for two-phase LLM workflow
- Phase 1: Metadata analysis → content requests (~10K tokens)
- Phase 2: Targeted content → scholarly annotation (~50K tokens)
- Reduces token usage from 3.6M to ~60K per chapter
- LLM-guided content selection (smarter than keyword matching)

V1 (comprehensive approach) preserved in: integrate_llm_enhancements_v1_comprehensive.py
"""

import json
import re
import os
import logging
import traceback
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"llm_enhancement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Create logger
logger = logging.getLogger('integrate_llm')
logger.setLevel(logging.DEBUG)

# File handler - detailed logs
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Console handler - important messages only
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info(f"Logging initialized - log file: {LOG_FILE}")

# Note: Set OPENAI_API_KEY environment variable before running

# Import simplified LLM function (still used for summary enhancement)
try:
    from workflows.shared.llm_integration import call_llm
    LLM_AVAILABLE = True
    logger.info("✓ LLM integration loaded successfully")
except ImportError as e:
    LLM_AVAILABLE = False
    logger.error(f"✗ LLM integration failed to load: {e}")

# Import new interactive system (V3 with hybrid prompt quality enforcement)
# UPDATED: Now using TwoPhaseOrchestrator from refactored phases package
try:
    from workflows.llm_enhancement.scripts.metadata_extraction_system import MetadataServiceFactory
    # REFACTORED: Use TwoPhaseOrchestrator from shared/phases (migrated location)
    from workflows.shared.phases import TwoPhaseOrchestrator
    INTERACTIVE_SYSTEM_AVAILABLE = True
    logger.info("✓ Interactive system loaded successfully (using TwoPhaseOrchestrator)")
except ImportError as e:
    INTERACTIVE_SYSTEM_AVAILABLE = False
    logger.error(f"✗ Interactive system failed to load: {e}")
    print(f"Warning: Interactive system not available, will use fallback: {e}")

# Global orchestrator (singleton pattern for efficiency)
_orchestrator = None

REPO_ROOT = Path(__file__).parent.parent.parent.parent
GUIDELINES_FILE = REPO_ROOT / "workflows" / "base_guideline_generation" / "output" / "chapter_summaries" / "PYTHON_GUIDELINES_Learning_Python_Ed6.md"
JSON_DIR = REPO_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
TAXONOMY_DATA = None  # Will be loaded from --taxonomy argument

# Regex pattern constants (to avoid duplication)
CHAPTER_TITLE_PATTERN = r'## Chapter \d+:\s*(.+)'
CHAPTER_SUMMARY_PATTERN = r'### Chapter Summary\s*\n([^#]+)(?=\n###|\n##|$)'

def get_or_create_orchestrator() -> Optional[TwoPhaseOrchestrator]:
    """Get or create the global orchestrator instance (singleton pattern).
    
    Pattern: Singleton (Python Essential Reference Ch. 7)
    Ensures we only initialize the metadata service once for efficiency.
    
    UPDATED: Now returns TwoPhaseOrchestrator (Sprint 1 Day 1-2 refactoring)
    """
    global _orchestrator
    
    if _orchestrator is None and INTERACTIVE_SYSTEM_AVAILABLE:
        logger.info("Initializing two-phase orchestrator (refactored architecture)...")
        print("Initializing two-phase orchestrator...")
        try:
            metadata_service = MetadataServiceFactory.create_default()
            _orchestrator = TwoPhaseOrchestrator(metadata_service)
            logger.info("✓ TwoPhaseOrchestrator initialized successfully")
            print("✓ System ready (using refactored architecture)")
        except Exception as e:
            logger.error(f"✗ Failed to initialize orchestrator: {e}")
            logger.debug(traceback.format_exc())
            print(f"ERROR: Failed to initialize system: {e}")
            return None
    
    return _orchestrator

def load_companion_books():
    """Load all companion book JSON files from Textbooks_JSON directory."""
    companion_data = {}
    
    logger.info(f"Loading companion books from: {JSON_DIR}")
    
    if not JSON_DIR.exists():
        logger.error(f"✗ JSON directory not found: {JSON_DIR}")
        print(f"Warning: JSON directory not found: {JSON_DIR}")
        return companion_data
        
    print(f"Loading from: {JSON_DIR}")
    
    for json_file in JSON_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                book_name = json_file.stem
                companion_data[book_name] = data
                pages_count = len(data.get('pages', []))
                logger.debug(f"  Loaded {pages_count} pages from {book_name}")
                print(f"  Loaded {pages_count} pages from {book_name}")
        except Exception as e:
            logger.error(f"  ✗ Error loading {json_file}: {e}")
            print(f"  Error loading {json_file}: {e}")
    
    logger.info(f"✓ Loaded {len(companion_data)} companion books successfully")
    return companion_data

def _find_matching_concepts_in_content(chapter_concepts: List[str], content: str) -> List[Dict]:
    """Find matching concepts in content and return match details."""
    matching_concepts = []
    content_lower = content.lower()
    
    for concept in chapter_concepts:
        concept_lower = concept.lower()
        if concept_lower in content_lower:
            occurrences = content_lower.count(concept_lower)
            matching_concepts.append({
                'concept': concept,
                'occurrences': occurrences
            })
    
    return matching_concepts


# Removed unused find_relevant_sections function (dead code, never called)
# Was causing F811 redefinition warning

def extract_chapter_1_to_10(content: str) -> Tuple[str, str, str]:
    """Extract header, chapters 1-10, and remainder."""
    lines = content.split('\n')
    
    chapter_1_start = None
    chapter_11_start = None
    
    for i, line in enumerate(lines):
        if line.startswith("## Chapter 1:"):
            chapter_1_start = i
        elif line.startswith("## Chapter 11:"):
            chapter_11_start = i
            break
    
    if chapter_1_start is None:
        return "", content, ""
    
    if chapter_11_start is None:
        chapter_11_start = len(lines)
    
    header = '\n'.join(lines[:chapter_1_start])
    chapters_1_10 = '\n'.join(lines[chapter_1_start:chapter_11_start])
    remainder = '\n'.join(lines[chapter_11_start:])
    
    return header, chapters_1_10, remainder

def _build_taxonomy_context() -> str:
    """Extract taxonomy structure into formatted context string.
    
    Service Layer Pattern: Separates taxonomy formatting logic from orchestration.
    Reduces complexity by extracting nested iteration logic.
    
    Returns:
        Formatted taxonomy context string, or empty string if unavailable
    """
    if not TAXONOMY_DATA or 'tiers' not in TAXONOMY_DATA:
        return ""
    
    context = "\n\nTAXONOMY STRUCTURE (concept hierarchy and relationships):\n"
    for tier_name, tier_data in TAXONOMY_DATA['tiers'].items():
        if isinstance(tier_data, dict):
            priority = tier_data.get('priority', '?')
            concepts = tier_data.get('concepts', [])
            if concepts:
                context += f"\n{tier_name.title()} (Priority {priority}):\n"
                context += f"  Concepts: {', '.join(concepts[:10])}"
                if len(concepts) > 10:
                    context += f" ... ({len(concepts)} total)"
                context += "\n"
    
    context += "\nUse this taxonomy to identify which tier this chapter's concepts belong to and suggest appropriate cross-references within the same or related tiers.\n"
    return context


def _build_enhancement_prompt(current_summary: str, chapter_num: int, chapter_title: str, taxonomy_context: str) -> str:
    """Build LLM prompt for summary enhancement.
    
    Service Layer Pattern: Encapsulates prompt construction logic.
    Single responsibility: prompt formatting only.
    
    Args:
        current_summary: Existing chapter summary text
        chapter_num: Chapter number
        chapter_title: Chapter title
        taxonomy_context: Formatted taxonomy structure (may be empty)
        
    Returns:
        Complete LLM prompt string
    """
    prompt = f"""
You are enhancing a Python education document chapter summary. 

CURRENT SUMMARY:
{current_summary}

CHAPTER: {chapter_num} - {chapter_title}
{taxonomy_context}
TASK: Enhance this summary by adding 2-3 specific cross-references to related Python concepts that would appear in other parts of Learning Python or companion books. 

GUIDELINES:
1. Keep the existing content
2. Add specific mentions like "relates to Chapter X on [topic]" or "builds toward [advanced concept]"
3. Add 1-2 practical applications or real-world connections
4. Maintain the academic tone and reference style
5. Keep the same footnote reference at the end
6. If taxonomy is provided, use it to identify concept relationships and suggest cross-references within appropriate tiers

ENHANCED SUMMARY:
"""
    return prompt


def _replace_summary_in_content(chapter_content: str, enhanced_summary: str) -> str:
    """Replace chapter summary in content with enhanced version.
    
    Service Layer Pattern: Isolates regex replacement logic.
    Single responsibility: summary substitution only.
    
    Args:
        chapter_content: Full chapter content
        enhanced_summary: Enhanced summary text from LLM
        
    Returns:
        Chapter content with enhanced summary
    """
    new_content = re.sub(
        r'(### Chapter Summary\s*\n)([^#]+)(?=\n###|\n##|$)',
        f"\\1{enhanced_summary}\n\n",
        chapter_content,
        count=1,
        flags=re.DOTALL
    )
    return new_content


def enhance_chapter_summary_with_llm(chapter_content: str, chapter_num: int) -> str:
    """Use LLM to enhance a chapter summary with cross-references.
    
    Orchestration Function (Service Layer Pattern): Coordinates enhancement workflow
    by delegating to specialized service functions. Reduced from CC 13 to CC <10
    through Extract Method refactoring.
    
    Architecture: Following Service Layer pattern (Architecture Patterns Ch. 4)
    - Thin orchestration layer
    - Delegates to domain services: _build_taxonomy_context, _build_enhancement_prompt, _replace_summary_in_content
    - Single responsibility: workflow coordination only
    
    Args:
        chapter_content: Full chapter markdown content
        chapter_num: Chapter number for context
        
    Returns:
        Enhanced chapter content, or original if enhancement fails
    """
    if not LLM_AVAILABLE:
        return chapter_content
    
    # Extract current summary
    summary_match = re.search(CHAPTER_SUMMARY_PATTERN, chapter_content, re.DOTALL)
    if not summary_match:
        return chapter_content
    
    current_summary = summary_match.group(1).strip()
    
    # Extract chapter title
    title_match = re.search(CHAPTER_TITLE_PATTERN, chapter_content)
    chapter_title = title_match.group(1) if title_match else f"Chapter {chapter_num}"
    
    # Build context and prompt using service functions
    taxonomy_context = _build_taxonomy_context()
    prompt = _build_enhancement_prompt(current_summary, chapter_num, chapter_title, taxonomy_context)
    
    try:
        enhanced_summary = call_llm(prompt, max_tokens=500)
        
        # Validate response quality
        enhanced_summary = enhanced_summary.strip()
        if enhanced_summary and len(enhanced_summary) > len(current_summary) * 0.8:
            return _replace_summary_in_content(chapter_content, enhanced_summary)
            
    except Exception as e:
        print(f"  LLM enhancement failed for Chapter {chapter_num}: {e}")
    
    return chapter_content

# Removed duplicate unused find_relevant_sections function (F811)
# Function was defined twice (lines 164 and 288) but never called

def add_cross_reference_section_comprehensive(
    chapter_content: str,
    chapter_num: int,
    _companion_data: Dict  # Unused - kept for API compatibility
) -> str:
    """Add cross-reference section using V2 Interactive Metadata-First system.
    
    V2 MIGRATION: Replaces old comprehensive approach with two-phase orchestrated analysis.
    - Phase 1: Metadata extraction and LLM-guided content requests (~10K tokens)
    - Phase 2: Targeted content retrieval and scholarly annotation (~50K tokens)
    Total: ~60K tokens vs v1's 107K+ tokens (400x more efficient than sending 3.6M token corpus)
    
    Pattern: Orchestration (Building Microservices Ch. 4, Microservice APIs Ch. 6)
    Uses: AnalysisOrchestrator for state management, MetadataServiceFactory for DDD
    """
    # Check if interactive system is available
    orchestrator = get_or_create_orchestrator()
    if not orchestrator:
        logger.warning(f"Interactive system unavailable, skipping Chapter {chapter_num}")
        print(f"  Interactive system unavailable, skipping Chapter {chapter_num}")
        return chapter_content
    
    # Extract chapter metadata
    title_match = re.search(CHAPTER_TITLE_PATTERN, chapter_content)
    chapter_title = title_match.group(1) if title_match else f"Chapter {chapter_num}"
    
    logger.info(f"Processing Chapter {chapter_num}: {chapter_title}")
    
    # Extract full chapter text (everything between this chapter and next chapter)
    chapter_pattern = rf'## Chapter {chapter_num}:.*?(?=## Chapter {chapter_num + 1}:|$)'
    chapter_match = re.search(chapter_pattern, chapter_content, re.DOTALL)
    full_chapter_text = chapter_match.group(0) if chapter_match else chapter_content
    
    # SCENARIO 2: LLM-driven comprehensive analysis
    # LLM reads full chapter → extracts concepts → reviews companion books → requests chapters
    print(f"  Running COMPREHENSIVE analysis for Chapter {chapter_num}...")
    logger.info(f"  Full chapter text: {len(full_chapter_text)} characters")
    print(f"  Full chapter text: {len(full_chapter_text)} characters")
    
    try:
        annotation = orchestrator.analyze_chapter_comprehensive(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            chapter_full_text=full_chapter_text
        )
        
        if annotation:
            logger.info(f"✓ Generated annotation for Chapter {chapter_num}: {len(annotation.annotation_text)} chars")
            # Format the scholarly annotation into document structure
            cross_ref_section = f"""
### Cross-Text Analysis

**Scholarly Annotation with Companion Books**

{annotation.annotation_text}

*Sources: {', '.join(annotation.sources_cited)}*
*Concepts Validated: {', '.join(annotation.concepts_validated)}*
{f"*Gaps Identified: {', '.join(annotation.gaps_identified)}*" if annotation.gaps_identified else ""}

"""
            
            # Insert into document structure
            insertion_match = re.search(r'(### Concept-by-Concept Breakdown.*?)(\n### Chapter Summary)', chapter_content, re.DOTALL)
            if insertion_match:
                before_section = insertion_match.group(1)
                start_pos = chapter_content.find(before_section)
                end_pos = start_pos + len(before_section)
                
                return (chapter_content[:end_pos] + 
                       cross_ref_section + 
                       chapter_content[end_pos:])
            else:
                # Fallback: insert before chapter summary
                summary_match = re.search(r'(\n### Chapter Summary)', chapter_content)
                if summary_match:
                    insertion_point = summary_match.start()
                    return (chapter_content[:insertion_point] + 
                           cross_ref_section + 
                           chapter_content[insertion_point:])
        else:
            logger.warning(f"  No annotation generated for Chapter {chapter_num}")
            print(f"  No annotation generated for Chapter {chapter_num}")
                
    except Exception as e:
        logger.error(f"  ✗ Analysis failed for Chapter {chapter_num}: {e}")
        logger.debug(traceback.format_exc())
        print(f"  Analysis failed for Chapter {chapter_num}: {e}")
    
    return chapter_content

def _perform_critical_checks(companion_data: Dict, orchestrator) -> int:
    """Perform all critical pre-flight checks. Returns 0 on success, 1 on failure."""
    # CRITICAL CHECK 1: LLM availability
    if not LLM_AVAILABLE:
        logger.error("✗ CRITICAL: LLM not available. Check API keys.")
        print("❌ CRITICAL ERROR: LLM not available. Check API keys.")
        print("   Set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable")
        return 1
    
    # CRITICAL CHECK 2: Interactive system availability
    if not INTERACTIVE_SYSTEM_AVAILABLE:
        logger.error("✗ CRITICAL: Interactive system not available")
        print("❌ CRITICAL ERROR: Interactive system not available")
        print("   Required modules: metadata_extraction_system, interactive_llm_system_v3_hybrid_prompt")
        return 1
    
    # CRITICAL CHECK 3: Companion books loaded
    if not companion_data:
        logger.error("✗ CRITICAL: No companion book data loaded.")
        print("❌ CRITICAL ERROR: No companion book data loaded.")
        print(f"   Check that JSON files exist in: {JSON_DIR}")
        return 1
    
    # CRITICAL CHECK 4: Minimum number of books
    if len(companion_data) < 10:
        logger.error(f"✗ CRITICAL: Only {len(companion_data)} books loaded (expected 14)")
        print(f"❌ CRITICAL ERROR: Only {len(companion_data)} books loaded (expected 14)")
        print(f"   Check JSON directory: {JSON_DIR}")
        return 1
    
    # CRITICAL CHECK 6: Orchestrator initialization
    if not orchestrator:
        logger.error("✗ CRITICAL: Failed to initialize orchestrator")
        print("❌ CRITICAL ERROR: Failed to initialize orchestrator")
        print("   The metadata service could not load book metadata")
        print(f"   Check that Textbooks_JSON directory has valid JSON files: {JSON_DIR}")
        return 1
    
    # CRITICAL CHECK 7: Verify orchestrator can see books
    try:
        books_metadata = orchestrator._legacy_orchestrator._build_books_metadata_only()
        if len(books_metadata) == 0:
            logger.error("✗ CRITICAL: Orchestrator loaded but found 0 books in metadata")
            print("❌ CRITICAL ERROR: Orchestrator found 0 books in metadata")
            print("   This is the issue you saw before: 'Book metadata for 0 books'")
            print("   Check MetadataServiceFactory paths in metadata_extraction_system.py")
            return 1
        logger.info(f"✓ Orchestrator can access {len(books_metadata)} books")
        print(f"✓ Orchestrator validated: {len(books_metadata)} books accessible")
    except Exception as e:
        logger.error(f"✗ CRITICAL: Failed to validate orchestrator: {e}")
        logger.debug(traceback.format_exc())
        print(f"❌ CRITICAL ERROR: Failed to validate orchestrator: {e}")
        return 1
    
    return 0


def _load_and_validate_guidelines() -> tuple[Optional[str], int]:
    """Load guidelines file and perform validation. Returns (content, exit_code)."""
    logger.info(f"Loading {GUIDELINES_FILE.name}...")
    print(f"Loading {GUIDELINES_FILE.name}...")
    
    # CRITICAL CHECK 5: Input file exists
    if not GUIDELINES_FILE.exists():
        logger.error(f"✗ CRITICAL: Guidelines file not found: {GUIDELINES_FILE}")
        print("❌ CRITICAL ERROR: Guidelines file not found")
        print(f"   Expected: {GUIDELINES_FILE}")
        return None, 1
    
    try:
        with open(GUIDELINES_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"✓ Loaded guidelines file: {len(content)} characters")
        return content, 0
    except Exception as e:
        logger.error(f"✗ CRITICAL: Failed to read guidelines file: {e}")
        logger.debug(traceback.format_exc())
        print(f"❌ CRITICAL ERROR: Failed to read guidelines file: {e}")
        return None, 1


def _extract_chapters_from_content(content: str) -> tuple[str, str, List[int], int]:
    """Extract chapters from content. Returns (header, chapters_content, chapter_list, exit_code)."""
    # Extract header (everything before Chapter 1)
    header_match = re.search(r'(.*)(?=## Chapter 1:)', content, re.DOTALL)
    header = header_match.group(1) if header_match else ""
    chapters_content = content[len(header):]
    
    logger.info(f"Loaded full document: {len(content.split())} words")
    print(f"Loaded full document: {len(content.split())} words")
    
    # Extract all chapter numbers
    chapter_pattern = r'## Chapter (\d+):'
    all_chapters = sorted([int(m.group(1)) for m in re.finditer(chapter_pattern, chapters_content)])
    
    # CRITICAL CHECK 8: Chapters found
    if not all_chapters:
        logger.error("✗ CRITICAL: No chapters found in document")
        print("❌ CRITICAL ERROR: No chapters found in document")
        print("   Check that the markdown file has chapters formatted as '## Chapter N:'")
        return header, chapters_content, [], 1
    
    logger.info(f"Found {len(all_chapters)} chapters (Chapter {all_chapters[0]} - Chapter {all_chapters[-1]})")
    print(f"\n📋 Found {len(all_chapters)} chapters (Chapter {all_chapters[0]} - Chapter {all_chapters[-1]})")
    
    # LIMIT TO CHAPTERS 1-10 FOR TESTING
    all_chapters = [ch for ch in all_chapters if 1 <= ch <= 10]
    logger.info(f"LIMITING to chapters 1-10 for testing: {all_chapters}")
    print(f"⚠️  LIMITING to chapters 1-10 for testing: {all_chapters}")
    
    return header, chapters_content, all_chapters, 0


def _test_first_chapter(orchestrator, chapters_content: str, test_chapter_num: int) -> int:
    """Test first chapter to validate workflow. Returns 0 on success, 1 on failure."""
    print(f"\n🧪 RUNNING TEST on Chapter {test_chapter_num} to validate workflow...")
    logger.info(f"Running test on Chapter {test_chapter_num} to validate workflow before processing all chapters")
    
    chapter_pattern = rf'(## Chapter {test_chapter_num}:.*?)(?=## Chapter {test_chapter_num + 1}:|$)'
    chapter_match = re.search(chapter_pattern, chapters_content, re.DOTALL)
    
    if not chapter_match:
        logger.error(f"✗ CRITICAL: Could not extract test chapter {test_chapter_num}")
        print(f"❌ CRITICAL ERROR: Could not extract test chapter {test_chapter_num}")
        return 1
    
    test_chapter_content = chapter_match.group(1)
    
    try:
        print(f"   Testing LLM enhancement on Chapter {test_chapter_num}...")
        logger.info(f"   Testing LLM enhancement on Chapter {test_chapter_num}...")
        
        # Extract chapter metadata
        title_match = re.search(CHAPTER_TITLE_PATTERN, test_chapter_content)
        chapter_title = title_match.group(1) if title_match else f"Chapter {test_chapter_num}"
        
        # Extract full chapter text
        chapter_pattern = rf'## Chapter {test_chapter_num}:.*?(?=## Chapter {test_chapter_num + 1}:|$)'
        chapter_match = re.search(chapter_pattern, test_chapter_content, re.DOTALL)
        full_chapter_text = chapter_match.group(0) if chapter_match else test_chapter_content
        
        # Try to run the analysis
        annotation = orchestrator.analyze_chapter_comprehensive(
            chapter_num=test_chapter_num,
            chapter_title=chapter_title,
            chapter_full_text=full_chapter_text
        )
        
        if not annotation:
            logger.error("✗ CRITICAL: Test chapter returned no annotation")
            print("❌ CRITICAL ERROR: Test chapter returned no annotation")
            print("   The LLM workflow is not working correctly")
            return 1
        
        if len(annotation.annotation_text) < 100:
            logger.error(f"✗ CRITICAL: Test annotation too short ({len(annotation.annotation_text)} chars)")
            print(f"❌ CRITICAL ERROR: Test annotation too short ({len(annotation.annotation_text)} chars)")
            print(f"   Expected substantial annotation, got: {annotation.annotation_text[:200]}")
            return 1
        
        logger.info(f"✓ Test successful: Generated {len(annotation.annotation_text)} char annotation")
        print(f"✓ TEST PASSED: Generated {len(annotation.annotation_text)} char annotation")
        print(f"✓ Sources cited: {len(annotation.sources_cited)}")
        print("✓ Ready to process all chapters")
        return 0
        
    except Exception as e:
        logger.error(f"✗ CRITICAL: Test chapter failed: {e}")
        logger.debug(traceback.format_exc())
        print("❌ CRITICAL ERROR: Test chapter failed")
        print(f"   Error: {e}")
        print("   Cannot proceed - would waste tokens on all chapters")
        print(f"   Check the log file for details: {LOG_FILE}")
        return 1


def _process_single_chapter(chapter_num: int, chapters_content: str, companion_data: Dict,
                           all_chapters: List[int]) -> Tuple[Optional[str], bool]:
    """
    Process a single chapter with LLM enhancement.
    
    Returns:
        (enhanced_chapter, success_flag) tuple
    """
    print(f"\n{'='*70}")
    print(f"[Chapter {chapter_num}/{all_chapters[-1]}] Enhancing...")
    print(f"{'='*70}")
    logger.info(f"{'='*70}")
    logger.info(f"Processing Chapter {chapter_num}/{all_chapters[-1]}")
    logger.info(f"{'='*70}")
    
    # Extract individual chapter
    chapter_pattern = rf'(## Chapter {chapter_num}:.*?)(?=## Chapter {chapter_num + 1}:|$)'
    chapter_match = re.search(chapter_pattern, chapters_content, re.DOTALL)
    
    if not chapter_match:
        logger.warning(f"  Could not find Chapter {chapter_num}")
        print(f"  Warning: Could not find Chapter {chapter_num}")
        return None, False
    
    chapter_content = chapter_match.group(1)
    
    try:
        # Enhance summary
        logger.info(f"  Enhancing summary for Chapter {chapter_num}...")
        print("  Enhancing summary...")
        enhanced_chapter = enhance_chapter_summary_with_llm(chapter_content, chapter_num)
        
        # Add cross-references
        logger.info(f"  Performing comprehensive cross-text analysis for Chapter {chapter_num}...")
        print("  Performing comprehensive cross-text analysis...")
        enhanced_chapter = add_cross_reference_section_comprehensive(enhanced_chapter, chapter_num, companion_data)
        
        has_cross_refs = "### Cross-Text Analysis" in enhanced_chapter
        if has_cross_refs:
            logger.info(f"  ✓ Cross-references added to Chapter {chapter_num}")
        else:
            logger.warning(f"  No cross-references added to Chapter {chapter_num}")
        
        logger.info(f"✓ Chapter {chapter_num} processing complete")
        return (chapter_content, enhanced_chapter), has_cross_refs
        
    except Exception as e:
        logger.error(f"✗ Failed to process Chapter {chapter_num}: {e}")
        logger.debug(traceback.format_exc())
        print(f"  ERROR: Failed to process Chapter {chapter_num}: {e}")
        return None, False


def _process_all_chapters(header: str, chapters_content: str, all_chapters: List[int],
                         companion_data: Dict) -> Tuple[str, int, List[int], int]:
    """
    Process all chapters with LLM enhancement.
    
    Returns:
        (enhanced_content, chapters_with_cross_refs, failed_chapters, exit_code)
    """
    enhanced_content = chapters_content
    chapters_with_cross_refs = 0
    failed_chapters = []
    consecutive_failures = 0
    MAX_CONSECUTIVE_FAILURES = 3
    
    for chapter_num in all_chapters:
        result, success = _process_single_chapter(chapter_num, chapters_content, companion_data, all_chapters)
        
        if result is None:
            failed_chapters.append(chapter_num)
            consecutive_failures += 1
        else:
            chapter_content, enhanced_chapter = result
            enhanced_content = enhanced_content.replace(chapter_content, enhanced_chapter)
            if success:
                chapters_with_cross_refs += 1
                consecutive_failures = 0
            else:
                consecutive_failures += 1
        
        # Check for too many consecutive failures
        if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
            logger.error(f"✗ CRITICAL: {MAX_CONSECUTIVE_FAILURES} consecutive failures - stopping")
            print(f"\n❌ CRITICAL: {MAX_CONSECUTIVE_FAILURES} consecutive failures detected")
            print(f"   Failed chapters: {failed_chapters[-MAX_CONSECUTIVE_FAILURES:]}")
            print("   Stopping to prevent wasting tokens")
            print(f"   Check the log file: {LOG_FILE}")
            
            # Save partial results if any were successful
            if chapters_with_cross_refs > 0:
                _save_partial_results(header, enhanced_content, chapters_with_cross_refs)
            
            return enhanced_content, chapters_with_cross_refs, failed_chapters, 1
    
    return enhanced_content, chapters_with_cross_refs, failed_chapters, 0


def _save_partial_results(header: str, enhanced_content: str, chapters_with_cross_refs: int):
    """Save partial results when processing is interrupted."""
    enhanced_document = header + enhanced_content
    output_filename = "PYTHON_GUIDELINES_Learning_Python_Ed6_LLM_ENHANCED_PARTIAL.md"
    output_dir = REPO_ROOT / "workflows" / "llm_enhancement" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    partial_file = output_dir / output_filename
    with open(partial_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_document)
    print(f"   💾 Saved partial results ({chapters_with_cross_refs} chapters) to: {partial_file}")
    logger.info(f"Saved partial results to: {partial_file}")


def main():
    """Main entry point. Refactored to reduce cognitive complexity."""
    print("="*66)
    print("Comprehensive LLM Enhancement with All Companion Books")
    print("="*66)
    
    logger.info("="*66)
    logger.info("Starting LLM Enhancement Workflow")
    logger.info("="*66)
    
    # Load companion book data
    print("Loading companion book JSON files from Textbooks_JSON:")
    logger.info("Loading companion book JSON files from Textbooks_JSON:")
    companion_data = load_companion_books()
    
    total_books = len(companion_data)
    total_pages = sum(len(book_data.get('pages', [])) for book_data in companion_data.values())
    logger.info(f"Successfully loaded {total_books} companion books with {total_pages} total pages")
    print(f"\n📚 Successfully loaded {total_books} companion books with {total_pages} total pages")
    print(f"Using {os.getenv('LLM_PROVIDER', 'anthropic').upper()} for comprehensive analysis")
    
    # Load guidelines
    content, exit_code = _load_and_validate_guidelines()
    if exit_code != 0:
        return exit_code
    
    # Initialize orchestrator
    print("\nInitializing LLM orchestrator (this validates book metadata loading)...")
    orchestrator = get_or_create_orchestrator()
    
    # Perform all critical checks
    exit_code = _perform_critical_checks(companion_data, orchestrator)
    if exit_code != 0:
        return exit_code
    
    # Extract chapters
    header, chapters_content, all_chapters, exit_code = _extract_chapters_from_content(content)
    if exit_code != 0:
        return exit_code
    
    # Test first chapter
    exit_code = _test_first_chapter(orchestrator, chapters_content, all_chapters[0])
    if exit_code != 0:
        return exit_code
    
    # All critical checks passed
    print("\n✅ ALL CRITICAL CHECKS PASSED")
    print(f"🚀 Proceeding with full enhancement of {len(all_chapters)} chapters...")
    logger.info("✅ ALL CRITICAL CHECKS PASSED - Proceeding with full enhancement")
    
    user_confirm = input(f"\n⚠️  This will make ~{len(all_chapters) * 2} API calls (~{len(all_chapters) * 60_000} tokens). Continue? [y/N]: ")
    if user_confirm.lower() != 'y':
        print("❌ Enhancement cancelled by user")
        logger.info("Enhancement cancelled by user")
        return 0
    
    print("🔄 Processing ALL chapters with LLM enhancement...")
    
    # Process all chapters
    enhanced_content, chapters_with_cross_refs, failed_chapters, exit_code = _process_all_chapters(
        header, chapters_content, all_chapters, companion_data
    )
    
    if exit_code != 0:
        return exit_code
    
    # Reconstruct the full document
    enhanced_document = header + enhanced_content
    
    # Save enhanced version to workflow output directory
    output_filename = "PYTHON_GUIDELINES_Learning_Python_Ed6_LLM_ENHANCED.md"
    output_dir = REPO_ROOT / "workflows" / "llm_enhancement" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    enhanced_file = output_dir / output_filename
    
    try:
        # Save enhanced version
        with open(enhanced_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_document)
        logger.info(f"✓ Enhanced version saved to: {enhanced_file}")
    except Exception as e:
        logger.error(f"✗ Failed to save enhanced version: {e}")
        logger.debug(traceback.format_exc())
        print(f"ERROR: Failed to save enhanced version: {e}")
        return 1
    
    print(f"\n{'='*70}")
    print("✅ Enhancement complete!")
    print(f"{'='*70}")
    logger.info(f"{'='*70}")
    logger.info("Enhancement Complete - Summary")
    logger.info(f"{'='*70}")
    
    print(f"📊 Processed: {len(all_chapters)} chapters (Chapter {all_chapters[0]} - Chapter {all_chapters[-1]})")
    print(f"📊 With cross-references: {chapters_with_cross_refs} chapter(s)")
    logger.info(f"Processed: {len(all_chapters)} chapters")
    logger.info(f"Successfully enhanced: {chapters_with_cross_refs} chapters")
    
    if failed_chapters:
        logger.warning(f"Failed chapters: {failed_chapters}")
        print(f"⚠️  Failed chapters: {failed_chapters}")
    
    print(f"📄 Enhanced version saved to: {enhanced_file}")
    print(f"\nModel used: {os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929')}")
    print(f"Provider: {os.getenv('LLM_PROVIDER', 'anthropic').upper()}")
    print(f"📝 Log file: {LOG_FILE}")
    
    logger.info(f"Enhanced version saved to: {enhanced_file}")
    logger.info(f"Model: {os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929')}")
    logger.info(f"Provider: {os.getenv('LLM_PROVIDER', 'anthropic').upper()}")
    logger.info("="*66)
    
    return 0

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Integrate LLM enhancements with taxonomy-aware cross-referencing')
    parser.add_argument(
        '--guideline',
        type=str,
        help='Path to the base guideline file to enhance'
    )
    parser.add_argument(
        '--taxonomy',
        type=str,
        help='Path to taxonomy JSON file (defines concept hierarchy and relationships)'
    )
    args = parser.parse_args()
    
    # Update global paths if provided
    if args.guideline:
        GUIDELINES_FILE = Path(args.guideline)
        if not GUIDELINES_FILE.exists():
            print(f"ERROR: Guideline file not found: {GUIDELINES_FILE}")
            exit(1)
    
    # Load taxonomy if provided
    TAXONOMY_DATA = None
    if args.taxonomy:
        taxonomy_path = Path(args.taxonomy)
        if not taxonomy_path.exists():
            print(f"ERROR: Taxonomy file not found: {taxonomy_path}")
            exit(1)
        
        try:
            with open(taxonomy_path, 'r', encoding='utf-8') as f:
                TAXONOMY_DATA = json.load(f)
            print(f"✓ Loaded taxonomy: {taxonomy_path.name}")
            
            # Extract tier information for display
            if 'tiers' in TAXONOMY_DATA:
                tier_count = len(TAXONOMY_DATA['tiers'])
                print(f"  Tiers: {', '.join(TAXONOMY_DATA['tiers'].keys())} ({tier_count} total)")
        except Exception as e:
            print(f"ERROR: Failed to load taxonomy: {e}")
            exit(1)
    
    # Display startup banner
    print("\n" + "="*70)
    print("  LLM Cross-Referencing System - V2 Interactive Metadata-First")
    print("="*70)
    provider = os.getenv('LLM_PROVIDER', 'anthropic').upper()
    model = os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929') if provider == 'ANTHROPIC' else os.getenv('OPENAI_MODEL', 'gpt-5-nano')
    print(f"  Provider: {provider}")
    print(f"  Model: {model}")
    print(f"  Temperature: {os.getenv('LLM_TEMPERATURE', '0.2')}")
    print(f"  Max Tokens: {os.getenv('LLM_MAX_TOKENS', '4096')}")
    print(f"  Target: {GUIDELINES_FILE.name}")
    if TAXONOMY_DATA:
        print(f"  Taxonomy: {taxonomy_path.name}")
    print("="*70 + "\n")
    
    exit_code = main()
    exit(exit_code if exit_code is not None else 0)