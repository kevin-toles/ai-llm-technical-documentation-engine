"""
Unified Workflow Validation Services

Provides validation for all workflow stages:
- Tab 1: PDF to JSON conversion
- Tab 2: Metadata extraction  
- Tab 3: Taxonomy generation (not currently used)
- Tab 4: Metadata enrichment
- Tab 5: Base guideline generation
- Tab 6: LLM enhancement (input aggregate + output validation)

Architecture Pattern: Facade Pattern + Strategy Pattern
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)

Each validator returns a standardized result:
{
    "passed": bool,
    "errors": List[str],
    "warnings": List[str],
    "info": List[str]
}
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@dataclass
class ValidationResult:
    """Standardized validation result across all workflows."""
    passed: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)
    
    def add_error(self, message: str):
        self.errors.append(message)
        self.passed = False
    
    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def add_info(self, message: str):
        self.info.append(message)
    
    def merge(self, other: 'ValidationResult'):
        """Merge another validation result into this one."""
        if not other.passed:
            self.passed = False
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }


class PDFConversionValidator:
    """
    Validates PDF to JSON conversion output (Tab 1).
    
    Checks:
    1. Output JSON exists
    2. Required fields present (pages, chapters, metadata)
    3. Pages have content (not empty)
    4. At least one chapter detected
    5. Page content is not just whitespace
    """
    
    MIN_PAGES_WITH_CONTENT = 5  # Expect at least 5 pages with actual content
    MIN_CONTENT_PER_PAGE = 100  # Minimum chars for a page to count as having content

    @staticmethod
    def _validate_file_and_load(output_json: Path, result: ValidationResult) -> Optional[dict]:
        """Validate file exists and load JSON data."""
        if not output_json.exists():
            result.add_error(f"Output JSON not created: {output_json.name}")
            return None
        
        result.add_info(f"Output file exists: {output_json.name}")
        
        try:
            with open(output_json) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid JSON: {e}")
            return None

    @staticmethod
    def _validate_required_fields(data: dict, result: ValidationResult) -> bool:
        """Validate required fields are present."""
        required_fields = ["pages", "chapters", "metadata"]
        for field in required_fields:
            if field not in data:
                result.add_error(f"Missing required field: '{field}'")
        return not result.errors

    @staticmethod
    def _validate_pages(pages: List[dict], result: ValidationResult) -> None:
        """Validate page content."""
        if not pages:
            result.add_error("No pages extracted from PDF")
            return
        
        result.add_info(f"Pages extracted: {len(pages)}")
        
        pages_with_content = 0
        empty_pages = []
        
        for page in pages:
            content = page.get("content", "")
            page_num = page.get("page_number", "?")
            
            if content and len(content.strip()) >= PDFConversionValidator.MIN_CONTENT_PER_PAGE:
                pages_with_content += 1
            else:
                empty_pages.append(page_num)
        
        if pages_with_content < PDFConversionValidator.MIN_PAGES_WITH_CONTENT:
            result.add_error(
                f"Too few pages with content: {pages_with_content} "
                f"(minimum: {PDFConversionValidator.MIN_PAGES_WITH_CONTENT})"
            )
        else:
            result.add_info(f"Pages with content: {pages_with_content}/{len(pages)}")
        
        if len(empty_pages) > len(pages) * 0.5:
            result.add_warning(f"High proportion of empty pages: {len(empty_pages)}/{len(pages)}")

    @staticmethod
    def _validate_chapters(chapters: List[dict], result: ValidationResult) -> None:
        """Validate chapter structure."""
        if not chapters:
            result.add_error("No chapters detected")
            return
        
        result.add_info(f"Chapters detected: {len(chapters)}")
        
        for ch in chapters:
            required_ch_fields = ["number", "title", "start_page", "end_page"]
            missing = [f for f in required_ch_fields if f not in ch]
            if missing:
                result.add_warning(f"Chapter {ch.get('number', '?')} missing fields: {missing}")
    
    @staticmethod
    def validate(source_pdf: Path, output_json: Path) -> ValidationResult:
        """Validate PDF conversion output using helper methods."""
        result = ValidationResult()
        
        # Load and validate file
        data = PDFConversionValidator._validate_file_and_load(output_json, result)
        if data is None:
            return result
        
        # Check required fields
        if not PDFConversionValidator._validate_required_fields(data, result):
            return result
        
        # Validate pages
        PDFConversionValidator._validate_pages(data.get("pages", []), result)
        if result.errors:
            return result
        
        # Validate chapters
        PDFConversionValidator._validate_chapters(data.get("chapters", []), result)
        
        # Validate metadata
        metadata = data.get("metadata", {})
        if not metadata.get("title"):
            result.add_warning("Book metadata missing title")
        
        return result


class MetadataExtractionValidator:
    """
    Validates metadata extraction output (Tab 2).
    
    Checks:
    1. Metadata JSON exists
    2. Content was actually captured from source pages
    3. Keywords and concepts extracted
    4. Summaries are meaningful (not just fallbacks)
    """
    
    MIN_SUMMARY_LENGTH = 50
    MIN_KEYWORDS = 3
    MIN_CONCEPTS = 3
    
    @staticmethod
    def _load_metadata(metadata_json: Path, result: "ValidationResult") -> Optional[List]:
        """Load and validate metadata JSON structure."""
        if not metadata_json.exists():
            result.add_error(f"Metadata file not created: {metadata_json.name}")
            return None
        
        result.add_info(f"Metadata file exists: {metadata_json.name}")
        
        try:
            with open(metadata_json) as f:
                metadata = json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid metadata JSON: {e}")
            return None
        
        if not isinstance(metadata, list):
            result.add_error(f"Metadata must be a list, got {type(metadata).__name__}")
            return None
        
        if not metadata:
            result.add_error("Metadata is empty (0 chapters)")
            return None
        
        result.add_info(f"Chapters in metadata: {len(metadata)}")
        return metadata
    
    @staticmethod
    def _build_page_content_map(source_json: Path, result: "ValidationResult") -> Dict[int, int]:
        """Build page number to content length mapping from source JSON."""
        page_content_map = {}
        if source_json.exists():
            try:
                with open(source_json) as f:
                    source_data = json.load(f)
                    source_pages = source_data.get("pages", [])
                for page in source_pages:
                    page_num = page.get("page_number")
                    if page_num is not None:
                        content = page.get("content", "")
                        page_content_map[page_num] = len(content) if content else 0
            except Exception:
                result.add_warning("Could not load source JSON for content validation")
        return page_content_map
    
    @classmethod
    def _validate_chapter(
        cls, 
        chapter: Dict, 
        page_content_map: Dict[int, int], 
        result: "ValidationResult"
    ) -> bool:
        """Validate a single chapter. Returns True if empty extraction detected with source content."""
        ch_num = chapter.get("chapter_number", "?")
        
        required = ["chapter_number", "title", "start_page", "end_page", 
                   "summary", "keywords", "concepts"]
        missing = [f for f in required if f not in chapter]
        if missing:
            result.add_error(f"Chapter {ch_num}: Missing fields: {missing}")
            return False
        
        summary = chapter.get("summary", "")
        keywords = chapter.get("keywords", [])
        concepts = chapter.get("concepts", [])
        start_page = chapter.get("start_page")
        end_page = chapter.get("end_page")
        
        is_empty = (
            len(summary) < cls.MIN_SUMMARY_LENGTH and
            len(keywords) < cls.MIN_KEYWORDS and
            len(concepts) < cls.MIN_CONCEPTS
        )
        
        if not is_empty:
            return False
        
        source_chars = sum(
            page_content_map.get(p, 0) 
            for p in range(start_page, end_page + 1)
        )
        
        if source_chars > 500:
            result.add_error(
                f"Chapter {ch_num}: Source has {source_chars:,} chars "
                f"but extraction appears empty (summary: {len(summary)}, "
                f"keywords: {len(keywords)}, concepts: {len(concepts)})"
            )
            return True
        
        result.add_warning(
            f"Chapter {ch_num}: Minimal extraction (source may have limited content)"
        )
        return False
    
    @classmethod
    def validate(cls, source_json: Path, metadata_json: Path) -> "ValidationResult":
        """Validate metadata extraction output."""
        result = ValidationResult()
        
        metadata = cls._load_metadata(metadata_json, result)
        if metadata is None:
            return result
        
        page_content_map = cls._build_page_content_map(source_json, result)
        
        for chapter in metadata:
            cls._validate_chapter(chapter, page_content_map, result)
        
        if not result.errors:
            result.add_info("All chapters have valid extraction")
        
        return result


class MetadataEnrichmentValidator:
    """
    Validates metadata enrichment output (Tab 4).
    
    Checks:
    1. Enriched JSON exists
    2. Required structure (book, enrichment_metadata, chapters)
    3. Enrichment metadata has method and libraries
    4. Chapters have enriched fields
    """
    
    @staticmethod
    def validate(source_metadata: Path, enriched_json: Path) -> ValidationResult:
        """Validate metadata enrichment output."""
        result = ValidationResult()
        
        # Check output exists
        if not enriched_json.exists():
            result.add_error(f"Enriched file not created: {enriched_json.name}")
            return result
        
        result.add_info(f"Enriched file exists: {enriched_json.name}")
        
        # Load enriched data
        try:
            with open(enriched_json) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid enriched JSON: {e}")
            return result
        
        # Check structure
        required_top_level = ["book", "enrichment_metadata", "chapters"]
        for field in required_top_level:
            if field not in data:
                result.add_error(f"Missing required field: '{field}'")
        
        if result.errors:
            return result
        
        # Validate enrichment_metadata
        enrichment_meta = data.get("enrichment_metadata", {})
        if enrichment_meta.get("method") != "statistical":
            result.add_warning(f"Unexpected method: {enrichment_meta.get('method')}")
        
        if "libraries" not in enrichment_meta:
            result.add_warning("Missing libraries info in enrichment_metadata")
        
        result.add_info(f"Enrichment method: {enrichment_meta.get('method', 'unknown')}")
        
        # Validate chapters
        chapters = data.get("chapters", [])
        if not chapters:
            result.add_error("No chapters in enriched output")
            return result
        
        result.add_info(f"Chapters enriched: {len(chapters)}")
        
        # Check enrichment fields in chapters
        enrichment_fields = ["tier", "category", "relevance_score"]
        chapters_with_enrichment = 0
        
        for ch in chapters:
            has_enrichment = any(f in ch for f in enrichment_fields)
            if has_enrichment:
                chapters_with_enrichment += 1
        
        if chapters_with_enrichment == 0:
            result.add_warning("No chapters have enrichment fields (tier, category, relevance)")
        else:
            result.add_info(f"Chapters with enrichment: {chapters_with_enrichment}/{len(chapters)}")
        
        return result


class BaseGuidelineValidator:
    """
    Validates base guideline generation output (Tab 5).
    
    Checks:
    1. Output file exists (MD and/or JSON)
    2. Markdown has expected structure (headers, content)
    3. JSON has valid guideline schema
    4. Content is not empty/minimal
    """
    
    MIN_GUIDELINE_LENGTH = 1000  # Minimum chars for a valid guideline
    
    @classmethod
    def _validate_md_output(cls, output_md: Path, result: "ValidationResult") -> None:
        """Validate markdown output file."""
        if not output_md.exists():
            result.add_error(f"Markdown output not created: {output_md.name}")
            return
        
        result.add_info(f"Markdown output exists: {output_md.name}")
        content = output_md.read_text()
        
        if len(content) < cls.MIN_GUIDELINE_LENGTH:
            result.add_error(
                f"Guideline too short: {len(content)} chars "
                f"(min: {cls.MIN_GUIDELINE_LENGTH})"
            )
        else:
            result.add_info(f"Guideline length: {len(content):,} chars")
        
        if "# " not in content:
            result.add_warning("No top-level headers found in markdown")
        
        if "## " not in content:
            result.add_warning("No second-level headers found in markdown")
    
    @staticmethod
    def _validate_json_output(output_json: Path, result: "ValidationResult") -> None:
        """Validate JSON output file."""
        if not output_json.exists():
            result.add_error(f"JSON output not created: {output_json.name}")
            return
        
        result.add_info(f"JSON output exists: {output_json.name}")
        
        try:
            with open(output_json) as f:
                data = json.load(f)
            
            if "guidelines" not in data and "content" not in data:
                result.add_warning("JSON missing 'guidelines' or 'content' field")
        except json.JSONDecodeError as e:
            result.add_error(f"Invalid guideline JSON: {e}")
    
    @classmethod
    def validate(cls, source_metadata: Path, output_md: Optional[Path] = None, 
                 output_json: Optional[Path] = None) -> "ValidationResult":
        """Validate base guideline generation output."""
        result = ValidationResult()
        
        if not output_md and not output_json:
            result.add_error("No output file specified")
            return result
        
        if output_md:
            cls._validate_md_output(output_md, result)
        
        if output_json:
            cls._validate_json_output(output_json, result)
        
        return result


class LLMEnhancementValidator:
    """
    Validates LLM enhancement workflow (Tab 6).
    
    Two-phase validation:
    1. Pre-LLM: Validate aggregate input is complete and well-formed
    2. Post-LLM: Validate enhanced output meets quality standards
    """
    
    MIN_ENHANCED_LENGTH = 2000
    REQUIRED_ENHANCEMENT_MARKERS = [
        "**From",  # Source annotations
        "```",      # Code examples
    ]
    
    @staticmethod
    def validate_input_aggregate(aggregate_path: Path) -> ValidationResult:
        """
        Validate input aggregate before sending to LLM.
        
        Checks:
        1. Aggregate file exists and is valid
        2. Contains sufficient content for LLM processing
        3. Structure is correct for LLM prompt
        """
        result = ValidationResult()
        
        if not aggregate_path.exists():
            result.add_error(f"Aggregate file not found: {aggregate_path.name}")
            return result
        
        result.add_info(f"Aggregate file exists: {aggregate_path.name}")
        
        # Check file size (proxy for content)
        file_size = aggregate_path.stat().st_size
        if file_size < 1000:
            result.add_error(f"Aggregate too small: {file_size} bytes")
        else:
            result.add_info(f"Aggregate size: {file_size:,} bytes")
        
        # Load and validate content
        if aggregate_path.suffix == ".json":
            try:
                with open(aggregate_path) as f:
                    data = json.load(f)
                
                # Check for required fields
                if "content" not in data and "guidelines" not in data:
                    result.add_warning("Aggregate missing 'content' or 'guidelines' field")
                
            except json.JSONDecodeError as e:
                result.add_error(f"Invalid aggregate JSON: {e}")
        else:
            # Markdown aggregate
            content = aggregate_path.read_text()
            if len(content.strip()) < 500:
                result.add_error("Aggregate content too short for LLM processing")
        
        return result
    
    @classmethod
    def _check_enhancement_markers(cls, content: str, result: "ValidationResult") -> None:
        """Check for expected enhancement markers in content."""
        markers_found = []
        markers_missing = []
        
        for marker in cls.REQUIRED_ENHANCEMENT_MARKERS:
            if marker in content:
                markers_found.append(marker)
            else:
                markers_missing.append(marker)
        
        if markers_missing:
            result.add_warning(f"Missing enhancement markers: {markers_missing}")
        
        if markers_found:
            result.add_info(f"Enhancement markers found: {len(markers_found)}")
    
    @staticmethod
    def _check_truncation(content: str, original_path: Optional[Path], result: "ValidationResult") -> None:
        """Check for LLM truncation issues by comparing with original."""
        if not original_path or not original_path.exists():
            return
        
        original_content = original_path.read_text()
        
        if len(content) < len(original_content) * 0.8:
            result.add_warning(
                f"Enhanced content ({len(content):,} chars) is shorter than "
                f"original ({len(original_content):,} chars) - possible truncation"
            )
        
        truncation_markers = [
            "I'll continue",
            "Let me know if",
            "[continues]",
            "...more to follow"
        ]
        
        for marker in truncation_markers:
            if marker.lower() in content.lower():
                result.add_error(f"LLM truncation detected: '{marker}'")
    
    @classmethod
    def validate_enhanced_output(cls, enhanced_path: Path, 
                                  original_path: Optional[Path] = None) -> "ValidationResult":
        """
        Validate LLM-enhanced output.
        
        Checks:
        1. Enhanced file exists
        2. Content length is reasonable
        3. Expected enhancement markers present
        4. Content is not truncated (if original provided)
        """
        result = ValidationResult()
        
        if not enhanced_path.exists():
            result.add_error(f"Enhanced output not created: {enhanced_path.name}")
            return result
        
        result.add_info(f"Enhanced output exists: {enhanced_path.name}")
        content = enhanced_path.read_text()
        
        if len(content) < cls.MIN_ENHANCED_LENGTH:
            result.add_error(
                f"Enhanced output too short: {len(content)} chars "
                f"(min: {cls.MIN_ENHANCED_LENGTH})"
            )
        else:
            result.add_info(f"Enhanced output length: {len(content):,} chars")
        
        cls._check_enhancement_markers(content, result)
        cls._check_truncation(content, original_path, result)
        
        return result


class WorkflowValidationFacade:
    """
    Facade for all workflow validations.
    
    Provides a single interface for the frontend to call appropriate
    validators based on workflow stage.
    """
    
    def __init__(self, workflows_dir: Path):
        self.workflows_dir = workflows_dir
    
    def validate_pdf_conversion(self, pdf_filename: str) -> Dict[str, Any]:
        """Validate Tab 1: PDF to JSON conversion."""
        source_pdf = self.workflows_dir / "pdf_to_json" / "input" / pdf_filename
        output_json = self.workflows_dir / "pdf_to_json" / "output" / "textbooks_json" / f"{Path(pdf_filename).stem}.json"
        
        result = PDFConversionValidator.validate(source_pdf, output_json)
        return result.to_dict()
    
    def validate_metadata_extraction(self, json_filename: str) -> Dict[str, Any]:
        """Validate Tab 2: Metadata extraction."""
        source_json = self.workflows_dir / "pdf_to_json" / "output" / "textbooks_json" / json_filename
        metadata_json = self.workflows_dir / "metadata_extraction" / "output" / f"{Path(json_filename).stem}_metadata.json"
        
        result = MetadataExtractionValidator.validate(source_json, metadata_json)
        return result.to_dict()
    
    def validate_metadata_enrichment(self, metadata_filename: str) -> Dict[str, Any]:
        """Validate Tab 4: Metadata enrichment."""
        source_metadata = self.workflows_dir / "metadata_extraction" / "output" / metadata_filename
        # Output filename: remove _metadata suffix, add _enriched
        base_name = Path(metadata_filename).stem.replace("_metadata", "")
        enriched_json = self.workflows_dir / "metadata_enrichment" / "output" / f"{base_name}_enriched.json"
        
        result = MetadataEnrichmentValidator.validate(source_metadata, enriched_json)
        return result.to_dict()
    
    def validate_base_guideline(self, metadata_filename: str, 
                                 output_format: str = "both") -> Dict[str, Any]:
        """Validate Tab 5: Base guideline generation."""
        source = self.workflows_dir / "metadata_extraction" / "output" / metadata_filename
        base_name = Path(metadata_filename).stem.replace("_metadata", "")
        
        output_md = None
        output_json = None
        
        if output_format in ("md", "both"):
            output_md = self.workflows_dir / "base_guideline_generation" / "output" / f"{base_name}_GUIDELINES.md"
        if output_format in ("json", "both"):
            output_json = self.workflows_dir / "base_guideline_generation" / "output" / f"{base_name}_GUIDELINES.json"
        
        result = BaseGuidelineValidator.validate(source, output_md, output_json)
        return result.to_dict()
    
    def validate_llm_input(self, aggregate_filename: str) -> Dict[str, Any]:
        """Validate Tab 6 input: Pre-LLM aggregate."""
        aggregate_path = self.workflows_dir / "llm_enhancement" / "input" / aggregate_filename
        
        result = LLMEnhancementValidator.validate_input_aggregate(aggregate_path)
        return result.to_dict()
    
    def validate_llm_output(self, enhanced_filename: str, 
                            original_filename: Optional[str] = None) -> Dict[str, Any]:
        """Validate Tab 6 output: Post-LLM enhanced output."""
        enhanced_path = self.workflows_dir / "llm_enhancement" / "output" / enhanced_filename
        
        original_path = None
        if original_filename:
            original_path = self.workflows_dir / "llm_enhancement" / "input" / original_filename
        
        result = LLMEnhancementValidator.validate_enhanced_output(enhanced_path, original_path)
        return result.to_dict()
