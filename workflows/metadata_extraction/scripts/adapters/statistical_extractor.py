"""
Statistical metadata extractor using YAKE, Summa, and scikit-learn.

Domain-agnostic keyword extraction, concept identification, and summarization
that works across Python, biology, law, construction, and other domains.

Document References:
- DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN.md: Part 1.2 (Statistical NLP integration)
- ARCHITECTURE_GUIDELINES Ch. 4: Adapter pattern for external dependencies
- PYTHON_GUIDELINES Ch. 7: Class design, single responsibility principle
- BOOK_TAXONOMY_MATRIX: Architecture Patterns (Tier 1), Python Distilled (Tier 3)

TDD Status: GREEN phase - Minimal implementation to pass tests

Environment Variables (optional configuration):
- EXTRACTION_YAKE_TOP_N: Default top_n for keyword extraction (default: 20)
- EXTRACTION_YAKE_N: Max n-gram size for YAKE (default: 3)
- EXTRACTION_YAKE_DEDUPLIM: YAKE deduplication threshold (default: 0.9)
- EXTRACTION_STEM_DEDUP_ENABLED: Enable stem-based deduplication (default: true)
- EXTRACTION_NGRAM_CLEAN_ENABLED: Enable n-gram cleaning (default: true)
"""

import os
import re
from typing import List, Tuple, Set, Union, cast
import yake  # type: ignore[import-untyped]
from summa import keywords as summa_keywords, summarizer  # type: ignore[import-untyped]

# Try to import WordNet for dictionary validation
try:
    from nltk.corpus import wordnet
    _HAS_WORDNET = True
except ImportError:
    _HAS_WORDNET = False
    wordnet = None  # type: ignore


# Constants - Per PYTHON_GUIDELINES Ch. 6: Class constants for validation messages
_ERROR_EMPTY_TEXT = "Text cannot be empty"
_ERROR_INVALID_TOP_N = "top_n must be positive"
_ERROR_INVALID_RATIO = "ratio must be between 0.0 and 1.0"

# Technical term patterns that are valid even if not in WordNet
# These capture compound technical terms like "microservices", "asyncio", etc.
_TECHNICAL_SUFFIXES = frozenset([
    'api', 'apis', 'io', 'db', 'sql', 'orm', 'ui', 'ux', 'ml', 'ai', 'llm',
    'service', 'services', 'server', 'servers', 'client', 'clients',
    'handler', 'handlers', 'manager', 'managers', 'factory', 'factories',
    'pattern', 'patterns', 'model', 'models', 'view', 'views',
    'controller', 'controllers', 'adapter', 'adapters', 'wrapper', 'wrappers',
    'config', 'configs', 'setting', 'settings', 'option', 'options',
    'async', 'sync', 'thread', 'threads', 'process', 'processes',
    'queue', 'queues', 'cache', 'caches', 'pool', 'pools',
    'hook', 'hooks', 'callback', 'callbacks', 'listener', 'listeners',
    'parser', 'parsers', 'builder', 'builders', 'loader', 'loaders',
    'encoder', 'encoders', 'decoder', 'decoders', 'serializer', 'serializers',
])

# Known valid technical terms not in WordNet
_TECHNICAL_TERMS = frozenset([
    # Python/Programming
    'python', 'pythonic', 'microservices', 'microservice', 'asyncio', 'fastapi',
    'django', 'flask', 'sqlalchemy', 'pydantic', 'pytest', 'numpy', 'pandas',
    'tensorflow', 'pytorch', 'kubernetes', 'docker', 'redis', 'mongodb',
    'postgresql', 'graphql', 'restful', 'websocket', 'grpc', 'protobuf',
    # Architecture
    'refactoring', 'codebase', 'backend', 'frontend', 'middleware', 'endpoint',
    'api', 'sdk', 'cli', 'gui', 'orm', 'crud', 'mvc', 'mvvm',
    # Data/ML
    'dataset', 'dataframe', 'embeddings', 'vectorization', 'tokenization',
    'llm', 'llms', 'rag', 'langchain', 'openai', 'anthropic',
])

