"""Unit tests for batch mode CLI (--project flag)."""
import argparse
import csv
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from goa_semantic_tools.cli import _parse_project_csv, _run_batch


# =============================================================================
# Helpers
# =============================================================================

def _make_args(**kwargs) -> argparse.Namespace:
    """Return a minimal Namespace suitable for batch tests."""
    defaults = dict(
        project=None,
        output=None,
        species="human",
        model="gpt-4o",
        max_tokens=None,
        fdr=0.05,
        min_ic=3.0,
        min_leaves=2,
        max_genes=30,
        namespace=None,
        stop_after=None,
        literature_search=False,
        max_explained_themes=30,
        dry_run=False,
    )
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# =============================================================================
# _parse_project_csv
# =============================================================================

@pytest.mark.unit
class TestParseProjectCsv:

    def test_returns_list_of_dicts(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "A", "genes": "TP53,BRCA1"},
            {"name": "B", "genes": "MYC,KRAS"},
        ])
        rows = _parse_project_csv(csv_file)
        assert len(rows) == 2
        assert rows[0]["name"] == "A"
        assert rows[1]["genes"] == "MYC,KRAS"

    def test_raises_if_file_missing(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="not found"):
            _parse_project_csv(tmp_path / "nonexistent.csv")

    def test_raises_if_empty(self, tmp_path):
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("name,genes\n")
        with pytest.raises(ValueError, match="empty"):
            _parse_project_csv(csv_file)

    def test_raises_if_name_column_missing(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [{"genes": "TP53", "description": "x"}])
        with pytest.raises(ValueError, match="'name'"):
            _parse_project_csv(csv_file)

    def test_raises_if_genes_column_missing(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [{"name": "A", "description": "x"}])
        with pytest.raises(ValueError, match="'genes'"):
            _parse_project_csv(csv_file)

    def test_optional_columns_preserved(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "A", "genes": "TP53", "species": "mouse", "description": "test"}
        ])
        rows = _parse_project_csv(csv_file)
        assert rows[0]["species"] == "mouse"
        assert rows[0]["description"] == "test"


# =============================================================================
# _run_batch — core behaviour
# =============================================================================

