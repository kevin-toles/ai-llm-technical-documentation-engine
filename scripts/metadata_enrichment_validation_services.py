"""
Tab 4 Metadata Enrichment Validation Service Layer

Architecture Pattern: Service Layer + Strategy Pattern
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)

Services:
- EnrichmentStructureValidator: Validates JSON structure (book, enrichment_metadata, chapters)
- EnrichmentContentValidator: Validates enrichment fields per chapter
- StatisticalMethodValidator: Validates statistical method metadata (no LLM)
- EnrichmentValidationOrchestrator: Orchestrates all validation strategies

References:
    - MASTER_IMPLEMENTATION_GUIDE Task 2.2
    - ARCHITECTURE_GUIDELINES Ch.4: Service Layer Pattern
    - PYTHON_GUIDELINES Ch.8: Classes and OOP
"""

from typing import Dict, List, Any, Tuple, Optional


class ValidationResult:
    """Result of a single validation check."""
    
    def __init__(self, status: str, message: str):
        """
        Args:
            status: 'passed', 'failed', or 'warning'
            message: Description of the validation result
        """
        self.status = status
        self.message = message
    
    def is_passed(self) -> bool:
        return self.status == "passed"
    
    def is_failed(self) -> bool:
        return self.status == "failed"
    
    def is_warning(self) -> bool:
        return self.status == "warning"


class EnrichmentStructureValidator:
    """
    Validates enriched metadata JSON structure.
    
    Pattern: Strategy Pattern (one validation strategy)
    References:
        - ARCHITECTURE_GUIDELINES Ch.13: Strategy Pattern
    """
    
    @staticmethod
    def validate_structure(enriched_data: Dict[str, Any]) -> List[ValidationResult]:
        """
        Validate enriched metadata has required structure.
        
        Required structure:
        {
            "book": str,
            "enrichment_metadata": {
                "generated": str (ISO timestamp),
                "method": "statistical",
                "libraries": {
                    "yake": str,
                    "summa": str,
                    "scikit-learn": str
                },
                "corpus_size": int,
                "total_chapters_analyzed": int
            },
            "chapters": List[...]
        }
        
        Args:
            enriched_data: Enriched metadata dictionary to validate
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        # Check top-level keys
        required_keys = ["book", "enrichment_metadata", "chapters"]
        for key in required_keys:
            if key not in enriched_data:
                results.append(ValidationResult(
                    "failed",
                    f"Missing required top-level key: '{key}'"
                ))
            else:
                results.append(ValidationResult(
                    "passed",
                    f"Top-level key present: '{key}'"
                ))
        
        # If enrichment_metadata missing, can't validate further
        if "enrichment_metadata" not in enriched_data:
            return results
        
        # Check enrichment_metadata structure
        metadata = enriched_data["enrichment_metadata"]
        required_metadata_keys = [
            "generated",
            "method",
            "libraries",
            "corpus_size",
            "total_chapters_analyzed"
        ]
        
        for key in required_metadata_keys:
            if key not in metadata:
                results.append(ValidationResult(
                    "failed",
                    f"Missing enrichment_metadata key: '{key}'"
                ))
            else:
                results.append(ValidationResult(
                    "passed",
                    f"enrichment_metadata key present: '{key}'"
                ))
        
        return results


class EnrichmentContentValidator:
    """
    Validates enrichment content fields in chapters.
    
    Pattern: Strategy Pattern (one validation strategy)
    References:
        - ARCHITECTURE_GUIDELINES Ch.13: Strategy Pattern
    """
    
    REQUIRED_FIELDS = [
        "related_chapters",
        "keywords_enriched",
        "concepts_enriched"
    ]
    
    @staticmethod
    def _check_chapter_fields(
        chapter: Dict[str, Any], 
        chapter_id: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Check a single chapter for missing fields and invalid scores.
        
        Returns:
            Tuple of (missing_field_info, invalid_score_info) or None for each if valid
        """
        missing_field_info = None
        invalid_score_info = None
        
        # Check required enrichment fields present
        missing = [f for f in EnrichmentContentValidator.REQUIRED_FIELDS if f not in chapter]
        if missing:
            missing_field_info = f"{chapter_id} (missing: {', '.join(missing)})"
        
        # Validate similarity scores in related_chapters
        if "related_chapters" in chapter:
            for related in chapter["related_chapters"]:
                if "similarity_score" in related:
                    score = related["similarity_score"]
                    if not isinstance(score, (int, float)):
                        invalid_score_info = f"{chapter_id} (score not numeric: {type(score).__name__})"
                        break
                    if not (0.0 <= score <= 1.0):
                        invalid_score_info = f"{chapter_id} (score out of range: {score})"
                        break
        
        return missing_field_info, invalid_score_info
    
    @classmethod
    def validate_content(cls, chapters: List[Dict[str, Any]]) -> List["ValidationResult"]:
        """
        Validate each chapter has enrichment fields.
        
        Required per chapter:
        - related_chapters: List[Dict] with similarity scores
        - keywords_enriched: List[Dict] with keyword scores
        - concepts_enriched: List[str]
        
        Args:
            chapters: List of chapter dictionaries
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        if not chapters:
            results.append(ValidationResult(
                "warning",
                "No chapters found to validate"
            ))
            return results
        
        chapters_missing_fields = []
        chapters_with_invalid_scores = []
        
        for i, chapter in enumerate(chapters):
            chapter_id = chapter.get("chapter", f"Chapter {i+1}")
            missing_info, invalid_info = cls._check_chapter_fields(chapter, chapter_id)
            
            if missing_info:
                chapters_missing_fields.append(missing_info)
            if invalid_info:
                chapters_with_invalid_scores.append(invalid_info)
        
        # Report findings
        if chapters_missing_fields:
            results.append(ValidationResult(
                "failed",
                f"Chapters missing enrichment fields: {', '.join(chapters_missing_fields)}"
            ))
        else:
            results.append(ValidationResult(
                "passed",
                f"All {len(chapters)} chapters have required enrichment fields"
            ))
        
        if chapters_with_invalid_scores:
            results.append(ValidationResult(
                "failed",
                f"Chapters with invalid similarity scores: {', '.join(chapters_with_invalid_scores)}"
            ))
        else:
            results.append(ValidationResult(
                "passed",
                "All similarity scores valid (0.0-1.0)"
            ))
        
        return results


class StatisticalMethodValidator:
    """
    Validates statistical method metadata (ensures no LLM usage).
    
    Pattern: Strategy Pattern (one validation strategy)
    References:
        - ARCHITECTURE_GUIDELINES Ch.13: Strategy Pattern
    """
    
    @staticmethod
    def validate_method(enrichment_metadata: Dict[str, Any]) -> List[ValidationResult]:
        """
        Validate statistical method metadata.
        
        Requirements:
        - method must be "statistical" (not "llm" or "llm-enhanced")
        - libraries must contain: yake, summa, scikit-learn
        
        Args:
            enrichment_metadata: Enrichment metadata dictionary
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        # Check method is statistical
        method = enrichment_metadata.get("method", "")
        if method == "statistical":
            results.append(ValidationResult(
                "passed",
                "Method is 'statistical' (no LLM used)"
            ))
        else:
            results.append(ValidationResult(
                "failed",
                f"Method must be 'statistical', got: '{method}'"
            ))
        
        # Check required libraries present
        libraries = enrichment_metadata.get("libraries", {})
        required_libs = ["yake", "summa", "scikit-learn"]
        missing_libs = [lib for lib in required_libs if lib not in libraries]
        
        if missing_libs:
            results.append(ValidationResult(
                "failed",
                f"Missing required libraries: {', '.join(missing_libs)}"
            ))
        else:
            results.append(ValidationResult(
                "passed",
                f"All required libraries present: {', '.join(required_libs)}"
            ))
        
        return results


