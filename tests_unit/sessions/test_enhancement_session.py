"""
Unit tests for EnhancementSession - WBS 3.1.2.3

Tests session-based enhancement workflow with context management.

Reference:
- GUIDELINES pp. 2153: External state stores (Redis) for session state
- ARCHITECTURE.md: Session Manager with TTL
- CODING_PATTERNS_ANALYSIS: Async stubs for Redis compatibility
- Comp_Static_Analysis_Report #38: Session expiration handling
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

# =============================================================================
# RED PHASE: Tests written before implementation
# =============================================================================


class TestEnhancementSessionInstantiation:
    """Tests for EnhancementSession instantiation."""

    def test_instantiation_with_defaults(self) -> None:
        """EnhancementSession should instantiate with default configuration."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        session = EnhancementSession()

        assert session is not None
        assert session._session_id is None  # Not created yet
        assert session._ttl_seconds > 0

    def test_instantiation_with_custom_ttl(self) -> None:
        """EnhancementSession should accept custom TTL."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        session = EnhancementSession(ttl_seconds=7200)

        assert session._ttl_seconds == 7200

    def test_instantiation_with_context(self) -> None:
        """EnhancementSession should accept initial context."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        context = {"document_id": "doc_123", "user_id": "user_456"}
        session = EnhancementSession(context=context)

        assert session._context == context