# Noise patterns to filter from YAKE/Summa extraction
# These are common artifacts from OCR, source watermarks, and code snippets
_NOISE_PATTERNS = [
    r'^_',              # Leading underscore (private variables like _add, _name)
    r'^[a-z]$',         # Single letters (a, b, c, n, o)
    r'^\d+$',           # Pure numbers
    r'^[A-Z]$',         # Single capital letters
    r'_$',              # Trailing underscore
    r'^__',             # Dunder prefixes
    r'__$',             # Dunder suffixes
]

# Known noise terms from OCR artifacts and book sources
_NOISE_TERMS = frozenset([
    # PDF/source watermarks
    'oceanofpdf', 'ebscohost', 'packt', 'manning', 'oreilly', 'springer',
    'wiley', 'apress', 'pragprog', 'nostarch', 'informit', 'pearson',
    # Common OCR artifacts
    'www', 'http', 'https', 'com', 'org', 'edu', 'gov', 'net',
    # Python builtins that are too generic
    'self', 'cls', 'def', 'class', 'return', 'import', 'from', 'none',
    'true', 'false', 'print', 'pass', 'break', 'continue', 'elif',
    # Test artifacts  
    'test', 'tests', 'testing', 'fixture', 'mock',
    # Generic noise
    'chapter', 'page', 'figure', 'table', 'example', 'note', 'see',
    'also', 'using', 'used', 'use', 'like', 'new', 'get', 'set',
    'one', 'two', 'first', 'second', 'next', 'following', 'previous',
])


def _is_in_dictionary(word: str) -> bool:
    """Check if word exists in WordNet dictionary."""
    if not _HAS_WORDNET or wordnet is None:
        return True  # If WordNet not available, allow all
    return bool(wordnet.synsets(word.lower()))


def _is_technical_term(word: str) -> bool:
    """Check if word is a known technical term or matches technical patterns."""
    word_lower = word.lower()
    
    # Check known technical terms
    if word_lower in _TECHNICAL_TERMS:
        return True
    
    # Check technical suffixes (e.g., "microservices" ends with "services")
    for suffix in _TECHNICAL_SUFFIXES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix):
            return True
    
    return False


def _is_valid_keyword(keyword: str) -> bool:
    """
    Filter out noisy keywords from YAKE extraction.
    
    Valid keywords should be:
    - At least 2 characters
    - Not match noise patterns (underscores, single chars, etc.)
    - Not be known noise terms (watermarks, builtins, etc.)
    
    Args:
        keyword: Keyword string to validate
        
    Returns:
        True if keyword is valid, False otherwise
    """
    if not keyword or len(keyword) < 2:
        return False
    
    keyword_lower = keyword.lower().strip()
    
    # Check against noise terms
    if keyword_lower in _NOISE_TERMS:
        return False
    
    # Check noise patterns
    for pattern in _NOISE_PATTERNS:
        if re.search(pattern, keyword_lower):
            return False
    
    return True


def _is_valid_concept(concept: str) -> bool:
    """
    Filter out noisy concepts from extraction.
    
    Valid concepts must:
    - Be at least 3 characters
    - Be alphabetic (no numbers, underscores)
    - Not be known noise terms
    - Not match noise patterns
    - Be either: in WordNet dictionary OR a known technical term
    
    This filters out proper nouns like "Valentina", "Paestum" that are
    statistically significant but not meaningful technical concepts.
    
    Args:
        concept: Concept string to validate
        
    Returns:
        True if concept is valid, False otherwise
    """
    if not concept or len(concept) < 3:
        return False
    
    concept_lower = concept.lower().strip()
    
    # Must be alphabetic
    if not concept_lower.isalpha():
        return False
    
    # Check against noise terms
    if concept_lower in _NOISE_TERMS:
        return False
    
    # Check noise patterns
    for pattern in _NOISE_PATTERNS:
        if re.search(pattern, concept_lower):
            return False
    
    # Must be a real word: in dictionary OR known technical term
    if not _is_in_dictionary(concept_lower) and not _is_technical_term(concept_lower):
        return False
    
    return True


