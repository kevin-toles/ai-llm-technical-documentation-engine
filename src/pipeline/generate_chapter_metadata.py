#!/usr/bin/env python3
"""
Generate Chapter Metadata: Summaries, Keywords, and Concepts

This script extracts chapter summaries, keywords, and key concepts from 
all 15 book JSON files and updates the chapter_metadata_cache.json file.

For each chapter in each book:
1. Reads the chapter's page content from the JSON
2. Extracts keywords and concepts from the text
3. Generates a brief summary of the chapter's main topics
4. Updates the metadata cache with this information

Usage:
    python3 generate_chapter_metadata.py

Reference: 
- Python Distilled Ch. 7 - Dataclass configuration patterns
- Python Distilled Ch. 9 - pathlib.Path operations  
- Microservices Up and Running Ch. 7 - 12-Factor App configuration
"""

import json
import re
from typing import List, Dict, Any, Tuple
from collections import Counter

# Configuration management (12-Factor App pattern)
from config.settings import settings

# Book locations (simplified - all books now in textbooks_json_dir root)
# Reference: Microservices Ch. 7 - Externalized configuration
BOOK_PATHS = {
    "Fluent Python 2nd.json": "",
    "Python Distilled.json": "",
    "Python Essential Reference 4th.json": "",
    "Python Cookbook 3rd.json": "",
    "Learning Python Ed6.json": "",
    "Python Data Analysis 3rd.json": "",
    "Architecture Patterns with Python.json": "",
    "Python Architecture Patterns.json": "",
    "Building Microservices.json": "",
    "Microservice Architecture.json": "",
    "Microservices Up and Running.json": "",
    "Building Python Microservices with FastAPI.json": "",
    "Microservice APIs Using Python Flask FastAPI.json": "",
    "Python Microservices Development.json": ""
}

def _get_python_keyword_list() -> List[str]:
    """Return comprehensive list of Python and programming keywords to detect."""
    return [
        # Core language
        'class', 'function', 'method', 'decorator', 'generator', 'iterator',
        'closure', 'lambda', 'comprehension', 'exception', 'inheritance',
        'module', 'package', 'import', 'namespace', 'scope', 'variable',
        'type', 'object', 'attribute', 'property', 'descriptor',
        'metaclass', 'protocol', 'interface', 'abstract', 'polymorphism',
        'encapsulation', 'composition', 'mixin', 
        
        # Async/Concurrency
        'threading', 'async', 'await', 'coroutine', 'asyncio',
        'concurrent', 'parallel', 'multiprocessing',
        
        # I/O and Data
        'file', 'io', 'stream', 'context manager',
        'serialization', 'pickle', 'json', 'xml', 'csv', 'database',
        'encoding', 'decoding', 'buffer',
        
        # Testing/Quality
        'testing', 'unittest', 'pytest', 'debugging', 'profiling', 
        'optimization', 'performance', 'benchmark',
        
        # Architecture/Design
        'pattern', 'architecture', 'design', 'refactoring',
        'microservice', 'api', 'rest', 'http', 'web', 'server',
        'client', 'endpoint', 'route', 'middleware',
        
        # Data Structures
        'data structure', 'algorithm', 'sorting', 'searching',
        'list', 'dict', 'dictionary', 'set', 'tuple', 'string', 
        'bytes', 'array', 'queue', 'stack', 'tree', 'graph', 
        'hash', 'collection', 'sequence',
        
        # Types
        'int', 'integer', 'float', 'bool', 'boolean', 'str',
        'none', 'type hint', 'annotation', 'typing',
        
        # Advanced
        'metaprogramming', 'reflection', 'introspection',
        'bytecode', 'compilation', 'interpretation',
        'memory management', 'garbage collection',
        
        # Common operations
        'loop', 'iteration', 'recursion', 'conditional',
        'expression', 'statement', 'operator', 'operand',
        'assignment', 'comparison', 'logic', 'bitwise',
        
        # Error handling
        'error', 'exception', 'traceback', 'assertion',
        'validation', 'sanitization',
        
        # OOP specific
        'constructor', 'destructor', 'instance', 'subclass',
        'superclass', 'override', 'overload', 'static method',
        'class method', 'instance method', 'property',
        
        # Functional
        'map', 'filter', 'reduce', 'zip', 'enumerate',
        'higher-order', 'immutable', 'pure function',
    ]


