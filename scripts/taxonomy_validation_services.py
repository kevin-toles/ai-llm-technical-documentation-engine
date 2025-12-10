"""
Tab 3 Taxonomy Validation Service Layer

Architecture Pattern: Service Layer + Strategy Pattern
Reference: Architecture Patterns Ch. 4 (Service Layer), Ch. 13 (Strategy Pattern)

Services:
- TaxonomyStructureValidator: Validates JSON structure (tiers, priority, concepts keys)
- TierCategorizationValidator: Validates 3-tier structure and priority ordering
- ConceptDeduplicationValidator: Validates no duplicate concepts within tiers
- TaxonomyValidationOrchestrator: Orchestrates all validation strategies
- ValidationResultFormatter: Formats and prints results

References:
    - MASTER_IMPLEMENTATION_GUIDE Task 2.1
    - ARCHITECTURE_GUIDELINES Ch.4: Service Layer Pattern
    - PYTHON_GUIDELINES Ch.8: Classes and OOP
"""

from typing import Dict, List, Any, Optional
from collections import Counter


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


class TaxonomyStructureValidator:
    """
    Validates taxonomy JSON structure.
    
    Pattern: Strategy Pattern (one validation strategy)
    References:
        - ARCHITECTURE_GUIDELINES Ch.13: Strategy Pattern
    """
    
    @staticmethod
    def validate_structure(taxonomy: Dict[str, Any]) -> List[ValidationResult]:
        """
        Validate taxonomy has required structure.
        
        Required structure:
        {
            "tiers": {
                "tier_name": {
                    "priority": int,
                    "concepts": List[str]
                }
            }
        }
        
        Args:
            taxonomy: Taxonomy dictionary to validate
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        # Check top-level 'tiers' key
        if "tiers" not in taxonomy:
            results.append(ValidationResult(
                "failed",
                "Missing required top-level 'tiers' key"
            ))
            return results
        
        results.append(ValidationResult(
            "passed",
            "Top-level 'tiers' key present"
        ))
        
        tiers = taxonomy["tiers"]
        
        if not isinstance(tiers, dict):
            results.append(ValidationResult(
                "failed",
                "'tiers' must be a dictionary"
            ))
            return results
        
        # Validate each tier structure
        for tier_name, tier_data in tiers.items():
            if not isinstance(tier_data, dict):
                results.append(ValidationResult(
                    "failed",
                    f"Tier '{tier_name}' must be a dictionary"
                ))
                continue
            
            # Check required keys
            if "priority" not in tier_data:
                results.append(ValidationResult(
                    "failed",
                    f"Tier '{tier_name}' missing required 'priority' key"
                ))
            elif not isinstance(tier_data["priority"], int):
                results.append(ValidationResult(
                    "failed",
                    f"Tier '{tier_name}' priority must be an integer"
                ))
            else:
                results.append(ValidationResult(
                    "passed",
                    f"Tier '{tier_name}' has valid priority: {tier_data['priority']}"
                ))
            
            if "concepts" not in tier_data:
                results.append(ValidationResult(
                    "failed",
                    f"Tier '{tier_name}' missing required 'concepts' key"
                ))
            elif not isinstance(tier_data["concepts"], list):
                results.append(ValidationResult(
                    "failed",
                    f"Tier '{tier_name}' concepts must be a list"
                ))
            else:
                results.append(ValidationResult(
                    "passed",
                    f"Tier '{tier_name}' has {len(tier_data['concepts'])} concepts"
                ))
        
        return results


class TierCategorizationValidator:
    """
    Validates tier categorization and priority ordering.
    
    Pattern: Strategy Pattern (one validation strategy)
    References:
        - ARCHITECTURE_GUIDELINES Ch.13: Strategy Pattern
    """
    
    EXPECTED_TIERS = {"architecture", "implementation", "practices"}
    EXPECTED_PRIORITIES = {
        "architecture": 1,
        "implementation": 2,
        "practices": 3
    }
    
    @staticmethod
    def validate_tiers(taxonomy: Dict[str, Any]) -> List[ValidationResult]:
        """
        Validate 3-tier structure and priority ordering.
        
        Expected tiers:
        - architecture (priority 1)
        - implementation (priority 2)
        - practices (priority 3)
        
        Args:
            taxonomy: Taxonomy dictionary to validate
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        if "tiers" not in taxonomy:
            results.append(ValidationResult(
                "failed",
                "Cannot validate tier categorization: missing 'tiers' key"
            ))
            return results
        
        tiers = taxonomy["tiers"]
        tier_names = set(tiers.keys())
        
        # Check for expected tiers
        missing_tiers = TierCategorizationValidator.EXPECTED_TIERS - tier_names
        extra_tiers = tier_names - TierCategorizationValidator.EXPECTED_TIERS
        
        if missing_tiers:
            results.append(ValidationResult(
                "failed",
                f"Missing required tiers: {', '.join(sorted(missing_tiers))}"
            ))
        else:
            results.append(ValidationResult(
                "passed",
                "All required tiers present (architecture, implementation, practices)"
            ))
        
        if extra_tiers:
            results.append(ValidationResult(
                "warning",
                f"Unexpected additional tiers: {', '.join(sorted(extra_tiers))}"
            ))
        
        # Validate priority ordering
        for tier_name, expected_priority in TierCategorizationValidator.EXPECTED_PRIORITIES.items():
            if tier_name in tiers:
                tier_data = tiers[tier_name]
                actual_priority = tier_data.get("priority")
                
                if actual_priority == expected_priority:
                    results.append(ValidationResult(
                        "passed",
                        f"Tier '{tier_name}' has correct priority: {actual_priority}"
                    ))
                else:
                    results.append(ValidationResult(
                        "failed",
                        f"Tier '{tier_name}' has incorrect priority: "
                        f"{actual_priority} (expected {expected_priority})"
                    ))
        
        return results