def _get_word_stem(word: str) -> str:
    """
    Get a simple stem for a word by removing common suffixes.
    
    Uses a simple suffix-stripping approach rather than full stemmer
    to avoid heavy dependencies like NLTK's PorterStemmer.
    
    Per PYTHON_GUIDELINES Ch. 7: Simple, focused functions.
    
    Args:
        word: Word to stem
        
    Returns:
        Stemmed word (lowercase)
    """
    word = word.lower().strip()
    
    # Handle special case: words ending in 'es' where base ends in 'e'
    # e.g., "architectures" -> "architecture", "types" -> "type"
    if word.endswith('es') and len(word) > 4:
        # Check if removing just 's' gives a valid-looking stem
        potential_stem = word[:-1]  # Remove just 's'
        if potential_stem.endswith('e'):
            return potential_stem
    
    # Common English suffixes in order (more specific first)
    # Use minimum stem length to avoid over-stemming
    suffix_rules = [
        # (suffix, min_stem_length)
        ('ization', 3),
        ('isation', 3),
        ('ational', 3),
        ('fulness', 3),
        ('ousness', 3),
        ('iveness', 3),
        ('ement', 3),
        ('ation', 3),
        ('ening', 3),
        ('ising', 3),
        ('izing', 3),
        ('ively', 3),
        ('ously', 3),
        ('fully', 3),
        ('ness', 3),
        ('ment', 3),
        ('able', 3),
        ('ible', 3),
        ('ings', 3),
        ('tion', 3),
        ('sion', 3),
        ('ally', 3),
        ('edly', 3),
        ('ing', 4),  # Higher min to avoid "model" → "mod"
        ('ies', 3),
        ('ied', 3),
        ('ers', 3),
        ('ery', 3),
        ('est', 3),
        ('ful', 3),
        ('ish', 3),
        ('ity', 3),
        ('ive', 3),
        ('ous', 3),
        ('ly', 3),
        ('ed', 3),
        ('er', 3),
        ('s', 4),   # Only strip 's' from longer words
    ]
    
    for suffix, min_stem in suffix_rules:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if len(stem) >= min_stem:
                return stem
    
    return word


def _get_phrase_stem_signature(phrase: str) -> str:
    """
    Get a stem signature for a multi-word phrase.
    
    The signature is the sorted stems of all words, allowing
    detection of phrases with same conceptual meaning.
    
    Args:
        phrase: Multi-word phrase
        
    Returns:
        Sorted stem signature string
    """
    words = phrase.lower().split()
    stems = sorted(_get_word_stem(w) for w in words)
    return " ".join(stems)


def _deduplicate_by_stem(
    items: List[Tuple[str, float]] | List[str]
) -> List[Tuple[str, float]] | List[str]:
    """
    Deduplicate keywords/concepts by word stem.
    
    Keeps only the first occurrence of each stem, preserving
    order and scores. Handles both keyword tuples and concept strings.
    
    Per ARCHITECTURE_GUIDELINES Ch. 4: Single responsibility - dedup only.
    Per PYTHON_GUIDELINES Ch. 7: Function does one thing well.
    
    Args:
        items: List of (keyword, score) tuples or list of concept strings
        
    Returns:
        Deduplicated list in same format as input
        
    Examples:
        >>> _deduplicate_by_stem([("model", 0.01), ("models", 0.02)])
        [("model", 0.01)]
        >>> _deduplicate_by_stem(["model", "models", "data"])
        ["model", "data"]
    """
    if not items:
        return items
    
    seen_stems: Set[str] = set()
    result: List[Tuple[str, float]] | List[str] = []
    
    # Detect input type
    is_tuple_list = isinstance(items[0], tuple)
    
    for item in items:
        if is_tuple_list:
            keyword, score = item  # type: ignore
            stem_sig = _get_phrase_stem_signature(keyword)
            if stem_sig not in seen_stems:
                seen_stems.add(stem_sig)
                result.append((keyword, score))  # type: ignore
        else:
            # String list (concepts)
            concept = cast(str, item)
            stem = _get_word_stem(concept)
            if stem not in seen_stems:
                seen_stems.add(stem)
                result.append(concept)  # type: ignore
    
    return result