def _extract_capitalized_terms(text: str, existing_keywords: List[tuple]) -> List[tuple]:
    """Extract frequently occurring capitalized terms from text."""
    cap_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
    capitalized = re.findall(cap_pattern, text)
    cap_counter = Counter(capitalized)
    
    existing_kw_set = {k[0] for k in existing_keywords}
    cap_keywords = []
    
    for term, count in cap_counter.most_common(15):
        if count >= 2 and len(term) > 3 and term.lower() not in existing_kw_set:
            cap_keywords.append((term.lower(), count))
    
    return cap_keywords


def _get_stop_words() -> set:
    """Return set of common English stop words to filter out."""
    return {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
            'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about',
            'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'under', 'again', 'further', 'then',
            'once', 'here', 'there', 'when', 'where', 'why', 'how',
            'all', 'both', 'each', 'few', 'more', 'most', 'other',
            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
            'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should'}


def _extract_frequent_words(text_lower: str, existing_keywords: List[tuple]) -> List[tuple]:
    """Extract frequently occurring words when few keywords found."""
    stop_words = _get_stop_words()
    words = re.findall(r'\b[a-z]{4,}\b', text_lower)
    word_counter = Counter(w for w in words if w not in stop_words)
    
    existing_kw_set = {k[0] for k in existing_keywords}
    freq_keywords = []
    
    for word, count in word_counter.most_common(20):
        if count >= 3 and word not in existing_kw_set:
            freq_keywords.append((word, count))
    
    return freq_keywords


def extract_keywords_from_text(text: str, max_keywords: int = 15) -> List[str]:
    """
    Extract meaningful keywords from chapter text.
    
    Identifies technical terms, Python concepts, and key topics.
    """
    text_lower = text.lower()
    
    # Find Python/programming keywords in text
    python_keywords = _get_python_keyword_list()
    found_keywords = []
    
    for keyword in python_keywords:
        count = text_lower.count(keyword)
        if count >= 1:
            found_keywords.append((keyword, count))
    
    # Sort by frequency
    found_keywords.sort(key=lambda x: x[1], reverse=True)
    
    # Add capitalized terms (likely class names, concepts)
    cap_keywords = _extract_capitalized_terms(text, found_keywords)
    found_keywords.extend(cap_keywords)
    
    # Add frequent words if still few keywords
    if len(found_keywords) < 5:
        freq_keywords = _extract_frequent_words(text_lower, found_keywords)
        found_keywords.extend(freq_keywords)
    
    # Return top keywords
    return [kw[0] for kw in found_keywords[:max_keywords]]


# Comprehensive list of technical concept patterns to detect
CONCEPT_PATTERNS = [
    # OOP Concepts
    r'\b(object[- ]oriented programming)\b',
    r'\b(class hierarchy)\b',
    r'\b(inheritance)\b',
    r'\b(polymorphism)\b',
    r'\b(encapsulation)\b',
    r'\b(multiple inheritance)\b',
    r'\b(method resolution order)\b',
    r'\b(abstract base class[es]*)\b',
    
    # Functional Programming
    r'\b(functional programming)\b',
    r'\b(higher[- ]order function[s]*)\b',
    r'\b(first[- ]class function[s]*)\b',
    r'\b(closure[s]*)\b',
    r'\b(lambda function[s]*)\b',
    
    # Python Features
    r'\b(list comprehension[s]*)\b',
    r'\b(dict comprehension[s]*)\b',
    r'\b(generator expression[s]*)\b',
    r'\b(generator[s]*)\b',
    r'\b(iterator[s]*)\b',
    r'\b(decorator[s]*)\b',
    r'\b(decorator pattern[s]*)\b',
    r'\b(context manager[s]*)\b',
    r'\b(special method[s]*)\b',
    r'\b(magic method[s]*)\b',
    r'\b(dunder method[s]*)\b',
    r'\b(data model)\b',
    r'\b(type hint[s]*)\b',
    r'\b(type annotation[s]*)\b',
    r'\b(duck typing)\b',
    r'\b(dynamic typing)\b',
    
    # Async/Concurrency
    r'\b(async[/ ]await)\b',
    r'\b(coroutine[s]*)\b',
    r'\b(asynchronous programming)\b',
    r'\b(concurrency)\b',
    r'\b(parallel processing)\b',
    r'\b(threading)\b',
    r'\b(multiprocessing)\b',
    
    # Architecture/Design
    r'\b(design pattern[s]*)\b',
    r'\b(architectural pattern[s]*)\b',
    r'\b(dependency injection)\b',
    r'\b(microservice[s]*)\b',
    r'\b(service[- ]oriented architecture)\b',
    r'\b(api design)\b',
    r'\b(rest[ful]* api[s]*)\b',
    r'\b(repository pattern)\b',
    r'\b(factory pattern)\b',
    r'\b(singleton pattern)\b',
    
    # Data Structures
    r'\b(data structure[s]*)\b',
    r'\b(linked list[s]*)\b',
    r'\b(hash table[s]*)\b',
    r'\b(binary tree[s]*)\b',
    r'\b(graph[s]*)\b',
    r'\b(queue[s]*)\b',
    r'\b(stack[s]*)\b',
    
    # Testing/Debugging
    r'\b(unit test[s]*)\b',
    r'\b(integration test[s]*)\b',
    r'\b(test[- ]driven development)\b',
    r'\b(debugging)\b',
    r'\b(profiling)\b',
    
    # Error Handling
    r'\b(exception handling)\b',
    r'\b(error handling)\b',
    r'\b(exception[s]*)\b',
    r'\b(try[- ]except)\b',
    
    # I/O and Data
    r'\b(file handling)\b',
    r'\b(file i[/]o)\b',
    r'\b(input[/ ]output)\b',
    r'\b(serialization)\b',
    r'\b(deserialization)\b',
    r'\b(json parsing)\b',
    r'\b(xml processing)\b',
    
    # String/Text
    r'\b(string manipulation)\b',
    r'\b(regular expression[s]*)\b',
    r'\b(text processing)\b',
    r'\b(string formatting)\b',
    
    # Modules/Packages
    r'\b(module[s]*)\b',
    r'\b(package[s]*)\b',
    r'\b(import system)\b',
    r'\b(namespace[s]*)\b',
]


