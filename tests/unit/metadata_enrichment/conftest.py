"""
Shared pytest fixtures for metadata_enrichment tests.

This module provides reusable fixtures for metadata enrichment testing.
All ML processing is delegated to ai-agents MSEP service per Kitchen Brigade architecture.

Reference: MULTI_STAGE_ENRICHMENT_PIPELINE_ARCHITECTURE.md
"""

import sys
from pathlib import Path
from typing import Any

# Add project root to Python path for imports (before other imports)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pytest


# =============================================================================
# Sample Data Fixtures
# =============================================================================

@pytest.fixture
def sample_chapters() -> list[dict[str, Any]]:
    """
    Sample chapter data for testing enrichment operations.
    
    Returns 5 chapters with varying semantic content for testing.
    """
    return [
        {
            "chapter_id": "ch1",
            "title": "Introduction to Machine Learning",
            "description": "Basics of ML algorithms and neural networks",
            "content": "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
        },
        {
            "chapter_id": "ch2", 
            "title": "Deep Learning Fundamentals",
            "description": "Neural network architectures and training",
            "content": "Deep learning uses multi-layer neural networks to model complex patterns in data."
        },
        {
            "chapter_id": "ch3",
            "title": "Natural Language Processing",
            "description": "Text analysis and language models",
            "content": "NLP combines linguistics and machine learning to process human language."
        },
        {
            "chapter_id": "ch4",
            "title": "Computer Vision Basics",
            "description": "Image recognition and processing",
            "content": "Computer vision enables machines to interpret visual information from images and video."
        },
        {
            "chapter_id": "ch5",
            "title": "Reinforcement Learning",
            "description": "Learning through trial and error",
            "content": "Reinforcement learning trains agents to make decisions by rewarding desired behaviors."
        },
    ]


@pytest.fixture
def sample_texts() -> list[str]:
    """Simple text samples for testing."""
    return [
        "Machine learning enables computers to learn from data.",
        "Deep neural networks process information in layers.",
        "Natural language processing understands human text.",
    ]


@pytest.fixture
def sample_book_metadata() -> dict[str, Any]:
    """Sample book metadata for testing enrichment workflows."""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "chapters": [
            {
                "chapter_number": 1,
                "title": "Introduction",
                "summary": "An introduction to the topic.",
                "keywords": ["intro", "basics"],
                "concepts": ["fundamentals"],
            },
            {
                "chapter_number": 2,
                "title": "Core Concepts",
                "summary": "Core concepts and patterns.",
                "keywords": ["patterns", "design"],
                "concepts": ["architecture"],
            },
        ],
    }