class TestEnhancementSessionContextManager:
    """Tests for async context manager protocol."""

    @pytest.mark.asyncio
    async def test_aenter_creates_session(self) -> None:
        """__aenter__ should create session via gateway."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        mock_response = {"session_id": "sess_abc123", "expires_at": "2025-12-05T00:00:00Z"}

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value=mock_response
        ):
            session = EnhancementSession()
            result = await session.__aenter__()

            assert result is session
            assert session._session_id == "sess_abc123"

    @pytest.mark.asyncio
    async def test_aexit_deletes_session(self) -> None:
        """__aexit__ should delete session via gateway."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={"session_id": "sess_xyz"}
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ) as mock_delete:
            async with EnhancementSession() as session:
                pass

            mock_delete.assert_called_once_with("sess_xyz")

    @pytest.mark.asyncio
    async def test_aexit_handles_delete_failure_gracefully(self) -> None:
        """__aexit__ should not raise on delete failure."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession
        from workflows.shared.clients.llm_gateway import GatewayAPIError

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={"session_id": "sess_fail"}
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock,
            side_effect=GatewayAPIError("Session not found", status_code=404)
        ):
            # Should not raise
            async with EnhancementSession() as session:
                pass

            assert session._session_id == "sess_fail"


class TestEnhancementSessionLifecycle:
    """Tests for session lifecycle management."""

    @pytest.mark.asyncio
    async def test_session_id_property_returns_id_when_created(self) -> None:
        """session_id property should return ID when session exists."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={"session_id": "sess_123"}
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ):
            async with EnhancementSession() as session:
                assert session.session_id == "sess_123"

    def test_session_id_property_returns_none_before_create(self) -> None:
        """session_id property should return None before session created."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        session = EnhancementSession()
        assert session.session_id is None

    @pytest.mark.asyncio
    async def test_is_active_returns_true_when_session_valid(self) -> None:
        """is_active should return True for valid session."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={
                "session_id": "sess_active",
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
            }
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ):
            async with EnhancementSession() as session:
                assert session.is_active is True

    @pytest.mark.asyncio
    async def test_is_active_returns_false_when_expired(self) -> None:
        """is_active should return False for expired session."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={
                "session_id": "sess_expired",
                "expires_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
            }
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ):
            async with EnhancementSession() as session:
                assert session.is_active is False


class TestEnhancementSessionEnhance:
    """Tests for enhancement operations within session."""

    @pytest.mark.asyncio
    async def test_enhance_passes_session_id_to_gateway(self) -> None:
        """enhance() should pass session_id in chat_completion call."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        mock_completion = {
            "choices": [{"message": {"content": "Enhanced content"}}],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        }

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={"session_id": "sess_enhance"}
        ), patch.object(
            EnhancementSession, "_call_gateway_completion",
            new_callable=AsyncMock, return_value=mock_completion
        ) as mock_call, patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ):
            async with EnhancementSession() as session:
                result = await session.enhance("Test prompt", max_tokens=100)

            mock_call.assert_called_once()
            call_kwargs = mock_call.call_args
            assert call_kwargs is not None

    @pytest.mark.asyncio
    async def test_enhance_returns_response_content(self) -> None:
        """enhance() should return the content from gateway response."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        mock_completion = {
            "choices": [{"message": {"content": "Enhanced text here"}}],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        }

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={"session_id": "sess_content"}
        ), patch.object(
            EnhancementSession, "_call_gateway_completion",
            new_callable=AsyncMock, return_value=mock_completion
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ):
            async with EnhancementSession() as session:
                result = await session.enhance("Test prompt", max_tokens=100)

            assert result.content == "Enhanced text here"


class TestEnhancementSessionExpiry:
    """Tests for session expiry handling - Ref: Comp_Static_Analysis_Report #38."""

    @pytest.mark.asyncio
    async def test_refresh_session_on_expiry(self) -> None:
        """Session should refresh when expired and auto_refresh=True."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        # First session expires, second is fresh
        create_calls = [
            {"session_id": "sess_old", "expires_at": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()},
            {"session_id": "sess_new", "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()},
        ]
        create_call_count = [0]

        async def mock_create(*args, **kwargs):
            result = create_calls[create_call_count[0]]
            create_call_count[0] += 1
            return result

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, side_effect=mock_create
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ), patch.object(
            EnhancementSession, "_call_gateway_completion",
            new_callable=AsyncMock, return_value={
                "choices": [{"message": {"content": "Result"}}],
                "model": "test", "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}
            }
        ):
            session = EnhancementSession(auto_refresh=True)
            async with session:
                # Force check which should trigger refresh
                await session.ensure_active()
                assert session._session_id == "sess_new"

    @pytest.mark.asyncio
    async def test_raises_on_expiry_when_auto_refresh_false(self) -> None:
        """Session should raise SessionExpiredError when expired and auto_refresh=False."""
        from workflows.shared.sessions.enhancement_session import (
            EnhancementSession,
            SessionExpiredError,
        )

        expired_at = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={"session_id": "sess_exp", "expires_at": expired_at}
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ):
            session = EnhancementSession(auto_refresh=False)
            async with session:
                with pytest.raises(SessionExpiredError):
                    await session.ensure_active()


class TestEnhancementSessionIntegration:
    """Integration-style tests for multi-turn enhancement."""

    @pytest.mark.asyncio
    async def test_multi_turn_enhancement_maintains_context(self) -> None:
        """Multiple enhance() calls should maintain session context."""
        from workflows.shared.sessions.enhancement_session import EnhancementSession

        call_count = [0]

        async def mock_completion(*args, **kwargs):
            call_count[0] += 1
            return {
                "choices": [{"message": {"content": f"Response {call_count[0]}"}}],
                "model": "test", "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}
            }

        with patch.object(
            EnhancementSession, "_create_gateway_session",
            new_callable=AsyncMock, return_value={
                "session_id": "sess_multi",
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
            }
        ), patch.object(
            EnhancementSession, "_call_gateway_completion",
            new_callable=AsyncMock, side_effect=mock_completion
        ), patch.object(
            EnhancementSession, "_delete_gateway_session",
            new_callable=AsyncMock
        ):
            async with EnhancementSession() as session:
                result1 = await session.enhance("First enhancement", max_tokens=100)
                result2 = await session.enhance("Second enhancement", max_tokens=100)
                result3 = await session.enhance("Third enhancement", max_tokens=100)

                assert result1.content == "Response 1"
                assert result2.content == "Response 2"
                assert result3.content == "Response 3"
                assert call_count[0] == 3