def _find_pattern_matches(text_lower: str) -> List[Tuple[str, int]]:
    """Find all concept pattern matches in text."""
    concept_counts = []
    for pattern in CONCEPT_PATTERNS:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            concept = matches[0] if isinstance(matches[0], str) else matches[0][0]
            count = len(matches)
            if count >= 1:
                concept_counts.append((concept.strip(), count))
    return concept_counts


def _extract_noun_phrases(text: str, existing_concepts: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """Extract noun phrases as fallback when few concepts found."""
    noun_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[a-z]+){0,2})\b', text)
    phrase_counter = Counter(noun_phrases)
    
    additional_concepts = []
    for phrase, count in phrase_counter.most_common(15):
        if count >= 2 and len(phrase) > 3:
            if not any(phrase.lower() in c[0].lower() for c in existing_concepts):
                additional_concepts.append((phrase.lower(), count))
    
    return additional_concepts


def _deduplicate_concepts(concept_counts: List[Tuple[str, int]], max_concepts: int) -> List[str]:
    """Remove duplicates and return top concepts."""
    concept_counts.sort(key=lambda x: x[1], reverse=True)
    
    seen = set()
    unique_concepts = []
    for concept, _count in concept_counts:
        concept_clean = concept.strip().lower()
        if concept_clean not in seen:
            seen.add(concept_clean)
            unique_concepts.append(concept)
    
    return unique_concepts[:max_concepts]


def extract_concepts_from_text(text: str, max_concepts: int = 10) -> List[str]:
    """
    Extract key concepts discussed in the chapter.
    
    Focuses on multi-word technical phrases and important topics.
    """
    text_lower = text.lower()
    
    # Find pattern-based concepts
    concept_counts = _find_pattern_matches(text_lower)
    
    # Fallback to noun phrases if few concepts found
    if len(concept_counts) < 3:
        concept_counts.extend(_extract_noun_phrases(text, concept_counts))
    
    return _deduplicate_concepts(concept_counts, max_concepts)


def _extract_sample_text(chapter_pages: List[Dict[str, Any]], num_pages: int = 5) -> str:
    """Extract sample text from first N pages for analysis."""
    sample_text = ""
    for page in chapter_pages[:num_pages]:
        sample_text += page.get('content', '') + " "
    return sample_text


def _find_introductory_sentences(sample_text: str, max_sentences: int = 20) -> List[str]:
    """
    Find sentences that introduce chapter topics.
    
    Returns:
        List of meaningful introductory sentences
    """
    sentences = re.split(r'[.!?]+\s+', sample_text)
    meaningful_sentences = []
    
    introductory_markers = [
        'this chapter', 'we will', 'you will learn', 'introduces',
        'covers', 'discusses', 'explores', 'examines', 'provides',
        'focuses on', 'presents', 'demonstrates', 'explains'
    ]
    
    for sent in sentences[:max_sentences]:
        sent = sent.strip()
        if any(marker in sent.lower() for marker in introductory_markers):
            if 30 < len(sent) < 300:  # Reasonable length
                meaningful_sentences.append(sent)
    
    return meaningful_sentences