@pytest.mark.unit
class TestRunBatch:

    def test_calls_pipeline_for_each_row(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "C1", "genes": "TP53,BRCA1"},
            {"name": "C2", "genes": "MYC,KRAS,AKT1"},
        ])
        args = _make_args(project=str(csv_file))

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline, \
             patch("goa_semantic_tools.cli.Path") as mock_path_cls:
            # Let Path work normally except for results/ mkdir
            mock_path_cls.side_effect = lambda *a, **k: Path(*a, **k)
            _run_batch(args)

        assert mock_pipeline.call_count == 2
        # First call genes
        first_call_genes = mock_pipeline.call_args_list[0][0][2]
        assert "TP53" in first_call_genes and "BRCA1" in first_call_genes
        # Second call genes
        second_call_genes = mock_pipeline.call_args_list[1][0][2]
        assert set(second_call_genes) == {"MYC", "KRAS", "AKT1"}

    def test_input_mode_is_always_genes(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [{"name": "X", "genes": "TP53"}])
        args = _make_args(project=str(csv_file))

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline:
            _run_batch(args)

        input_mode = mock_pipeline.call_args_list[0][0][1]
        assert input_mode == "genes"

    def test_output_path_uses_datestamp_and_name(self, tmp_path, monkeypatch):
        csv_file = tmp_path / "myproject.csv"
        _write_csv(csv_file, [{"name": "clusterA", "genes": "TP53,BRCA1"}])
        args = _make_args(project=str(csv_file))

        fixed_dt = "2026-03-27_120000"
        monkeypatch.setattr(
            "goa_semantic_tools.cli.datetime",
            type("FakeDT", (), {"now": staticmethod(lambda: type("T", (), {"strftime": lambda self, fmt: fixed_dt})())}),
        )

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline:
            _run_batch(args)

        base_output: Path = mock_pipeline.call_args_list[0][0][3]
        assert base_output.name == "clusterA"
        assert fixed_dt in str(base_output)
        assert "clusterA" in str(base_output.parent)

    def test_species_override_from_csv_row(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "A", "genes": "Trp53,Brca1", "species": "mouse"},
        ])
        args = _make_args(project=str(csv_file), species="human")

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline:
            _run_batch(args)

        args_row = mock_pipeline.call_args_list[0][0][0]
        assert args_row.species == "mouse"

    def test_default_species_used_when_not_in_csv(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [{"name": "A", "genes": "TP53"}])
        args = _make_args(project=str(csv_file), species="human")

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline:
            _run_batch(args)

        args_row = mock_pipeline.call_args_list[0][0][0]
        assert args_row.species == "human"

    def test_continues_after_single_failure(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "good1", "genes": "TP53"},
            {"name": "bad",   "genes": "BRCA1"},
            {"name": "good2", "genes": "MYC"},
        ])
        args = _make_args(project=str(csv_file))

        call_count = 0
        def pipeline_side_effect(args_row, mode, genes, base_output):
            nonlocal call_count
            call_count += 1
            if args_row.species == "human" and genes == ["BRCA1"]:
                raise RuntimeError("simulated failure")

        with patch("goa_semantic_tools.cli._run_pipeline", side_effect=pipeline_side_effect):
            rc = _run_batch(args)

        assert call_count == 3
        assert rc == 1  # non-zero because one failed

    def test_returns_zero_when_all_succeed(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "A", "genes": "TP53"},
            {"name": "B", "genes": "MYC"},
        ])
        args = _make_args(project=str(csv_file))

        with patch("goa_semantic_tools.cli._run_pipeline"):
            rc = _run_batch(args)

        assert rc == 0

    def test_returns_one_when_any_fails(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [{"name": "A", "genes": "TP53"}])
        args = _make_args(project=str(csv_file))

        with patch("goa_semantic_tools.cli._run_pipeline", side_effect=RuntimeError("boom")):
            rc = _run_batch(args)

        assert rc == 1

    def test_skips_row_with_empty_genes(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "empty", "genes": ""},
            {"name": "ok",    "genes": "TP53"},
        ])
        args = _make_args(project=str(csv_file))

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline:
            _run_batch(args)

        assert mock_pipeline.call_count == 1  # only the non-empty row

    def test_manifest_written_to_results_dir(self, tmp_path, monkeypatch):
        csv_file = tmp_path / "proj.csv"
        _write_csv(csv_file, [{"name": "A", "genes": "TP53"}])
        args = _make_args(project=str(csv_file))

        # Redirect results/ to tmp_path
        monkeypatch.chdir(tmp_path)

        with patch("goa_semantic_tools.cli._run_pipeline"):
            _run_batch(args)

        manifest = tmp_path / "results" / "proj" / "batch_run.json"
        assert manifest.exists()
        data = json.loads(manifest.read_text())
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["rows"][0]["name"] == "A"

    def test_manifest_appends_on_subsequent_runs(self, tmp_path, monkeypatch):
        csv_file = tmp_path / "proj.csv"
        _write_csv(csv_file, [{"name": "A", "genes": "TP53"}])
        args = _make_args(project=str(csv_file))
        monkeypatch.chdir(tmp_path)

        with patch("goa_semantic_tools.cli._run_pipeline"):
            _run_batch(args)
            _run_batch(args)

        manifest = tmp_path / "results" / "proj" / "batch_run.json"
        data = json.loads(manifest.read_text())
        assert len(data) == 2

    def test_dry_run_does_not_call_pipeline(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [
            {"name": "A", "genes": "TP53,BRCA1"},
            {"name": "B", "genes": "MYC"},
        ])
        args = _make_args(project=str(csv_file), dry_run=True)

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline:
            rc = _run_batch(args)

        mock_pipeline.assert_not_called()
        assert rc == 0

    def test_genes_parsed_with_whitespace_stripping(self, tmp_path):
        csv_file = tmp_path / "project.csv"
        _write_csv(csv_file, [{"name": "A", "genes": " TP53 , BRCA1 , MYC "}])
        args = _make_args(project=str(csv_file))

        with patch("goa_semantic_tools.cli._run_pipeline") as mock_pipeline:
            _run_batch(args)

        genes = mock_pipeline.call_args_list[0][0][2]
        assert genes == ["TP53", "BRCA1", "MYC"]
