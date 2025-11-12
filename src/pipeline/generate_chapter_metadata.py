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
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set, Any
from collections import Counter

# Book locations
BOOK_PATHS = {
    "Fluent Python 2nd.json": "Engineering Practices/JSON",
    "Python Distilled.json": "Engineering Practices/JSON",
    "Python Essential Reference 4th.json": "Engineering Practices/JSON",
    "Python Cookbook 3rd.json": "Engineering Practices/JSON",
    "Learning Python Ed6.json": "Engineering Practices/JSON",
    "Python Data Analysis 3rd.json": "Engineering Practices/JSON",
    "Architecture Patterns with Python.json": "Architecture/JSON",
    "Python Architecture Patterns.json": "Architecture/JSON",
    "Building Microservices.json": "Architecture/JSON",
    "Microservice Architecture.json": "Architecture/JSON",
    "Microservices Up and Running.json": "Architecture/JSON",
    "Building Python Microservices with FastAPI.json": "Architecture/JSON",
    "Microservice APIs Using Python Flask FastAPI.json": "Architecture/JSON",
    "Python Microservices Development.json": "Architecture/JSON"
}

def extract_keywords_from_text(text: str, max_keywords: int = 15) -> List[str]:
    """
    Extract meaningful keywords from chapter text.
    
    Identifies technical terms, Python concepts, and key topics.
    """
    # Convert to lowercase for analysis
    text_lower = text.lower()
    
    # Expanded Python/programming keywords to look for
    python_keywords = [
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
    
    # Find which keywords appear in the text
    found_keywords = []
    for keyword in python_keywords:
        # Count occurrences (lower threshold to 1 for broader coverage)
        count = text_lower.count(keyword)
        if count >= 1:
            found_keywords.append((keyword, count))
    
    # Sort by frequency
    found_keywords.sort(key=lambda x: x[1], reverse=True)
    
    # Extract capitalized terms (likely important concepts like class names, etc.)
    cap_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
    capitalized = re.findall(cap_pattern, text)
    cap_counter = Counter(capitalized)
    
    # Add frequent capitalized terms (lower threshold)
    for term, count in cap_counter.most_common(15):
        if count >= 2 and len(term) > 3 and term.lower() not in [k[0] for k in found_keywords]:
            found_keywords.append((term.lower(), count))
    
    # If still very few keywords, extract from word frequency
    if len(found_keywords) < 5:
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about',
                     'into', 'through', 'during', 'before', 'after', 'above',
                     'below', 'between', 'under', 'again', 'further', 'then',
                     'once', 'here', 'there', 'when', 'where', 'why', 'how',
                     'all', 'both', 'each', 'few', 'more', 'most', 'other',
                     'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                     'so', 'than', 'too', 'very', 'can', 'will', 'just', 'should'}
        
        words = re.findall(r'\b[a-z]{4,}\b', text_lower)
        word_counter = Counter(w for w in words if w not in stop_words)
        
        for word, count in word_counter.most_common(20):
            if count >= 3 and word not in [k[0] for k in found_keywords]:
                found_keywords.append((word, count))
    
    # Return top keywords
    return [kw[0] for kw in found_keywords[:max_keywords]]


def extract_concepts_from_text(text: str, max_concepts: int = 10) -> List[str]:
    """
    Extract key concepts discussed in the chapter.
    
    Focuses on multi-word technical phrases and important topics.
    """
    text_lower = text.lower()
    
    # Extended list of multi-word concepts to search for
    concept_patterns = [
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
    
    # Find all concept matches
    concept_counts = []
    for pattern in concept_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            # Get the matched text (first capture group)
            concept = matches[0] if isinstance(matches[0], str) else matches[0][0]
            count = len(matches)
            # Lower threshold - include if mentioned even once
            if count >= 1:
                concept_counts.append((concept.strip(), count))
    
    # If we found very few concepts, extract noun phrases as fallback
    if len(concept_counts) < 3:
        # Extract important-looking noun phrases
        # Pattern: Capitalized Word + optional lowercase words
        noun_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[a-z]+){0,2})\b', text)
        phrase_counter = Counter(noun_phrases)
        
        for phrase, count in phrase_counter.most_common(15):
            if count >= 2 and len(phrase) > 3:
                # Don't add if it's already in concepts
                if not any(phrase.lower() in c[0].lower() for c in concept_counts):
                    concept_counts.append((phrase.lower(), count))
    
    # Sort by frequency
    concept_counts.sort(key=lambda x: x[1], reverse=True)
    
    # Remove duplicates and return top concepts
    seen = set()
    unique_concepts = []
    for concept, count in concept_counts:
        concept_clean = concept.strip().lower()
        if concept_clean not in seen:
            seen.add(concept_clean)
            unique_concepts.append(concept)
    
    return unique_concepts[:max_concepts]


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
    # Get sample text from first 5 pages for better analysis
    sample_text = ""
    for page in chapter_pages[:5]:
        sample_text += page.get('content', '') + " "
    
    # Extract meaningful sentences from the actual content
    sentences = re.split(r'[.!?]+\s+', sample_text)
    meaningful_sentences = []
    
    for sent in sentences[:20]:  # Check first 20 sentences
        sent = sent.strip()
        # Look for sentences that introduce topics (common patterns)
        if any(marker in sent.lower() for marker in [
            'this chapter', 'we will', 'you will learn', 'introduces',
            'covers', 'discusses', 'explores', 'examines', 'provides',
            'focuses on', 'presents', 'demonstrates', 'explains'
        ]):
            if 30 < len(sent) < 300:  # Reasonable length
                meaningful_sentences.append(sent)
    
    # Build summary
    summary_parts = []
    
    # Use meaningful sentence if found
    if meaningful_sentences:
        summary_parts.append(meaningful_sentences[0])
    else:
        # Fallback: describe based on title
        summary_parts.append(f"This chapter covers {chapter_title.lower()}.")
    
    # Add concepts if we found good ones
    if concepts:
        # Take top 3 most relevant concepts
        top_concepts = [c for c in concepts[:3] if len(c) > 3]
        if top_concepts:
            concept_str = ', '.join(top_concepts[:2])
            if len(top_concepts) > 2:
                concept_str += f', and {top_concepts[2]}'
            summary_parts.append(f"Key topics include {concept_str}.")
    
    # Add technical details from keywords
    if keywords:
        # Identify implementation vs conceptual keywords
        impl_keywords = [k for k in keywords[:10] if k in [
            'class', 'function', 'method', 'decorator', 'generator',
            'iterator', 'lambda', 'comprehension'
        ]]
        concept_keywords = [k for k in keywords[:10] if k in [
            'exception', 'inheritance', 'testing', 'debugging',
            'pattern', 'architecture', 'design', 'api'
        ]]
        
        keyword_details = []
        if impl_keywords:
            keyword_details.append(', '.join(impl_keywords[:2]))
        if concept_keywords:
            keyword_details.append(', '.join(concept_keywords[:2]))
        
        if keyword_details and len(summary_parts) < 3:
            summary_parts.append(f"Covers {', '.join(keyword_details)}.")
    
    # Combine summary parts
    summary = ' '.join(summary_parts)
    
    # If summary is still too short or generic, add more context from actual text
    if len(summary) < 150 and sample_text:
        # Find sentences with technical content
        for sent in sentences[1:15]:
            sent = sent.strip()
            # Look for sentences with code-related words
            if any(tech_word in sent.lower() for tech_word in [
                'python', 'code', 'program', 'syntax', 'variable',
                'function', 'class', 'method', 'object', 'data'
            ]):
                if 40 < len(sent) < 250 and sent not in summary:
                    summary += f" {sent}."
                    break
    
    return summary[:600]  # Limit to 600 chars for reasonable length


def load_book_json(book_name: str) -> Dict[str, Any]:
    """Load a book's JSON file."""
    base_path = Path("/Users/kevintoles/POC/tpm-job-finder-poc/Python_References")
    json_path = base_path / BOOK_PATHS[book_name] / book_name
    
    with open(json_path, 'r') as f:
        return json.load(f)


def process_chapter_metadata(book_name: str, chapter: Dict[str, Any], 
                            book_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single chapter and extract metadata.
    
    Returns updated chapter dict with summary, keywords, and concepts.
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
        print(f"    ⚠️  No pages found for this chapter range")
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
    
    # Load current metadata cache
    cache_path = Path(__file__).parent / "chapter_metadata_cache.json"
    with open(cache_path, 'r') as f:
        cache = json.load(f)
    
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
    
    print(f"\n✅ SUCCESS!")
    print(f"   Processed {books_processed} books")
    print(f"   Updated {chapters_processed} chapters")
    print(f"   Saved to: {cache_path}")
    print(f"\nAll chapters now have:")
    print(f"  - summary (2-3 sentence overview)")
    print(f"  - keywords (technical terms, max 15)")
    print(f"  - concepts (key topics discussed, max 10)")


if __name__ == "__main__":
    main()
