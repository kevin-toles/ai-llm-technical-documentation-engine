#!/usr/bin/env python3
"""
Merge Fluent Python metadata into chapter_metadata_cache.json
"""

import json
from pathlib import Path

# Paths
METADATA_PATH = Path(__file__).parent / "fluent_python_metadata.json"
CACHE_PATH = Path("/Users/kevintoles/POC/tpm-job-finder-poc/Python_References/Document Generation_Validation Scripts/chapter_metadata_cache.json")

def main():
    print("="*80)
    print("MERGING FLUENT PYTHON METADATA INTO CACHE")
    print("="*80)
    
    # Load Fluent Python metadata
    print(f"\nLoading: {METADATA_PATH}")
    with open(METADATA_PATH, 'r') as f:
        fluent_metadata = json.load(f)
    
    chapters = fluent_metadata.get('chapters', [])
    print(f"✓ Found {len(chapters)} chapters")
    
    # Load existing cache
    print(f"\nLoading: {CACHE_PATH}")
    with open(CACHE_PATH, 'r') as f:
        cache = json.load(f)
    
    print(f"✓ Current cache has {len(cache)} books")
    
    # Add Fluent Python to cache
    book_key = "Fluent Python 2nd.json"
    cache[book_key] = chapters
    
    print(f"\n✓ Added '{book_key}' with {len(chapters)} chapters")
    
    # Save updated cache
    print(f"\nSaving updated cache to: {CACHE_PATH}")
    with open(CACHE_PATH, 'w') as f:
        json.dump(cache, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"✅ SUCCESS!")
    print(f"   Cache now contains {len(cache)} books")
    print(f"   Fluent Python 2nd: {len(chapters)} chapters")
    print(f"{'='*80}")
    
    # Show sample chapter
    if chapters:
        print("\nSample chapter entry:")
        print(json.dumps(chapters[0], indent=2))


if __name__ == "__main__":
    main()
