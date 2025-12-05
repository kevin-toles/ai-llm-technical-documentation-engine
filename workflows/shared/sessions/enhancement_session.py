"""
Enhancement Session - WBS 3.1.2.3 Session-Based Enhancement

Context manager for session-based LLM enhancement workflow.
Maintains conversation context across multiple enhancement turns.

Reference Documents:
- GUIDELINES pp. 2153: External state stores (Redis) for session state
- ARCHITECTURE.md: Session Manager with TTL
- CODING_PATTERNS_ANALYSIS: Async stubs for Redis compatibility
- Comp_Static_Analysis_Report #38: Session expiration handling

Pattern: Context Manager for resource lifecycle (session create/delete)
Pattern: Facade over LLMGatewayClient session methods
"""

import os
from datetime import datetime, timezone
from typing import Any, Optional

from workflows.shared.clients.llm_gateway import (
    LLMGatewayClient,
    GatewayError,
)
from workflows.shared.providers.base import LLMResponse


# =============================================================================
# Custom Exceptions
# =============================================================================


class SessionError(Exception):
    """Base exception for session errors."""

    pass


class SessionExpiredError(SessionError):
    """
    Raised when session has expired.

    Reference: Comp_Static_Analysis_Report #38 - Session expiration handling
    """

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        super().__init__(f"Session {session_id} has expired")


class SessionNotCreatedError(SessionError):
    """Raised when attempting to use session before creation."""

    pass


# =============================================================================
# EnhancementSession Class
# =============================================================================