def _build_concept_summary(concepts: List[str]) -> str:
    """Build summary sentence from top concepts."""
    if not concepts:
        return ""
    
    top_concepts = [c for c in concepts[:3] if len(c) > 3]
    if not top_concepts:
        return ""
    
    concept_str = ', '.join(top_concepts[:2])
    if len(top_concepts) > 2:
        concept_str += f', and {top_concepts[2]}'
    
    return f"Key topics include {concept_str}."


def _categorize_keywords(keywords: List[str]) -> tuple[List[str], List[str]]:
    """
    Categorize keywords into implementation and conceptual.
    
    Returns:
        (implementation_keywords, conceptual_keywords)
    """
    impl_keywords = [k for k in keywords[:10] if k in [
        'class', 'function', 'method', 'decorator', 'generator',
        'iterator', 'lambda', 'comprehension'
    ]]
    concept_keywords = [k for k in keywords[:10] if k in [
        'exception', 'inheritance', 'testing', 'debugging',
        'pattern', 'architecture', 'design', 'api'
    ]]
    
    return impl_keywords, concept_keywords


def _build_keyword_summary(keywords: List[str], max_parts: int) -> str:
    """Build summary sentence from categorized keywords."""
    if not keywords:
        return ""
    
    impl_keywords, concept_keywords = _categorize_keywords(keywords)
    
    keyword_details = []
    if impl_keywords:
        keyword_details.append(', '.join(impl_keywords[:2]))
    if concept_keywords:
        keyword_details.append(', '.join(concept_keywords[:2]))
    
    if keyword_details and max_parts < 3:
        return f"Covers {', '.join(keyword_details)}."
    
    return ""


def _add_technical_context(summary: str, sentences: List[str], sample_text: str) -> str:
    """Add additional technical context if summary is too short."""
    if len(summary) >= 150 or not sample_text:
        return summary
    
    technical_terms = [
        'python', 'code', 'program', 'syntax', 'variable',
        'function', 'class', 'method', 'object', 'data'
    ]
    
    for sent in sentences[1:15]:
        sent = sent.strip()
        if any(tech_word in sent.lower() for tech_word in technical_terms):
            if 40 < len(sent) < 250 and sent not in summary:
                return f"{summary} {sent}."
    
    return summary


def generate_chapter_summary(chapter_pages: List[Dict[str, Any]], 
                            chapter_title: str,
                            keywords: List[str],
                            concepts: List[str]) -> str:
    """
    Generate a concise summary of what the chapter covers.
    
    Creates a 2-3 sentence summary based on:
    - Chapter title
    - Extracted keywords
    - Identified concepts
    - First few pages of content
    """
    # Extract sample text from first pages
    sample_text = _extract_sample_text(chapter_pages, num_pages=5)
    
    # Find introductory sentences
    meaningful_sentences = _find_introductory_sentences(sample_text, max_sentences=20)
    
    # Build summary parts
    summary_parts = []
    
    # Use meaningful sentence if found
    if meaningful_sentences:
        summary_parts.append(meaningful_sentences[0])
    else:
        summary_parts.append(f"This chapter covers {chapter_title.lower()}.")
    
    # Add concept summary
    concept_summary = _build_concept_summary(concepts)
    if concept_summary:
        summary_parts.append(concept_summary)
    
    # Add keyword-based summary if needed
    keyword_summary = _build_keyword_summary(keywords, len(summary_parts))
    if keyword_summary:
        summary_parts.append(keyword_summary)
    
    # Combine summary parts
    summary = ' '.join(summary_parts)
    
    # Add technical context if needed
    sentences = re.split(r'[.!?]+\s+', sample_text)
    summary = _add_technical_context(summary, sentences, sample_text)
    
    return summary[:600]  # Limit to 600 chars for reasonable length


