"""
Unit tests for Tool Definitions and Handlers - WBS 3.1.2.2

Tests tool schema formats and handler execution.
"""

import pytest
from unittest.mock import MagicMock, patch

from workflows.shared.tools.definitions import (
    get_search_corpus_tool,
    get_get_chapter_tool,
    get_get_related_chapters_tool,
    get_list_books_tool,
    get_all_enhancement_tools,
    TOOL_NAMES,
)


class TestToolDefinitions:
    """Tests for tool definition schemas."""

    def test_search_corpus_tool_has_required_fields(self) -> None:
        """search_corpus tool should have type, function, parameters."""
        tool = get_search_corpus_tool()

        assert tool["type"] == "function"
        assert "function" in tool
        assert tool["function"]["name"] == "search_corpus"
        assert "parameters" in tool["function"]
        assert "query" in tool["function"]["parameters"]["properties"]

    def test_search_corpus_tool_query_required(self) -> None:
        """search_corpus tool should require query parameter."""
        tool = get_search_corpus_tool()

        assert "required" in tool["function"]["parameters"]
        assert "query" in tool["function"]["parameters"]["required"]

    def test_get_chapter_tool_has_required_fields(self) -> None:
        """get_chapter tool should have book and chapter_number params."""
        tool = get_get_chapter_tool()

        assert tool["type"] == "function"
        assert tool["function"]["name"] == "get_chapter"
        params = tool["function"]["parameters"]["properties"]
        assert "book" in params
        assert "chapter_number" in params

    def test_get_chapter_tool_both_params_required(self) -> None:
        """get_chapter tool should require both parameters."""
        tool = get_get_chapter_tool()

        required = tool["function"]["parameters"]["required"]
        assert "book" in required
        assert "chapter_number" in required

    def test_get_related_chapters_tool_has_required_fields(self) -> None:
        """get_related_chapters tool should have source chapter params."""
        tool = get_get_related_chapters_tool()

        assert tool["type"] == "function"
        assert tool["function"]["name"] == "get_related_chapters"
        params = tool["function"]["parameters"]["properties"]
        assert "book" in params
        assert "chapter_number" in params
        assert "top_k" in params
        assert "exclude_same_book" in params

    def test_list_books_tool_has_no_required_params(self) -> None:
        """list_books tool should have no required parameters."""
        tool = get_list_books_tool()

        assert tool["type"] == "function"
        assert tool["function"]["name"] == "list_books"
        assert tool["function"]["parameters"]["required"] == []

    def test_get_all_enhancement_tools_returns_all_tools(self) -> None:
        """get_all_enhancement_tools should return all 4 tools."""
        tools = get_all_enhancement_tools()

        assert len(tools) == 4
        tool_names = [t["function"]["name"] for t in tools]
        assert "search_corpus" in tool_names
        assert "get_chapter" in tool_names
        assert "get_related_chapters" in tool_names
        assert "list_books" in tool_names

    def test_tool_names_constant_matches_definitions(self) -> None:
        """TOOL_NAMES should match defined tool names."""
        tools = get_all_enhancement_tools()
        defined_names = {t["function"]["name"] for t in tools}

        for name in TOOL_NAMES.values():
            assert name in defined_names