class EnrichmentValidationOrchestrator:
    """
    Orchestrates all enrichment validation strategies.
    
    Pattern: Service Layer orchestration
    References:
        - ARCHITECTURE_GUIDELINES Ch.4: Service Layer Pattern
        - PYTHON_GUIDELINES Ch.8: Classes and OOP
    """
    
    def __init__(self, enriched_data: Dict[str, Any]):
        """
        Args:
            enriched_data: Enriched metadata dictionary from Tab 4
        """
        self.enriched_data = enriched_data
        self.all_results: List[ValidationResult] = []
    
    def validate_all(self) -> bool:
        """
        Run all validation strategies and report results.
        
        Returns:
            True if all validations passed, False otherwise
        """
        print("\n" + "="*70)
        print("Tab 4 Metadata Enrichment Validation")
        print("="*70)
        
        # Strategy 1: Structure validation
        print("\n1. Structure Validation")
        print("-" * 70)
        structure_results = EnrichmentStructureValidator.validate_structure(
            self.enriched_data
        )
        self._print_results(structure_results)
        self.all_results.extend(structure_results)
        
        # Strategy 2: Statistical method validation
        print("\n2. Statistical Method Validation")
        print("-" * 70)
        if "enrichment_metadata" in self.enriched_data:
            method_results = StatisticalMethodValidator.validate_method(
                self.enriched_data["enrichment_metadata"]
            )
            self._print_results(method_results)
            self.all_results.extend(method_results)
        else:
            print("⚠️  Skipping - enrichment_metadata not found")
        
        # Strategy 3: Content validation
        print("\n3. Enrichment Content Validation")
        print("-" * 70)
        if "chapters" in self.enriched_data:
            content_results = EnrichmentContentValidator.validate_content(
                self.enriched_data["chapters"]
            )
            self._print_results(content_results)
            self.all_results.extend(content_results)
        else:
            print("⚠️  Skipping - chapters not found")
        
        # Summary
        print("\n" + "="*70)
        print("Validation Summary")
        print("="*70)
        
        passed = sum(1 for r in self.all_results if r.is_passed())
        failed = sum(1 for r in self.all_results if r.is_failed())
        warnings = sum(1 for r in self.all_results if r.is_warning())
        
        print(f"✓ Passed:   {passed}")
        print(f"✗ Failed:   {failed}")
        print(f"⚠️ Warnings: {warnings}")
        print("="*70)
        
        success = failed == 0
        if success:
            print("\n✅ All validations passed!")
        else:
            print(f"\n❌ {failed} validation(s) failed")
        
        return success
    
    def _print_results(self, results: List[ValidationResult]) -> None:
        """Print validation results with appropriate icons."""
        for result in results:
            if result.is_passed():
                print(f"  ✓ {result.message}")
            elif result.is_failed():
                print(f"  ✗ {result.message}")
            elif result.is_warning():
                print(f"  ⚠️  {result.message}")
