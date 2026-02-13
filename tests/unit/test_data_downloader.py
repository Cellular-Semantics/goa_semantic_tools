"""
Unit Tests for Data Downloader

Tests helper functions without network access.
"""

import pytest
from pathlib import Path

from goa_semantic_tools.utils.data_downloader import (
    get_reference_data_dir,
    get_test_data_dir,
    get_test_gaf_path,
    ensure_gaf_data,
)


@pytest.mark.unit
class TestGetReferenceDataDir:
    """Tests for get_reference_data_dir function."""

    def test_returns_path(self):
        """Should return a Path object."""
        result = get_reference_data_dir()
        assert isinstance(result, Path)

    def test_path_is_reference_data(self):
        """Path should end with reference_data."""
        result = get_reference_data_dir()
        assert result.name == "reference_data"

    def test_creates_directory(self):
        """Should create directory if it doesn't exist."""
        result = get_reference_data_dir()
        assert result.exists()
        assert result.is_dir()


@pytest.mark.unit
class TestGetTestDataDir:
    """Tests for get_test_data_dir function."""

    def test_returns_path(self):
        """Should return a Path object."""
        result = get_test_data_dir()
        assert isinstance(result, Path)

    def test_path_is_test_data(self):
        """Path should end with test_data."""
        result = get_test_data_dir()
        assert result.name == "test_data"

    def test_parent_is_tests(self):
        """Parent should be tests directory."""
        result = get_test_data_dir()
        assert result.parent.name == "tests"


@pytest.mark.unit
class TestGetTestGafPath:
    """Tests for get_test_gaf_path function."""

    def test_returns_path_or_none(self):
        """Should return Path or None."""
        result = get_test_gaf_path()
        assert result is None or isinstance(result, Path)


@pytest.mark.unit
class TestEnsureGafDataValidation:
    """Tests for ensure_gaf_data input validation."""

    def test_invalid_species_raises(self):
        """Invalid species should raise ValueError."""
        with pytest.raises(ValueError, match="Unsupported species"):
            ensure_gaf_data(species="fish")

    def test_invalid_species_message(self):
        """Error message should include valid options."""
        with pytest.raises(ValueError, match="human.*mouse|mouse.*human"):
            ensure_gaf_data(species="rat")
