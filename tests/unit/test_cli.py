"""
Unit Tests for CLI module

Tests CLI helper functions and argument parsing without requiring full pipeline execution.
"""

import json
import tempfile
import warnings
from pathlib import Path
from unittest.mock import patch

import pytest

from goa_semantic_tools.cli import (
    _determine_input_mode,
    _load_and_validate_json,
    _load_literature_json,
    _save_literature_json,
    _warn_ignored_params,
    parse_gene_list,
)


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
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("TP53\n")
            f.write("BRCA1\n")
            f.write("BRCA2\n")
            f.flush()

            genes = parse_gene_list(None, f.name)
            assert genes == ["TP53", "BRCA1", "BRCA2"]

            Path(f.name).unlink()

    def test_file_with_comments(self):
        """Comments in file should be ignored."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("# This is a comment\n")
            f.write("TP53\n")
            f.write("# Another comment\n")
            f.write("BRCA1\n")
            f.write("\n")  # Empty line
            f.write("BRCA2\n")
            f.flush()

            genes = parse_gene_list(None, f.name)
            assert genes == ["TP53", "BRCA1", "BRCA2"]

            Path(f.name).unlink()

    def test_file_lowercase_converted(self):
        """Lowercase genes in file should be uppercased."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("tp53\n")
            f.write("Brca1\n")
            f.flush()

            genes = parse_gene_list(None, f.name)
            assert genes == ["TP53", "BRCA1"]

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


@pytest.mark.unit
class TestDetermineInputMode:
    """Tests for _determine_input_mode."""

    def _make_args(self, **kwargs):
        from argparse import Namespace

        defaults = {
            "genes": None,
            "genes_file": None,
            "enrichment_json": None,
            "literature_json": None,
        }
        defaults.update(kwargs)
        return Namespace(**defaults)

    def test_genes_mode(self):
        args = self._make_args(genes="TP53,BRCA1")
        assert _determine_input_mode(args) == "genes"

    def test_genes_file_mode(self):
        args = self._make_args(genes_file="genes.txt")
        assert _determine_input_mode(args) == "genes"

    def test_enrichment_json_mode(self):
        args = self._make_args(enrichment_json="results/test_enrichment.json")
        assert _determine_input_mode(args) == "enrichment"

    def test_literature_json_mode(self):
        args = self._make_args(literature_json="results/test_literature.json")
        assert _determine_input_mode(args) == "literature"


@pytest.mark.unit
class TestLoadAndValidateJson:
    """Tests for _load_and_validate_json."""

    def test_valid_json(self, tmp_path):
        p = tmp_path / "test.json"
        p.write_text(json.dumps({"themes": [1, 2, 3]}))
        data = _load_and_validate_json(p, "themes", "Test")
        assert data["themes"] == [1, 2, 3]

    def test_missing_file(self, tmp_path):
        p = tmp_path / "missing.json"
        with pytest.raises(ValueError, match="file not found"):
            _load_and_validate_json(p, "themes", "Test")

    def test_missing_key(self, tmp_path):
        p = tmp_path / "test.json"
        p.write_text(json.dumps({"other": 123}))
        with pytest.raises(ValueError, match="missing required key 'themes'"):
            _load_and_validate_json(p, "themes", "Test")

    def test_not_object(self, tmp_path):
        p = tmp_path / "test.json"
        p.write_text(json.dumps([1, 2, 3]))
        with pytest.raises(ValueError, match="must be a JSON object"):
            _load_and_validate_json(p, "themes", "Test")


