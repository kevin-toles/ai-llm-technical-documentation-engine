"""
Tools Module - WBS 3.1.2.2 Tool-Use Integration

Exports tool definitions and handlers for LLM enhancement workflow.

Usage:
    from workflows.shared.tools import get_all_enhancement_tools, execute_tool

    # Get tool definitions for chat completion
    tools = get_all_enhancement_tools()

    # Execute a tool call
    result = execute_tool("search_corpus", {"query": "decorators"})
"""

from workflows.shared.tools.definitions import (
    get_search_corpus_tool,
    get_get_chapter_tool,
    get_get_related_chapters_tool,
    get_list_books_tool,
    get_all_enhancement_tools,
    TOOL_NAMES,
)

from workflows.shared.tools.handlers import (
    search_corpus,
    get_chapter,
    get_related_chapters,
    list_books,
    execute_tool,
    TOOL_HANDLERS,
)

__all__ = [
    # Tool definitions
    "get_search_corpus_tool",
    "get_get_chapter_tool",
    "get_get_related_chapters_tool",
    "get_list_books_tool",
    "get_all_enhancement_tools",
    "TOOL_NAMES",
    # Tool handlers
    "search_corpus",
    "get_chapter",
    "get_related_chapters",
    "list_books",
    "execute_tool",
    "TOOL_HANDLERS",
]
