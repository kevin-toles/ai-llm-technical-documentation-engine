"""
Tool Definitions for LLM Enhancement - WBS 3.1.2.2 Tool-Use Integration

Defines tool schemas for document enhancement workflow.
These tools allow the LLM to interact with the document corpus.

Reference Documents:
- llm-gateway/src/models/domain.py: ToolDefinition, ToolCall models
- GUIDELINES pp. 1510-1569: Tool inventory patterns
- workflows/metadata_enrichment/scripts/chapter_metadata_manager.py
- workflows/metadata_enrichment/scripts/semantic_similarity_engine.py

Pattern: Tool inventory (GUIDELINES pp. 1518)
Pattern: JSON Schema for parameters (OpenAI/Anthropic compatible)
"""

from typing import Any

# =============================================================================
# Tool Schemas (OpenAI/Anthropic compatible format)
# =============================================================================


def get_search_corpus_tool() -> dict[str, Any]:
    """
    Get the search_corpus tool definition.

    This tool allows the LLM to search across all books in the corpus
    for chapters related to a query.

    Returns:
        Tool definition dict in OpenAI/Anthropic format.
    """
    return {
        "type": "function",
        "function": {
            "name": "search_corpus",
            "description": (
                "Search the document corpus for chapters related to a query. "
                "Returns a list of relevant chapters with their metadata."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (e.g., 'decorator patterns', 'error handling')",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5)",
                        "default": 5,
                    },
                    "min_similarity": {
                        "type": "number",
                        "description": "Minimum similarity score (0.0-1.0) to include results (default: 0.3)",
                        "default": 0.3,
                    },
                },
                "required": ["query"],
            },
        },
    }


def get_get_chapter_tool() -> dict[str, Any]:
    """
    Get the get_chapter tool definition.

    This tool retrieves detailed information about a specific chapter.

    Returns:
        Tool definition dict in OpenAI/Anthropic format.
    """
    return {
        "type": "function",
        "function": {
            "name": "get_chapter",
            "description": (
                "Get detailed metadata and content summary for a specific chapter. "
                "Use this to get more context about a chapter found in search results."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book": {
                        "type": "string",
                        "description": "The book filename (e.g., 'Fluent_Python_2nd_Content.json')",
                    },
                    "chapter_number": {
                        "type": "integer",
                        "description": "The chapter number to retrieve",
                    },
                },
                "required": ["book", "chapter_number"],
            },
        },
    }


def get_get_related_chapters_tool() -> dict[str, Any]:
    """
    Get the get_related_chapters tool definition.

    This tool finds chapters semantically similar to a given chapter.

    Returns:
        Tool definition dict in OpenAI/Anthropic format.
    """
    return {
        "type": "function",
        "function": {
            "name": "get_related_chapters",
            "description": (
                "Find chapters that are semantically related to a given chapter. "
                "Uses embedding-based similarity to find conceptually similar content."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book": {
                        "type": "string",
                        "description": "The book filename of the source chapter",
                    },
                    "chapter_number": {
                        "type": "integer",
                        "description": "The source chapter number",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Maximum number of related chapters to return (default: 5)",
                        "default": 5,
                    },
                    "exclude_same_book": {
                        "type": "boolean",
                        "description": "Whether to exclude chapters from the same book (default: false)",
                        "default": False,
                    },
                },
                "required": ["book", "chapter_number"],
            },
        },
    }


def get_list_books_tool() -> dict[str, Any]:
    """
    Get the list_books tool definition.

    This tool lists all books available in the corpus.

    Returns:
        Tool definition dict in OpenAI/Anthropic format.
    """
    return {
        "type": "function",
        "function": {
            "name": "list_books",
            "description": (
                "List all books available in the document corpus. "
                "Returns book titles and their chapter counts."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }


def get_all_enhancement_tools() -> list[dict[str, Any]]:
    """
    Get all tool definitions for the enhancement workflow.

    Returns:
        List of all tool definitions in OpenAI/Anthropic format.
    """
    return [
        get_search_corpus_tool(),
        get_get_chapter_tool(),
        get_get_related_chapters_tool(),
        get_list_books_tool(),
    ]


# =============================================================================
# Tool Names Enum (for tool_choice parameter)
# =============================================================================

TOOL_NAMES = {
    "search_corpus": "search_corpus",
    "get_chapter": "get_chapter",
    "get_related_chapters": "get_related_chapters",
    "list_books": "list_books",
}