def load_book_json(book_name: str) -> Dict[str, Any]:
    """
    Load a book's JSON file using PathConfig.
    
    Reference: Python Distilled Ch. 9 - Path operations, file I/O
    """
    # Use PathConfig for centralized path management
    json_dir = settings.paths.textbooks_json_dir
    
    # Build path: textbooks_json_dir / subdirectory / book_name
    subdirectory = BOOK_PATHS.get(book_name, "")
    if subdirectory:
        json_path = json_dir / subdirectory / book_name
    else:
        json_path = json_dir / book_name
    
    with open(json_path, 'r') as f:
        return json.load(f)


def process_chapter_metadata(_book_name: str, chapter: Dict[str, Any], 
                            book_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single chapter and extract metadata.
    
    Returns updated chapter dict with summary, keywords, and concepts.
    
    Args:
        _book_name: Book name (reserved for future use)
        chapter: Chapter dictionary with metadata
        book_data: Full book data with pages
    """
    chapter_num = chapter['chapter_number']
    start_page = chapter['start_page']
    end_page = chapter['end_page']
    title = chapter['title']
    
    print(f"  Processing Ch.{chapter_num}: {title} (pp.{start_page}-{end_page})")
    
    # Extract pages for this chapter
    chapter_pages = []
    for page in book_data.get('pages', []):
        page_num = page.get('page_number')
        if page_num and start_page <= page_num <= end_page:
            chapter_pages.append(page)
    
    if not chapter_pages:
        print("    ⚠️  No pages found for this chapter range")
        # Return chapter with empty metadata
        return {
            **chapter,
            'summary': f"Chapter {chapter_num}: {title}",
            'keywords': [],
            'concepts': []
        }
    
    # Combine all chapter text
    chapter_text = "\n".join([p.get('content', '') for p in chapter_pages])
    
    # Extract metadata
    keywords = extract_keywords_from_text(chapter_text)
    concepts = extract_concepts_from_text(chapter_text)
    summary = generate_chapter_summary(chapter_pages, title, keywords, concepts)
    
    print(f"    ✓ Keywords: {len(keywords)}, Concepts: {len(concepts)}")
    
    # Return updated chapter metadata
    return {
        **chapter,
        'summary': summary,
        'keywords': keywords,
        'concepts': concepts
    }


def main():
    """Main processing function."""
    print("="*80)
    print("GENERATING CHAPTER METADATA FOR ALL 15 BOOKS")
    print("="*80)
    
    # Load current metadata cache from configured metadata directory
    # Reference: Python Distilled Ch. 9 p. 228 - mkdir(parents=True, exist_ok=True)
    cache_path = settings.paths.metadata_dir / "chapter_metadata_cache.json"
    
    # Create metadata directory if it doesn't exist (12-Factor App - idempotent operations)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load cache if exists, otherwise start with empty dict
    if cache_path.exists():
        with open(cache_path, 'r') as f:
            cache = json.load(f)
    else:
        print(f"No existing cache found at {cache_path}, starting fresh")
        cache = {}
    
    print(f"\nLoaded cache with {len(cache)} books\n")
    
    # Process each book
    books_processed = 0
    chapters_processed = 0
    
    for book_name in BOOK_PATHS.keys():
        if book_name not in cache:
            print(f"⚠️  {book_name} not in cache, skipping...")
            continue
        
        print(f"\n{'='*80}")
        print(f"Processing: {book_name}")
        print(f"{'='*80}")
        
        try:
            # Load book JSON
            book_data = load_book_json(book_name)
            
            # Process each chapter
            updated_chapters = []
            for chapter in cache[book_name]:
                updated_chapter = process_chapter_metadata(book_name, chapter, book_data)
                updated_chapters.append(updated_chapter)
                chapters_processed += 1
            
            # Update cache
            cache[book_name] = updated_chapters
            books_processed += 1
            
            print(f"✓ Completed {book_name}: {len(updated_chapters)} chapters")
            
        except FileNotFoundError as e:
            print(f"❌ Error loading {book_name}: {e}")
            continue
        except Exception as e:
            print(f"❌ Error processing {book_name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Save updated cache
    print(f"\n{'='*80}")
    print("SAVING UPDATED METADATA")
    print(f"{'='*80}")
    
    with open(cache_path, 'w') as f:
        json.dump(cache, f, indent=2)
    
    print("\n✅ SUCCESS!")
    print(f"   Processed {books_processed} books")
    print(f"   Updated {chapters_processed} chapters")
    print(f"   Saved to: {cache_path}")
    print("\nAll chapters now have:")
    print("  - summary (2-3 sentence overview)")
    print("  - keywords (technical terms, max 15)")
    print("  - concepts (key topics discussed, max 10)")


if __name__ == "__main__":
    main()
