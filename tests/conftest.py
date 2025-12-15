"""
Pytest configuration for comprehensive test suite.

This configuration sets up:
- Test discovery paths
- Shared fixtures
- Test markers
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "integration: Integration tests for workflow interactions")
    config.addinivalue_line("markers", "e2e: End-to-end workflow tests")
    config.addinivalue_line("markers", "slow: Tests that take a long time to run")
    config.addinivalue_line("markers", "pipeline: Full pipeline integration tests")
    config.addinivalue_line("markers", "live: Tests that require live services")