class EnhancementSession:
    """
    Async context manager for session-based enhancement workflow.

    Creates a session at start of document processing, maintains context
    across multiple enhancement turns, and cleans up on exit.

    Reference:
    - GUIDELINES pp. 2153: Session state management
    - ARCHITECTURE.md: Session Manager API
    - WBS 3.1.2.3: Session-Based Enhancement

    Example:
        async with EnhancementSession(ttl_seconds=3600) as session:
            result1 = await session.enhance("First prompt", max_tokens=500)
            result2 = await session.enhance("Second prompt", max_tokens=500)
            # Context maintained between calls

    Attributes:
        session_id: The session ID from the gateway (None before creation).
        is_active: Whether the session is active and not expired.
    """

    # Default TTL: 1 hour
    DEFAULT_TTL_SECONDS = 3600

    # Default model
    DEFAULT_MODEL = "claude-sonnet-4-5-20250929"

    def __init__(
        self,
        ttl_seconds: Optional[int] = None,
        context: Optional[dict[str, Any]] = None,
        gateway_url: Optional[str] = None,
        model: Optional[str] = None,
        auto_refresh: bool = True,
    ) -> None:
        """
        Initialize EnhancementSession.

        Args:
            ttl_seconds: Session TTL in seconds. Default 3600 (1 hour).
            context: Initial context data (document_id, user_id, etc.).
            gateway_url: LLM Gateway URL. Defaults to env LLM_GATEWAY_URL.
            model: Model to use for enhancements. Defaults to claude-sonnet-4-5-20250929.
            auto_refresh: Whether to auto-refresh expired sessions. Default True.
        """
        self._ttl_seconds = ttl_seconds or int(
            os.getenv("LLM_SESSION_TTL", str(self.DEFAULT_TTL_SECONDS))
        )
        self._context = context or {}
        self._gateway_url = gateway_url or os.getenv("LLM_GATEWAY_URL") or "http://localhost:8080"
        self._model = model or os.getenv("LLM_MODEL") or self.DEFAULT_MODEL
        self._auto_refresh = auto_refresh

        # Session state
        self._session_id: Optional[str] = None
        self._expires_at: Optional[datetime] = None
        self._client: Optional[LLMGatewayClient] = None

    @property
    def session_id(self) -> Optional[str]:
        """Get the current session ID (None if not created)."""
        return self._session_id

    @property
    def is_active(self) -> bool:
        """
        Check if session is active and not expired.

        Reference: Comp_Static_Analysis_Report #38 - Expiration check
        """
        if self._session_id is None:
            return False
        if self._expires_at is None:
            return False
        return datetime.now(timezone.utc) < self._expires_at

    async def __aenter__(self) -> "EnhancementSession":
        """
        Enter context: create session via gateway.

        Returns:
            self for use in async with statement
        """
        response = await self._create_gateway_session()
        self._session_id = response.get("session_id")
        
        # Parse expires_at if provided
        expires_at_str = response.get("expires_at")
        if expires_at_str:
            self._expires_at = self._parse_iso_datetime(expires_at_str)

        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """
        Exit context: delete session (gracefully handles failures).

        Reference: WBS 3.1.2.3.4 - Delete session after processing
        """
        if self._session_id is not None:
            try:
                await self._delete_gateway_session(self._session_id)
            except GatewayError:
                # Graceful degradation - session may already be expired or deleted
                # Reference: WBS 3.1.2.3.5 - Handle session expiry gracefully
                pass

    async def ensure_active(self) -> None:
        """
        Ensure session is active, refreshing if needed.

        Raises:
            SessionExpiredError: If session expired and auto_refresh is False.
            SessionNotCreatedError: If session not yet created.
        """
        if self._session_id is None:
            raise SessionNotCreatedError("Session not created. Use async with statement.")

        if not self.is_active:
            if self._auto_refresh:
                # Refresh: delete old (ignore errors) and create new
                try:
                    await self._delete_gateway_session(self._session_id)
                except GatewayError:
                    pass

                response = await self._create_gateway_session()
                self._session_id = response.get("session_id")
                expires_at_str = response.get("expires_at")
                if expires_at_str:
                    self._expires_at = self._parse_iso_datetime(expires_at_str)
            else:
                raise SessionExpiredError(self._session_id)

    async def enhance(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.0,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        Perform enhancement using session context.

        Args:
            prompt: Enhancement prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_prompt: Optional system prompt

        Returns:
            LLMResponse with enhancement content

        Raises:
            SessionExpiredError: If session expired and auto_refresh disabled
            SessionNotCreatedError: If session not created
        """
        await self.ensure_active()

        # Build messages
        messages: list[dict[str, Any]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Call gateway with session_id
        response = await self._call_gateway_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return self._parse_completion_response(response)

    # =========================================================================
    # Internal Gateway Methods
    # =========================================================================

    async def _create_gateway_session(self) -> dict[str, Any]:
        """Create session via LLMGatewayClient."""
        async with LLMGatewayClient(base_url=self._gateway_url) as client:
            return await client.create_session(
                ttl_seconds=self._ttl_seconds,
                context=self._context,
            )

    async def _delete_gateway_session(self, session_id: str) -> None:
        """Delete session via LLMGatewayClient."""
        async with LLMGatewayClient(base_url=self._gateway_url) as client:
            await client.delete_session(session_id)

    async def _call_gateway_completion(
        self,
        messages: list[dict[str, Any]],
        max_tokens: int,
        temperature: float,
    ) -> dict[str, Any]:
        """Call chat completion with session_id."""
        async with LLMGatewayClient(base_url=self._gateway_url) as client:
            return await client.chat_completion(
                model=self._model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                session_id=self._session_id,
            )

    def _parse_completion_response(self, response: dict[str, Any]) -> LLMResponse:
        """Parse gateway response into LLMResponse."""
        choices = response.get("choices", [])
        if not choices:
            return LLMResponse(
                content="",
                model=self._model,
                input_tokens=0,
                output_tokens=0,
            )

        message = choices[0].get("message", {})
        content = message.get("content", "")
        finish_reason = choices[0].get("finish_reason")

        usage = response.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        model = response.get("model", self._model)

        return LLMResponse(
            content=content,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            stop_reason=finish_reason,
        )

    def _parse_iso_datetime(self, iso_str: str) -> datetime:
        """Parse ISO datetime string to datetime object."""
        # Handle various ISO formats
        if iso_str.endswith("Z"):
            iso_str = iso_str[:-1] + "+00:00"
        return datetime.fromisoformat(iso_str)
