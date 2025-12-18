"""
Pytest configuration for tests_unit directory.

WBS MSE-6: Adds project root to Python path for imports.
Reference: tests/conftest.py pattern
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