class ConceptDeduplicationValidator:
    """
    Validates concept deduplication within tiers.
    
    Pattern: Strategy Pattern (one validation strategy)
    References:
        - ARCHITECTURE_GUIDELINES Ch.13: Strategy Pattern
    """
    
    @staticmethod
    def _validate_tier_duplicates(
        tier_name: str, 
        tier_data: Dict[str, Any]
    ) -> Optional["ValidationResult"]:
        """
        Validate a single tier for duplicate concepts.
        
        Extracted to reduce cognitive complexity.
        """
        if "concepts" not in tier_data:
            return None
        
        concepts = tier_data["concepts"]
        if not isinstance(concepts, list):
            return None
        
        concept_counts = Counter(concepts)
        duplicates = {c: count for c, count in concept_counts.items() if count > 1}
        
        if duplicates:
            return ValidationResult(
                "failed",
                f"Tier '{tier_name}' has duplicate concepts: " +
                ", ".join([f"{c} ({count}x)" for c, count in duplicates.items()])
            )
        return ValidationResult(
            "passed",
            f"Tier '{tier_name}' has no duplicate concepts ({len(concepts)} unique)"
        )
    
    @staticmethod
    def _analyze_cross_tier_concepts(tiers: Dict[str, Any]) -> Optional["ValidationResult"]:
        """
        Analyze concepts appearing in multiple tiers.
        
        Extracted to reduce cognitive complexity.
        """
        all_concepts: Dict[str, List[str]] = {}
        for tier_name, tier_data in tiers.items():
            if "concepts" in tier_data:
                for concept in tier_data["concepts"]:
                    if concept not in all_concepts:
                        all_concepts[concept] = []
                    all_concepts[concept].append(tier_name)
        
        cross_tier_concepts = {c: t for c, t in all_concepts.items() if len(t) > 1}
        
        if cross_tier_concepts:
            return ValidationResult(
                "passed",  # Not a failure - this is allowed
                f"{len(cross_tier_concepts)} concepts appear in multiple tiers "
                f"(e.g., {list(cross_tier_concepts.keys())[:3]})"
            )
        return None
    
    @classmethod
    def validate_deduplication(cls, taxonomy: Dict[str, Any]) -> List["ValidationResult"]:
        """
        Validate no duplicate concepts within same tier.
        
        Note: Same concept can appear in different tiers (e.g., 'class' can have
        both architectural and implementation aspects).
        
        Args:
            taxonomy: Taxonomy dictionary to validate
            
        Returns:
            List of ValidationResult objects
        """
        results = []
        
        if "tiers" not in taxonomy:
            results.append(ValidationResult(
                "failed",
                "Cannot validate deduplication: missing 'tiers' key"
            ))
            return results
        
        tiers = taxonomy["tiers"]
        
        for tier_name, tier_data in tiers.items():
            result = cls._validate_tier_duplicates(tier_name, tier_data)
            if result:
                results.append(result)
        
        cross_tier_result = cls._analyze_cross_tier_concepts(tiers)
        if cross_tier_result:
            results.append(cross_tier_result)
        
        return results


class TaxonomyValidationOrchestrator:
    """
    Orchestrates all taxonomy validation strategies.
    
    Pattern: Service Layer + Facade
    References:
        - ARCHITECTURE_GUIDELINES Ch.4: Service Layer Pattern
    """
    
    def __init__(self, taxonomy: Dict[str, Any]):
        """
        Args:
            taxonomy: Taxonomy dictionary to validate
        """
        self.taxonomy = taxonomy
        self.all_results: List[ValidationResult] = []
    
    def validate_all(self) -> bool:
        """
        Run all validation strategies and return overall success.
        
        Returns:
            True if all validations passed, False otherwise
        """
        print("\n🔍 Validating Taxonomy Structure...")
        print("=" * 70)
        
        # Run all validators
        validators = [
            ("Structure", TaxonomyStructureValidator.validate_structure),
            ("Tier Categorization", TierCategorizationValidator.validate_tiers),
            ("Concept Deduplication", ConceptDeduplicationValidator.validate_deduplication)
        ]
        
        for validator_name, validator_func in validators:
            print(f"\n📋 {validator_name}:")
            results = validator_func(self.taxonomy)
            self.all_results.extend(results)
            
            for result in results:
                if result.is_passed():
                    icon = "✓"
                elif result.is_warning():
                    icon = "⚠️"
                else:
                    icon = "✗"
                print(f"  {icon} {result.message}")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Validation Summary")
        print("=" * 70)
        
        passed = sum(1 for r in self.all_results if r.is_passed())
        failed = sum(1 for r in self.all_results if r.is_failed())
        warnings = sum(1 for r in self.all_results if r.is_warning())
        
        print(f"  Passed:   {passed}")
        print(f"  Failed:   {failed}")
        print(f"  Warnings: {warnings}")
        
        overall_success = failed == 0
        
        if overall_success:
            print("\n✅ All validations passed!")
        else:
            print(f"\n❌ {failed} validation(s) failed")
        
        print("=" * 70 + "\n")
        
        return overall_success
