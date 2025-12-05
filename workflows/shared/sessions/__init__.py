"""
Sessions Module - WBS 3.1.2.3 Session-Based Enhancement

Provides session management for multi-turn enhancement workflows.
"""

from workflows.shared.sessions.enhancement_session import (
    EnhancementSession,
    SessionExpiredError,
)

__all__ = [
    "EnhancementSession",
    "SessionExpiredError",
]