@pytest.mark.unit
class TestLiteratureJsonRoundtrip:
    """Tests for _save_literature_json and _load_literature_json."""

    def test_roundtrip(self, tmp_path):
        base = tmp_path / "test"
        gaf_pmids = {0: [{"pmid": "12345"}], 1: [{"pmid": "67890"}]}
        gaf_abstracts = {0: [{"pmid": "12345", "abstract": "text"}]}
        hub_gene_abstracts = {"SRC": [{"pmid": "11111"}]}
        snippet_evidence = {0: [{"snippet": "foo"}]}
        hub_gene_snippets = {"SRC": [{"snippet": "bar"}]}

        lit_path = _save_literature_json(
            base, "test_enrichment.json",
            gaf_pmids, gaf_abstracts, hub_gene_abstracts,
            snippet_evidence, hub_gene_snippets,
        )

        assert lit_path.exists()
        assert lit_path.name == "test_literature.json"

        loaded = _load_literature_json(lit_path)
        assert loaded["enrichment_source"] == "test_enrichment.json"
        assert loaded["gaf_pmids"][0] == [{"pmid": "12345"}]
        assert loaded["gaf_pmids"][1] == [{"pmid": "67890"}]
        assert loaded["gaf_abstracts"][0] == [{"pmid": "12345", "abstract": "text"}]
        assert loaded["hub_gene_abstracts"]["SRC"] == [{"pmid": "11111"}]
        assert loaded["snippet_evidence"][0] == [{"snippet": "foo"}]
        assert loaded["hub_gene_snippets"]["SRC"] == [{"snippet": "bar"}]

    def test_roundtrip_with_nones(self, tmp_path):
        base = tmp_path / "test"
        lit_path = _save_literature_json(base, "src.json", None, None, None, None, None)
        loaded = _load_literature_json(lit_path)
        assert loaded["gaf_pmids"] == {}
        assert loaded["hub_gene_abstracts"] == {}

    def test_load_missing_enrichment_source(self, tmp_path):
        p = tmp_path / "bad_literature.json"
        p.write_text(json.dumps({"gaf_pmids": {}}))
        with pytest.raises(ValueError, match="missing required key 'enrichment_source'"):
            _load_literature_json(p)


@pytest.mark.unit
class TestWarnIgnoredParams:
    """Tests for _warn_ignored_params."""

    def _make_args(self, **kwargs):
        from argparse import Namespace

        defaults = {
            "species": "human",
            "fdr": 0.05,
            "min_ic": 3.0,
            "min_leaves": 2,
            "max_genes": 30,
            "namespace": None,
        }
        defaults.update(kwargs)
        return Namespace(**defaults)

    def test_no_warning_for_genes_mode(self):
        args = self._make_args(fdr=0.01)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _warn_ignored_params(args, "genes")
        assert len(w) == 0

    def test_warning_for_enrichment_mode_with_changed_params(self):
        args = self._make_args(fdr=0.01, species="mouse")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _warn_ignored_params(args, "enrichment")
        assert len(w) == 1
        assert "--fdr" in str(w[0].message)
        assert "--species" in str(w[0].message)

    def test_no_warning_for_enrichment_mode_defaults(self):
        args = self._make_args()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            _warn_ignored_params(args, "enrichment")
        assert len(w) == 0


@pytest.mark.unit
class TestArgParsing:
    """Test argparse configuration via main() with sys.argv patching."""

    def test_genes_and_output_required(self):
        """At least one input and --output are required."""
        with pytest.raises(SystemExit):
            with patch("sys.argv", ["prog", "--output", "test"]):
                from goa_semantic_tools.cli import main
                main()

    def test_mutually_exclusive_inputs(self):
        """Cannot use --genes and --enrichment-json together."""
        with pytest.raises(SystemExit):
            with patch(
                "sys.argv",
                ["prog", "--genes", "TP53", "--enrichment-json", "x.json", "-o", "test"],
            ):
                from goa_semantic_tools.cli import main
                main()

    def test_stop_after_enrichment_with_enrichment_json_fails(self):
        """--stop-after enrichment + --enrichment-json is invalid."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"themes": []}, f)
            f.flush()
            with patch(
                "sys.argv",
                ["prog", "--enrichment-json", f.name, "-o", "test", "--stop-after", "enrichment"],
            ):
                from goa_semantic_tools.cli import main
                result = main()
                assert result == 1
            Path(f.name).unlink()

    def test_stop_after_literature_with_literature_json_fails(self):
        """--stop-after literature + --literature-json is invalid."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"enrichment_source": "x.json"}, f)
            f.flush()
            with patch(
                "sys.argv",
                ["prog", "--literature-json", f.name, "-o", "test", "--stop-after", "literature"],
            ):
                from goa_semantic_tools.cli import main
                result = main()
                assert result == 1
            Path(f.name).unlink()