class TestToolHandlers:
    """Tests for tool handler functions."""

    def test_execute_tool_unknown_tool_raises(self) -> None:
        """execute_tool should raise ValueError for unknown tools."""
        from workflows.shared.tools.handlers import execute_tool

        with pytest.raises(ValueError, match="Unknown tool"):
            execute_tool("unknown_tool", {})

    @patch("workflows.shared.tools.handlers._get_chapter_manager")
    @patch("workflows.shared.tools.handlers._get_corpus_dir")
    def test_list_books_returns_books_list(
        self, mock_corpus_dir: MagicMock, mock_manager: MagicMock
    ) -> None:
        """list_books should return list of books."""
        from workflows.shared.tools.handlers import list_books
        from pathlib import Path
        import tempfile

        # Create temp directory with mock files
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "Book_One_Content.json").touch()
            (tmppath / "Book_Two_Content.json").touch()

            mock_corpus_dir.return_value = tmppath

            # Mock manager
            mock_mgr = MagicMock()
            mock_mgr.get_chapters.return_value = [MagicMock(), MagicMock()]
            mock_manager.return_value = mock_mgr

            result = list_books()

        assert "books" in result
        assert "total" in result
        assert result["total"] == 2

    @patch("workflows.shared.tools.handlers._get_chapter_manager")
    def test_get_chapter_returns_chapter_info(
        self, mock_manager: MagicMock
    ) -> None:
        """get_chapter should return chapter metadata."""
        from workflows.shared.tools.handlers import get_chapter

        # Mock chapter info
        mock_chapter = MagicMock()
        mock_chapter.chapter_number = 1
        mock_chapter.title = "Introduction"
        mock_chapter.start_page = 1
        mock_chapter.end_page = 20
        mock_chapter.page_count = 20
        mock_chapter.keywords = ["intro", "basics"]
        mock_chapter.summary = "Chapter summary"
        mock_chapter.concepts = ["concept1"]

        mock_mgr = MagicMock()
        mock_mgr.get_chapter_by_number.return_value = mock_chapter
        mock_manager.return_value = mock_mgr

        result = get_chapter("test_book.json", 1)

        assert result["chapter_number"] == 1
        assert result["title"] == "Introduction"
        assert "keywords" in result

    @patch("workflows.shared.tools.handlers._get_chapter_manager")
    def test_get_chapter_not_found_returns_error(
        self, mock_manager: MagicMock
    ) -> None:
        """get_chapter should return error if chapter not found."""
        from workflows.shared.tools.handlers import get_chapter

        mock_mgr = MagicMock()
        mock_mgr.get_chapter_by_number.return_value = None
        mock_manager.return_value = mock_mgr

        result = get_chapter("test_book.json", 999)

        assert "error" in result
        assert "not found" in result["error"]

    def test_execute_tool_dispatches_to_correct_handler(self) -> None:
        """execute_tool should call the correct handler function."""
        from workflows.shared.tools import handlers

        # Patch the handler in the module and update the registry
        original_handler = handlers.TOOL_HANDLERS["list_books"]
        mock_handler = MagicMock(return_value={"books": [], "total": 0})
        handlers.TOOL_HANDLERS["list_books"] = mock_handler

        try:
            result = handlers.execute_tool("list_books", {})
            mock_handler.assert_called_once_with()
            assert result == {"books": [], "total": 0}
        finally:
            # Restore original handler
            handlers.TOOL_HANDLERS["list_books"] = original_handler


class TestToolSchemaValidation:
    """Tests for JSON Schema compliance."""

    def test_all_tools_have_description(self) -> None:
        """All tools should have descriptions."""
        tools = get_all_enhancement_tools()

        for tool in tools:
            assert "description" in tool["function"]
            assert len(tool["function"]["description"]) > 10

    def test_all_parameter_properties_have_types(self) -> None:
        """All parameter properties should have type field."""
        tools = get_all_enhancement_tools()

        for tool in tools:
            props = tool["function"]["parameters"].get("properties", {})
            for name, schema in props.items():
                assert "type" in schema, f"Property {name} missing type"

    def test_all_parameter_properties_have_descriptions(self) -> None:
        """All parameter properties should have descriptions."""
        tools = get_all_enhancement_tools()

        for tool in tools:
            props = tool["function"]["parameters"].get("properties", {})
            for name, schema in props.items():
                assert "description" in schema, f"Property {name} missing description"

    def test_parameters_schema_is_object_type(self) -> None:
        """All parameters schemas should be type: object."""
        tools = get_all_enhancement_tools()

        for tool in tools:
            assert tool["function"]["parameters"]["type"] == "object"