def _clean_ngram_duplicates(
    keywords: List[Tuple[str, float]]
) -> List[Tuple[str, float]]:
    """
    Remove n-grams that contain repeated words.
    
    Filters out phrases like "Models Models Applications" where
    a word appears more than once (case-insensitive).
    
    Per ARCHITECTURE_GUIDELINES: Remove noise from extraction.
    
    Args:
        keywords: List of (keyword, score) tuples
        
    Returns:
        Filtered list with no repeated-word n-grams
        
    Examples:
        >>> _clean_ngram_duplicates([("Models Models", 0.01), ("Machine Learning", 0.02)])
        [("Machine Learning", 0.02)]
    """
    if not keywords:
        return keywords
    
    result: List[Tuple[str, float]] = []
    
    for keyword, score in keywords:
        words = keyword.lower().split()
        # Check for repeated words (case-insensitive)
        if len(words) == len(set(words)):
            # No duplicates - keep this keyword
            result.append((keyword, score))
    
    return result


class StatisticalExtractor:
    """
    Adapter for statistical NLP libraries (YAKE, Summa, scikit-learn).
    
    Provides domain-agnostic metadata extraction without hardcoded keywords.
    Per ARCHITECTURE_GUIDELINES Ch. 4: Adapters isolate external dependencies.
    Per PYTHON_GUIDELINES Ch. 7: Single Responsibility - extraction only.
    
    Methods:
        extract_keywords: Extract keywords using YAKE (unsupervised)
        extract_concepts: Extract single-word concepts using Summa TextRank
        generate_summary: Generate extractive summary using Summa TextRank
    
    Example:
        >>> extractor = StatisticalExtractor()
        >>> keywords = extractor.extract_keywords("Python programming text...", top_n=10)
        >>> concepts = extractor.extract_concepts("Biology cell text...", top_n=5)
        >>> summary = extractor.generate_summary("Law contract text...", ratio=0.3)
    """
    
    def __init__(self):
        """
        Initialize YAKE keyword extractor with configurable parameters.
        
        Parameters can be overridden via environment variables:
        - EXTRACTION_YAKE_TOP_N: Default top_n (default: 20)
        - EXTRACTION_YAKE_N: Max n-gram size (default: 3)
        - EXTRACTION_YAKE_DEDUPLIM: Deduplication threshold (default: 0.9)
        - EXTRACTION_STEM_DEDUP_ENABLED: Enable stem deduplication (default: true)
        - EXTRACTION_NGRAM_CLEAN_ENABLED: Enable n-gram cleaning (default: true)
        
        YAKE Configuration (per research - see DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN):
        - lan='en': English language
        - n: Max n-gram size (1-3 words by default)
        - dedupLim: Deduplication threshold (0.9 by default)
        - top: Default number of keywords (overridden by top_n parameter)
        
        Per PYTHON_GUIDELINES Ch. 7: Initialize dependencies in __init__.
        """
        # Read configuration from environment variables
        self.default_top_n = int(os.environ.get("EXTRACTION_YAKE_TOP_N", "20"))
        yake_n = int(os.environ.get("EXTRACTION_YAKE_N", "3"))
        yake_deduplim = float(os.environ.get("EXTRACTION_YAKE_DEDUPLIM", "0.9"))
        
        # Deduplication flags
        self.stem_dedup_enabled = os.environ.get("EXTRACTION_STEM_DEDUP_ENABLED", "true").lower() == "true"
        self.ngram_clean_enabled = os.environ.get("EXTRACTION_NGRAM_CLEAN_ENABLED", "true").lower() == "true"
        
        self.kw_extractor = yake.KeywordExtractor(
            lan='en',
            n=yake_n,
            dedupLim=yake_deduplim,
            top=self.default_top_n,
            features=None
        )
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[Tuple[str, float]]:
        """
        Extract keywords using YAKE (Yet Another Keyword Extractor).
        
        YAKE is unsupervised and domain-agnostic - works on Python, biology,
        law, construction, and any other domain without training data.
        
        Args:
            text: Input text to extract keywords from
            top_n: Number of top keywords to return (default: 20)
        
        Returns:
            List of (keyword, score) tuples sorted by score (ascending).
            Lower YAKE scores indicate more important keywords.
        
        Raises:
            ValueError: If text is empty or top_n is invalid
        
        Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Part 1.2.1 (YAKE integration)
        - PYTHON_GUIDELINES Ch. 8: Input validation and error handling
        
        Example:
            >>> extractor = StatisticalExtractor()
            >>> keywords = extractor.extract_keywords("Python is a programming language", top_n=5)
            >>> # Returns: [('programming language', 0.05), ('python', 0.12), ...]
        """
        # Input validation - Per PYTHON_GUIDELINES Ch. 8
        if not text or not text.strip():
            raise ValueError(_ERROR_EMPTY_TEXT)
        
        if top_n <= 0:
            raise ValueError(_ERROR_INVALID_TOP_N)
        
        # Extract keywords using YAKE (request more to account for filtering)
        keywords = self.kw_extractor.extract_keywords(text)
        
        # Step 1: Filter out noisy keywords
        filtered_keywords = [(kw, score) for kw, score in keywords if _is_valid_keyword(kw)]
        
        # Step 2: Remove n-grams with repeated words (e.g., "Models Models")
        if self.ngram_clean_enabled:
            cleaned_keywords = _clean_ngram_duplicates(filtered_keywords)
        else:
            cleaned_keywords = filtered_keywords
        
        # Step 3: Deduplicate by stem (e.g., model/models/modeling → model)
        if self.stem_dedup_enabled:
            deduped_keywords = cast(List[Tuple[str, float]], _deduplicate_by_stem(cleaned_keywords))
        else:
            deduped_keywords = cleaned_keywords
        
        # Return top N keywords (already sorted by score ascending)
        return deduped_keywords[:top_n]
    
    def _extract_concepts_from_summa(self, text: str, top_n: int) -> List[str]:
        """
        Extract concepts using Summa TextRank.
        
        Helper method extracted to reduce cognitive complexity.
        
        Args:
            text: Input text
            top_n: Number of concepts to extract
            
        Returns:
            List of concepts or empty list on failure
        """
        try:
            # Request more than needed to account for filtering
            concepts = summa_keywords.keywords(text, words=top_n * 2, split=True)
            if not concepts:
                return []
            # Filter noisy concepts
            return [c for c in concepts if _is_valid_concept(c)][:top_n]
        except Exception:
            return []
    
    def _extract_concepts_from_keywords(self, text: str, top_n: int) -> List[str]:
        """
        Fallback: Extract single-word concepts from YAKE keywords.
        
        Helper method extracted to reduce cognitive complexity.
        
        Args:
            text: Input text
            top_n: Number of concepts to extract
            
        Returns:
            List of concepts or empty list on failure
        """
        try:
            keywords = self.kw_extractor.extract_keywords(text)
            concept_set = set()
            
            for keyword, score in keywords:
                # Split multi-word keywords into single words
                words = keyword.lower().split()
                for word in words:
                    # Use semantic filter instead of basic length/alpha check
                    if _is_valid_concept(word):
                        concept_set.add(word)
                        if len(concept_set) >= top_n:
                            break
                if len(concept_set) >= top_n:
                    break
            
            return list(concept_set)[:top_n]
        except Exception:
            return []
    
    def extract_concepts(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract single-word concepts using Summa TextRank keywords.
        
        TextRank is a graph-based algorithm that identifies important words
        based on their connections to other words in the text.
        
        Fallback: If Summa fails (short text, code-heavy, poor OCR), extracts
        concepts from keywords as a fallback to ensure metadata completeness.
        
        Args:
            text: Input text to extract concepts from
            top_n: Number of top concepts to return (default: 10)
        
        Returns:
            List of concept strings (single words) sorted by importance.
        
        Raises:
            ValueError: If text is empty or top_n is invalid
        
        Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Part 1.2.2 (Summa integration)
        - PYTHON_GUIDELINES Ch. 8: Input validation
        
        Example:
            >>> extractor = StatisticalExtractor()
            >>> concepts = extractor.extract_concepts("Biology cell text", top_n=5)
            >>> # Returns: ['cell', 'biology', 'protein', ...]
        """
        # Input validation
        if not text or not text.strip():
            raise ValueError(_ERROR_EMPTY_TEXT)
        
        if top_n <= 0:
            raise ValueError(_ERROR_INVALID_TOP_N)
        
        # Try Summa first (request more to account for deduplication)
        concepts = self._extract_concepts_from_summa(text, top_n * 2)
        
        # Fallback to YAKE keywords if Summa fails
        if not concepts:
            concepts = self._extract_concepts_from_keywords(text, top_n * 2)
        
        # Deduplicate by stem (e.g., model/models/modeling → model)
        deduped_concepts = cast(List[str], _deduplicate_by_stem(concepts))
        
        # Return top_n concepts
        return deduped_concepts[:top_n] if deduped_concepts else []
    
    def generate_summary(self, text: str, ratio: float = 0.2) -> str:
        """
        Generate extractive summary using Summa TextRank summarization.
        
        TextRank selects the most important sentences from the original text
        to create a summary. This is domain-agnostic and preserves context.
        
        Args:
            text: Input text to summarize
            ratio: Proportion of text to keep (0.0-1.0, default: 0.2 = 20%)
        
        Returns:
            Summary string containing complete sentences from original text.
        
        Raises:
            ValueError: If text is empty or ratio is invalid
        
        Document References:
        - DOMAIN_AGNOSTIC_IMPLEMENTATION_PLAN: Part 1.2.3 (Summarization)
        - PYTHON_GUIDELINES Ch. 8: Error handling
        
        Example:
            >>> extractor = StatisticalExtractor()
            >>> summary = extractor.generate_summary("Long text...", ratio=0.3)
            >>> # Returns: "Most important sentence. Another key point."
        """
        # Input validation
        if not text or not text.strip():
            raise ValueError(_ERROR_EMPTY_TEXT)
        
        if not 0.0 < ratio <= 1.0:
            raise ValueError(_ERROR_INVALID_RATIO)
        
        # Generate summary using Summa
        try:
            summary = summarizer.summarize(text, ratio=ratio)
        except Exception:
            # Summa can fail on very short text - return first sentence
            sentences = text.split('.')
            summary = sentences[0] + '.' if sentences else text
        
        # Return summary (Summa returns string)
        return summary if summary else text.split('.')[0] + '.'

    # =========================================================================
    # Safe Methods - Graceful degradation without exceptions
    # =========================================================================
    # 
    # These methods wrap the original extraction methods with try/except
    # to return empty results instead of raising exceptions on invalid input.
    # 
    # Use Case: Per-chapter processing in generate_metadata_universal.py
    # where a single bad chapter should not crash the entire book.
    #
    # Document References:
    # - ANTI_PATTERN_ANALYSIS.md: Section 1.3 (Missing Type Guards)
    # - ARCHITECTURE_GUIDELINES Ch. 8: Graceful degradation pattern
    # - PYTHON_GUIDELINES Ch. 8: EAFP error handling
    # =========================================================================

    def safe_extract_keywords(
        self, 
        text: str | None, 
        top_n: int = 20
    ) -> List[Tuple[str, float]]:
        """
        Safely extract keywords - returns empty list on invalid input.
        
        This method never raises exceptions. It returns an empty list for:
        - None input
        - Empty string input
        - Whitespace-only input
        - Any extraction failure
        
        Args:
            text: Input text (can be None, empty, or whitespace)
            top_n: Number of top keywords to return (default: 20)
        
        Returns:
            List of (keyword, score) tuples, or empty list on failure.
            
        Example:
            >>> extractor = StatisticalExtractor()
            >>> extractor.safe_extract_keywords("")  # Returns []
            >>> extractor.safe_extract_keywords(None)  # Returns []
            >>> extractor.safe_extract_keywords("Valid text")  # Returns keywords
        """
        # Guard: None or empty input
        if text is None or not text.strip():
            return []
        
        # Guard: Invalid top_n
        if top_n <= 0:
            return []
        
        try:
            return self.extract_keywords(text, top_n=top_n)
        except Exception:
            # Any failure returns empty list
            return []

    def safe_extract_concepts(
        self, 
        text: str | None, 
        top_n: int = 10
    ) -> List[str]:
        """
        Safely extract concepts - returns empty list on invalid input.
        
        This method never raises exceptions. It returns an empty list for:
        - None input
        - Empty string input
        - Whitespace-only input
        - Any extraction failure
        
        Args:
            text: Input text (can be None, empty, or whitespace)
            top_n: Number of top concepts to return (default: 10)
        
        Returns:
            List of concept strings, or empty list on failure.
            
        Example:
            >>> extractor = StatisticalExtractor()
            >>> extractor.safe_extract_concepts("")  # Returns []
            >>> extractor.safe_extract_concepts(None)  # Returns []
            >>> extractor.safe_extract_concepts("Valid text")  # Returns concepts
        """
        # Guard: None or empty input
        if text is None or not text.strip():
            return []
        
        # Guard: Invalid top_n
        if top_n <= 0:
            return []
        
        try:
            return self.extract_concepts(text, top_n=top_n)
        except Exception:
            # Any failure returns empty list
            return []

    def safe_generate_summary(
        self, 
        text: str | None, 
        ratio: float = 0.2,
        fallback: str = ""
    ) -> str:
        """
        Safely generate summary - returns fallback on invalid input.
        
        This method never raises exceptions. It returns the fallback for:
        - None input
        - Empty string input
        - Whitespace-only input
        - Any summarization failure
        
        Args:
            text: Input text (can be None, empty, or whitespace)
            ratio: Proportion of text to keep (default: 0.2)
            fallback: String to return on failure (default: "")
                      Typically: f"Chapter {num}: {title}"
        
        Returns:
            Summary string, or fallback on failure.
            
        Example:
            >>> extractor = StatisticalExtractor()
            >>> extractor.safe_generate_summary("")  # Returns ""
            >>> extractor.safe_generate_summary("", fallback="Chapter 1: Intro")
            'Chapter 1: Intro'
            >>> extractor.safe_generate_summary("Valid long text...")  # Returns summary
        """
        # Guard: None or empty input
        if text is None or not text.strip():
            return fallback
        
        # Guard: Invalid ratio
        if not 0.0 < ratio <= 1.0:
            return fallback
        
        try:
            summary = self.generate_summary(text, ratio=ratio)
            return summary if summary else fallback
        except Exception:
            # Any failure returns fallback
            return fallback
