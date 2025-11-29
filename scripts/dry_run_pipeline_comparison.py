#!/usr/bin/env python3
"""
Dry Run Pipeline Comparison - Full Workflow Analysis

Compares current outputs across all pipeline stages with new outputs
to verify quality improvements from recent changes:

Recent Changes (past 48 hours):
- Tab 1 (PDF to JSON): Unstructured PDF extractor with PyMuPDF fallback
- Tab 2 (Metadata Extraction): TOCParserStrategy, StatisticalExtractor with WordNet
- Tab 4 (Metadata Enrichment): BERTopic + Sentence Transformers integration
- Tab 5 (Guideline Generation): Topic-aware cross-referencing

Usage:
    # List available books
    python scripts/dry_run_pipeline_comparison.py --list-books
    
    # Compare single book across all stages
    python scripts/dry_run_pipeline_comparison.py --book "Architecture Patterns with Python"
    
    # Compare multiple books
    python scripts/dry_run_pipeline_comparison.py --all --limit 3
    
    # Generate JSON report
    python scripts/dry_run_pipeline_comparison.py --book "Fluent Python 2nd" --output-report reports/comparison.json

Output:
    - Tab 1: PDF extraction quality (elements, fallback usage)
    - Tab 2: Metadata extraction quality (chapters, keywords, concepts)
    - Tab 4: Enrichment quality (topic_id, related chapters, cross-book)
    - Tab 5: Guideline quality (cross-references, topic boosting)
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Tab1Metrics:
    """PDF to JSON extraction metrics."""
    book_name: str
    json_file_exists: bool = False
    json_file_size_kb: float = 0.0
    total_pages: int = 0
    chapters_detected: int = 0
    extraction_method: str = ""  # unstructured, pymupdf, fallback
    has_toc: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Tab2Metrics:
    """Metadata extraction metrics."""
    book_name: str
    metadata_file_exists: bool = False
    chapter_count: int = 0
    avg_keywords_per_chapter: float = 0.0
    avg_concepts_per_chapter: float = 0.0
    avg_summary_length: float = 0.0
    has_page_ranges: bool = False
    extraction_method: str = ""  # statistical, llm, hybrid
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Tab4Metrics:
    """Metadata enrichment metrics."""
    book_name: str
    enriched_file_exists: bool = False
    chapter_count: int = 0
    
    # NEW: Topic clustering
    has_topic_ids: bool = False
    topic_coverage_pct: float = 0.0
    unique_topics: int = 0
    
    # Cross-book analysis
    avg_related_chapters: float = 0.0
    avg_keywords_enriched: float = 0.0
    avg_concepts_enriched: float = 0.0
    
    # Method info
    enrichment_method: str = ""
    libraries: Dict[str, str] = field(default_factory=dict)
    corpus_size: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Tab5Metrics:
    """Guideline generation metrics."""
    book_name: str
    guideline_file_exists: bool = False
    section_count: int = 0
    cross_references_count: int = 0
    has_topic_boosting: bool = False
    output_format: str = ""  # json, markdown
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PipelineComparison:
    """Complete pipeline comparison for a book."""
    book_name: str
    analyzed_at: str = ""
    tab1: Optional[Tab1Metrics] = None
    tab2: Optional[Tab2Metrics] = None
    tab4: Optional[Tab4Metrics] = None
    tab5: Optional[Tab5Metrics] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "book_name": self.book_name,
            "analyzed_at": self.analyzed_at,
            "tab1_pdf_extraction": self.tab1.to_dict() if self.tab1 else None,
            "tab2_metadata_extraction": self.tab2.to_dict() if self.tab2 else None,
            "tab4_metadata_enrichment": self.tab4.to_dict() if self.tab4 else None,
            "tab5_guideline_generation": self.tab5.to_dict() if self.tab5 else None
        }


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_tab1(book_name: str) -> Tab1Metrics:
    """Analyze PDF to JSON extraction output."""
    metrics = Tab1Metrics(book_name=book_name)
    
    json_dir = PROJECT_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json"
    json_file = json_dir / f"{book_name}.json"
    
    if not json_file.exists():
        return metrics
    
    metrics.json_file_exists = True
    metrics.json_file_size_kb = json_file.stat().st_size / 1024
    
    try:
        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)
        
        # Analyze structure
        if isinstance(data, dict):
            metrics.total_pages = data.get("total_pages", 0)
            metrics.has_toc = bool(data.get("toc") or data.get("table_of_contents"))
            
            # Check extraction method from metadata
            extraction_info = data.get("extraction_info", {})
            metrics.extraction_method = extraction_info.get("method", "unknown")
            
            # Count chapters from structure
            chapters = data.get("chapters", [])
            metrics.chapters_detected = len(chapters)
            
        elif isinstance(data, list):
            # Old format: list of pages/elements
            metrics.total_pages = len(data)
            metrics.extraction_method = "legacy"
            
    except Exception as e:
        print(f"  ⚠️  Error parsing Tab 1 JSON: {e}")
    
    return metrics


def analyze_tab2(book_name: str) -> Tab2Metrics:
    """Analyze metadata extraction output."""
    metrics = Tab2Metrics(book_name=book_name)
    
    metadata_dir = PROJECT_ROOT / "workflows" / "metadata_extraction" / "output"
    metadata_file = metadata_dir / f"{book_name}_metadata.json"
    
    if not metadata_file.exists():
        return metrics
    
    metrics.metadata_file_exists = True
    
    try:
        with open(metadata_file, encoding='utf-8') as f:
            chapters = json.load(f)
        
        if not isinstance(chapters, list):
            return metrics
        
        metrics.chapter_count = len(chapters)
        
        # Calculate averages
        keyword_counts = []
        concept_counts = []
        summary_lengths = []
        has_pages = True
        
        for ch in chapters:
            keywords = ch.get("keywords", [])
            concepts = ch.get("concepts", [])
            summary = ch.get("summary", "")
            
            keyword_counts.append(len(keywords))
            concept_counts.append(len(concepts))
            summary_lengths.append(len(summary))
            
            if not ch.get("start_page") or not ch.get("end_page"):
                has_pages = False
        
        if chapters:
            metrics.avg_keywords_per_chapter = sum(keyword_counts) / len(chapters)
            metrics.avg_concepts_per_chapter = sum(concept_counts) / len(chapters)
            metrics.avg_summary_length = sum(summary_lengths) / len(chapters)
        
        metrics.has_page_ranges = has_pages
        metrics.extraction_method = "statistical"  # Current implementation
        
    except Exception as e:
        print(f"  ⚠️  Error parsing Tab 2 metadata: {e}")
    
    return metrics


def analyze_tab4(book_name: str) -> Tab4Metrics:
    """Analyze metadata enrichment output."""
    metrics = Tab4Metrics(book_name=book_name)
    
    enriched_dir = PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output"
    enriched_file = enriched_dir / f"{book_name}_enriched.json"
    
    if not enriched_file.exists():
        return metrics
    
    metrics.enriched_file_exists = True
    
    try:
        with open(enriched_file, encoding='utf-8') as f:
            data = json.load(f)
        
        # Enrichment metadata
        enrich_meta = data.get("enrichment_metadata", {})
        metrics.enrichment_method = enrich_meta.get("method", "unknown")
        metrics.libraries = enrich_meta.get("libraries", {})
        metrics.corpus_size = enrich_meta.get("corpus_size", 0)
        
        # Analyze chapters
        chapters = data.get("chapters", [])
        metrics.chapter_count = len(chapters)
        
        # Topic clustering analysis (NEW)
        topic_ids = [ch.get("topic_id") for ch in chapters if ch.get("topic_id") is not None]
        metrics.has_topic_ids = len(topic_ids) > 0
        metrics.unique_topics = len(set(topic_ids)) if topic_ids else 0
        metrics.topic_coverage_pct = (len(topic_ids) / len(chapters) * 100) if chapters else 0
        
        # Cross-book metrics
        related_counts = []
        kw_enriched_counts = []
        concept_enriched_counts = []
        
        for ch in chapters:
            related_counts.append(len(ch.get("related_chapters", [])))
            kw_enriched_counts.append(len(ch.get("keywords_enriched", [])))
            concept_enriched_counts.append(len(ch.get("concepts_enriched", [])))
        
        if chapters:
            metrics.avg_related_chapters = sum(related_counts) / len(chapters)
            metrics.avg_keywords_enriched = sum(kw_enriched_counts) / len(chapters)
            metrics.avg_concepts_enriched = sum(concept_enriched_counts) / len(chapters)
        
    except Exception as e:
        print(f"  ⚠️  Error parsing Tab 4 enriched: {e}")
    
    return metrics


def analyze_tab5(book_name: str) -> Tab5Metrics:
    """Analyze guideline generation output."""
    metrics = Tab5Metrics(book_name=book_name)
    
    guideline_dir = PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"
    
    # Check for JSON or MD output
    json_file = guideline_dir / f"{book_name}_guideline.json"
    md_file = guideline_dir / f"{book_name}_guideline.md"
    
    if json_file.exists():
        metrics.guideline_file_exists = True
        metrics.output_format = "json"
        
        try:
            with open(json_file, encoding='utf-8') as f:
                data = json.load(f)
            
            # Count sections
            if isinstance(data, dict):
                metrics.section_count = len(data.get("sections", data.get("chapters", [])))
                
                # Look for cross-references
                for section in data.get("sections", data.get("chapters", [])):
                    xrefs = section.get("cross_references", [])
                    metrics.cross_references_count += len(xrefs)
                    
                    # Check for topic boosting (look for topic_id in refs)
                    for xref in xrefs:
                        if xref.get("topic_id") is not None:
                            metrics.has_topic_boosting = True
                            break
                            
        except Exception as e:
            print(f"  ⚠️  Error parsing Tab 5 JSON: {e}")
            
    elif md_file.exists():
        metrics.guideline_file_exists = True
        metrics.output_format = "markdown"
        
        try:
            content = md_file.read_text(encoding='utf-8')
            # Count sections by headers
            metrics.section_count = content.count("\n## ")
            # Count cross-references (look for "See also" or "Related:")
            metrics.cross_references_count = content.count("See also") + content.count("Related:")
        except Exception as e:
            print(f"  ⚠️  Error parsing Tab 5 MD: {e}")
    
    return metrics


def analyze_book(book_name: str) -> PipelineComparison:
    """Run complete pipeline analysis for a book."""
    comparison = PipelineComparison(
        book_name=book_name,
        analyzed_at=datetime.now().isoformat()
    )
    
    comparison.tab1 = analyze_tab1(book_name)
    comparison.tab2 = analyze_tab2(book_name)
    comparison.tab4 = analyze_tab4(book_name)
    comparison.tab5 = analyze_tab5(book_name)
    
    return comparison


# =============================================================================
# REPORTING FUNCTIONS
# =============================================================================

def print_comparison_report(comparison: PipelineComparison) -> None:
    """Print human-readable comparison report."""
    print(f"\n{'='*70}")
    print(f"📊 PIPELINE ANALYSIS: {comparison.book_name}")
    print(f"{'='*70}")
    
    # Tab 1: PDF Extraction
    t1 = comparison.tab1
    print(f"\n📄 TAB 1: PDF to JSON Extraction")
    if t1 and t1.json_file_exists:
        print(f"   ✅ JSON file: {t1.json_file_size_kb:.1f} KB")
        print(f"   • Total pages: {t1.total_pages}")
        print(f"   • Chapters detected: {t1.chapters_detected}")
        print(f"   • Has TOC: {'Yes' if t1.has_toc else 'No'}")
        print(f"   • Extraction method: {t1.extraction_method}")
    else:
        print(f"   ⚠️  JSON file not found")
    
    # Tab 2: Metadata Extraction
    t2 = comparison.tab2
    print(f"\n📋 TAB 2: Metadata Extraction")
    if t2 and t2.metadata_file_exists:
        print(f"   ✅ Metadata file exists")
        print(f"   • Chapters: {t2.chapter_count}")
        print(f"   • Avg keywords/chapter: {t2.avg_keywords_per_chapter:.1f}")
        print(f"   • Avg concepts/chapter: {t2.avg_concepts_per_chapter:.1f}")
        print(f"   • Avg summary length: {t2.avg_summary_length:.0f} chars")
        print(f"   • Has page ranges: {'Yes' if t2.has_page_ranges else 'No'}")
        print(f"   • Method: {t2.extraction_method}")
    else:
        print(f"   ⚠️  Metadata file not found")
    
    # Tab 4: Metadata Enrichment
    t4 = comparison.tab4
    print(f"\n🔗 TAB 4: Metadata Enrichment")
    if t4 and t4.enriched_file_exists:
        print(f"   ✅ Enriched file exists")
        print(f"   • Chapters: {t4.chapter_count}")
        print(f"   • Corpus size: {t4.corpus_size} chapters analyzed")
        
        # Topic clustering (NEW FEATURE)
        if t4.has_topic_ids:
            print(f"   🆕 TOPIC CLUSTERING:")
            print(f"      • Coverage: {t4.topic_coverage_pct:.1f}%")
            print(f"      • Unique topics: {t4.unique_topics}")
        else:
            print(f"   ℹ️  No topic_id assignments (pre-BERTopic output)")
        
        print(f"   • Avg related chapters: {t4.avg_related_chapters:.2f}")
        print(f"   • Avg keywords enriched: {t4.avg_keywords_enriched:.2f}")
        print(f"   • Avg concepts enriched: {t4.avg_concepts_enriched:.2f}")
        print(f"   • Method: {t4.enrichment_method}")
        if t4.libraries:
            print(f"   • Libraries: {', '.join(f'{k}={v}' for k, v in t4.libraries.items())}")
    else:
        print(f"   ⚠️  Enriched file not found")
    
    # Tab 5: Guideline Generation
    t5 = comparison.tab5
    print(f"\n📖 TAB 5: Guideline Generation")
    if t5 and t5.guideline_file_exists:
        print(f"   ✅ Guideline file exists ({t5.output_format})")
        print(f"   • Sections: {t5.section_count}")
        print(f"   • Cross-references: {t5.cross_references_count}")
        print(f"   • Topic boosting: {'Yes' if t5.has_topic_boosting else 'No'}")
    else:
        print(f"   ⚠️  Guideline file not found")


def get_available_books() -> List[str]:
    """Get list of books that exist across any pipeline stage."""
    books = set()
    
    # Check each output directory
    dirs = [
        PROJECT_ROOT / "workflows" / "pdf_to_json" / "output" / "textbooks_json",
        PROJECT_ROOT / "workflows" / "metadata_extraction" / "output",
        PROJECT_ROOT / "workflows" / "metadata_enrichment" / "output",
        PROJECT_ROOT / "workflows" / "base_guideline_generation" / "output"
    ]
    
    for dir_path in dirs:
        if not dir_path.exists():
            continue
        for f in dir_path.glob("*.json"):
            name = f.stem
            # Normalize name
            name = name.replace("_metadata", "").replace("_enriched", "").replace("_guideline", "")
            if name and not name.startswith("."):
                books.add(name)
    
    return sorted(books)


def print_summary(comparisons: List[PipelineComparison]) -> None:
    """Print summary across all analyzed books."""
    print(f"\n{'='*70}")
    print("📊 SUMMARY ACROSS ALL BOOKS")
    print(f"{'='*70}")
    
    total_books = len(comparisons)
    
    # Tab 1 summary
    t1_exists = sum(1 for c in comparisons if c.tab1 and c.tab1.json_file_exists)
    print(f"\n📄 Tab 1 (PDF Extraction): {t1_exists}/{total_books} books have JSON")
    
    # Tab 2 summary
    t2_exists = sum(1 for c in comparisons if c.tab2 and c.tab2.metadata_file_exists)
    avg_chapters = sum(c.tab2.chapter_count for c in comparisons if c.tab2 and c.tab2.metadata_file_exists) / t2_exists if t2_exists else 0
    print(f"\n📋 Tab 2 (Metadata): {t2_exists}/{total_books} books have metadata")
    print(f"   Avg chapters per book: {avg_chapters:.1f}")
    
    # Tab 4 summary
    t4_exists = sum(1 for c in comparisons if c.tab4 and c.tab4.enriched_file_exists)
    t4_with_topics = sum(1 for c in comparisons if c.tab4 and c.tab4.has_topic_ids)
    print(f"\n🔗 Tab 4 (Enrichment): {t4_exists}/{total_books} books enriched")
    print(f"   Books with topic_id: {t4_with_topics}/{t4_exists} (NEW FEATURE)")
    
    if t4_exists > 0:
        avg_topics = sum(c.tab4.unique_topics for c in comparisons if c.tab4 and c.tab4.has_topic_ids) / max(t4_with_topics, 1)
        avg_related = sum(c.tab4.avg_related_chapters for c in comparisons if c.tab4 and c.tab4.enriched_file_exists) / t4_exists
        print(f"   Avg unique topics: {avg_topics:.1f}")
        print(f"   Avg related chapters: {avg_related:.2f}")
    
    # Tab 5 summary
    t5_exists = sum(1 for c in comparisons if c.tab5 and c.tab5.guideline_file_exists)
    t5_with_boost = sum(1 for c in comparisons if c.tab5 and c.tab5.has_topic_boosting)
    print(f"\n📖 Tab 5 (Guidelines): {t5_exists}/{total_books} books have guidelines")
    print(f"   With topic boosting: {t5_with_boost}/{t5_exists}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Analyze pipeline outputs across all workflow stages"
    )
    parser.add_argument(
        "--book",
        type=str,
        help="Specific book to analyze"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Analyze all available books"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum books to analyze with --all (default: 10)"
    )
    parser.add_argument(
        "--output-report",
        type=str,
        help="Path to save JSON report"
    )
    parser.add_argument(
        "--list-books",
        action="store_true",
        help="List available books and exit"
    )
    
    args = parser.parse_args()
    
    if args.list_books:
        books = get_available_books()
        print(f"\n📚 Available books ({len(books)}):")
        for book in books:
            print(f"  • {book}")
        return
    
    if not args.book and not args.all:
        parser.error("Either --book or --all must be specified")
    
    print("\n" + "="*70)
    print("🔬 PIPELINE DRY RUN ANALYSIS")
    print("   Checking outputs affected by recent changes:")
    print("   • Tab 1: Unstructured PDF extractor + PyMuPDF fallback")
    print("   • Tab 2: TOCParserStrategy + WordNet validation")
    print("   • Tab 4: BERTopic + Sentence Transformers")
    print("   • Tab 5: Topic-aware cross-referencing")
    print("="*70)
    
    # Determine which books to analyze
    if args.all:
        books = get_available_books()[:args.limit]
        print(f"\n📚 Analyzing {len(books)} books...")
    else:
        books = [args.book]
    
    comparisons = []
    for book_name in books:
        print(f"\n{'─'*70}")
        print(f"📖 Processing: {book_name}")
        print(f"{'─'*70}")
        
        comparison = analyze_book(book_name)
        comparisons.append(comparison)
        print_comparison_report(comparison)
    
    # Print summary if multiple books
    if len(comparisons) > 1:
        print_summary(comparisons)
    
    # Save report if requested
    if args.output_report:
        report_path = Path(args.output_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            "generated": datetime.now().isoformat(),
            "description": "Pipeline dry run analysis - checking workflow outputs",
            "recent_changes": [
                "Tab 1: Unstructured PDF extractor with PyMuPDF fallback",
                "Tab 2: TOCParserStrategy + StatisticalExtractor with WordNet",
                "Tab 4: BERTopic + Sentence Transformers integration",
                "Tab 5: Topic-aware cross-referencing"
            ],
            "books_analyzed": len(comparisons),
            "comparisons": [c.to_dict() for c in comparisons]
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"\n📁 Report saved to: {report_path}")


if __name__ == "__main__":
    main()
