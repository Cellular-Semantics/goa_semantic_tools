"""
Unit Tests for CLI module

Tests CLI helper functions without requiring full pipeline execution.
"""

import pytest
import tempfile
from pathlib import Path

from goa_semantic_tools.cli import parse_gene_list


@pytest.mark.unit
class TestParseGeneList:
    """Tests for parse_gene_list function."""

    def test_comma_separated_list(self):
        """Parse comma-separated gene list."""
        genes = parse_gene_list("TP53,BRCA1,BRCA2", None)
        assert genes == ["TP53", "BRCA1", "BRCA2"]

    def test_comma_separated_with_spaces(self):
        """Parse comma-separated list with spaces."""
        genes = parse_gene_list("TP53, BRCA1, BRCA2", None)
        assert genes == ["TP53", "BRCA1", "BRCA2"]

    def test_lowercase_converted_to_uppercase(self):
        """Gene symbols should be uppercased."""
        genes = parse_gene_list("tp53,brca1", None)
        assert genes == ["TP53", "BRCA1"]

    def test_empty_strings_removed(self):
        """Empty strings between commas should be removed."""
        genes = parse_gene_list("TP53,,BRCA1,", None)
        assert genes == ["TP53", "BRCA1"]

    def test_both_args_raises(self):
        """Providing both --genes and --genes-file should raise."""
        with pytest.raises(ValueError, match="Provide either --genes or --genes-file"):
            parse_gene_list("TP53", "genes.txt")

    def test_neither_arg_raises(self):
        """Providing neither argument should raise."""
        with pytest.raises(ValueError, match="Must provide either --genes or --genes-file"):
            parse_gene_list(None, None)

    def test_file_not_found_raises(self):
        """Non-existent file should raise."""
        with pytest.raises(ValueError, match="Gene list file not found"):
            parse_gene_list(None, "/nonexistent/path/genes.txt")

    def test_read_from_file(self):
        """Read gene list from file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("TP53\n")
            f.write("BRCA1\n")
            f.write("BRCA2\n")
            f.flush()

            genes = parse_gene_list(None, f.name)
            assert genes == ["TP53", "BRCA1", "BRCA2"]

            # Cleanup
            Path(f.name).unlink()

    def test_file_with_comments(self):
        """Comments in file should be ignored."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("# This is a comment\n")
            f.write("TP53\n")
            f.write("# Another comment\n")
            f.write("BRCA1\n")
            f.write("\n")  # Empty line
            f.write("BRCA2\n")
            f.flush()

            genes = parse_gene_list(None, f.name)
            assert genes == ["TP53", "BRCA1", "BRCA2"]

            # Cleanup
            Path(f.name).unlink()

    def test_file_lowercase_converted(self):
        """Lowercase genes in file should be uppercased."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("tp53\n")
            f.write("Brca1\n")
            f.flush()

            genes = parse_gene_list(None, f.name)
            assert genes == ["TP53", "BRCA1"]

            # Cleanup
            Path(f.name).unlink()

    def test_single_gene(self):
        """Single gene should work."""
        genes = parse_gene_list("TP53", None)
        assert genes == ["TP53"]

    def test_many_genes(self):
        """Many genes should work."""
        gene_list = ",".join([f"GENE{i}" for i in range(100)])
        genes = parse_gene_list(gene_list, None)
        assert len(genes) == 100
        assert genes[0] == "GENE0"
        assert genes[99] == "GENE99"
