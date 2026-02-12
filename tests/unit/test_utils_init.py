"""
Unit tests for utils __init__ module.

Tests utility helper functions.
"""
from __future__ import annotations

import pytest

from goa_semantic_tools.utils import ToolingContext, chunk_items


@pytest.mark.unit
class TestChunkItems:
    """Tests for chunk_items function."""

    def test_basic_chunking(self):
        """Test basic chunking."""
        items = ["a", "b", "c", "d", "e"]
        chunks = chunk_items(items, size=2)

        assert len(chunks) == 3
        assert chunks[0] == ["a", "b"]
        assert chunks[1] == ["c", "d"]
        assert chunks[2] == ["e"]

    def test_exact_size(self):
        """Test when items divide evenly."""
        items = ["a", "b", "c", "d"]
        chunks = chunk_items(items, size=2)

        assert len(chunks) == 2
        assert all(len(c) == 2 for c in chunks)

    def test_larger_size(self):
        """Test when size is larger than items."""
        items = ["a", "b"]
        chunks = chunk_items(items, size=10)

        assert len(chunks) == 1
        assert chunks[0] == ["a", "b"]

    def test_empty_input(self):
        """Test with empty input."""
        chunks = chunk_items([], size=10)

        assert chunks == []

    def test_generator_input(self):
        """Test with generator input."""
        def gen():
            yield "a"
            yield "b"
            yield "c"

        chunks = chunk_items(gen(), size=2)

        assert len(chunks) == 2


@pytest.mark.unit
class TestToolingContext:
    """Tests for ToolingContext dataclass."""

    def test_creation(self):
        """Test basic creation."""
        ctx = ToolingContext(workspace="/path/to/workspace")

        assert ctx.workspace == "/path/to/workspace"
        assert ctx.dry_run is False

    def test_with_dry_run(self):
        """Test with dry_run flag."""
        ctx = ToolingContext(workspace="/path", dry_run=True)

        assert ctx.dry_run is True
