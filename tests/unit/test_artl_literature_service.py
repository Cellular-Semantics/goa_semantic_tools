"""
Unit tests for artl Literature Service.

TDD: Tests written BEFORE implementation.
Tests cover prompt loading, JSON parsing, prompt building, and the
resolve_assertions_via_literature orchestration function.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from goa_semantic_tools.services.reference_retrieval_service import (
    AtomicAssertion,
    ReferenceMatch,
)


# =============================================================================
# Test _extract_json helper
# =============================================================================


@pytest.mark.unit
class TestExtractJson:
    """Tests for _extract_json helper."""

    def test_bare_json(self):
        """Test extracting bare JSON object."""
        from goa_semantic_tools.services.artl_literature_service import _extract_json

        text = '{"references_found": [{"pmid": "12345"}]}'
        result = _extract_json(text)
        assert result is not None
        assert "references_found" in result

    def test_code_fenced_json(self):
        """Test extracting JSON from markdown code fence."""
        from goa_semantic_tools.services.artl_literature_service import _extract_json

        text = """Here are the results:
```json
{"references_found": [{"pmid": "12345"}]}
```
"""
        result = _extract_json(text)
        assert result is not None
        assert "references_found" in result

    def test_code_fence_no_language(self):
        """Test extracting JSON from code fence without language tag."""
        from goa_semantic_tools.services.artl_literature_service import _extract_json

        text = """Results:
```
{"references_found": []}
```
"""
        result = _extract_json(text)
        assert result is not None
        assert "references_found" in result

    def test_no_json_returns_none(self):
        """Test that non-JSON text returns None."""
        from goa_semantic_tools.services.artl_literature_service import _extract_json

        text = "No JSON here, just regular text about genes."
        result = _extract_json(text)
        assert result is None

    def test_nested_braces(self):
        """Test JSON with nested objects."""
        from goa_semantic_tools.services.artl_literature_service import _extract_json

        text = '{"references_found": [{"pmid": "123", "meta": {"key": "val"}}]}'
        result = _extract_json(text)
        assert result is not None
        assert result["references_found"][0]["meta"]["key"] == "val"

    def test_json_with_surrounding_text(self):
        """Test extracting JSON surrounded by non-JSON text."""
        from goa_semantic_tools.services.artl_literature_service import _extract_json

        text = 'I found these results: {"references_found": []} End of results.'
        result = _extract_json(text)
        assert result is not None


# =============================================================================
# Test _parse_literature_response
# =============================================================================


@pytest.mark.unit
class TestParseLiteratureResponse:
    """Tests for _parse_literature_response."""

    def _make_assertion(self, genes=None, go_terms=None):
        return AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="ATM and BRCA1 cooperate in DNA damage response",
            genes=genes or ["ATM", "BRCA1"],
            go_term_ids=go_terms or ["GO:0006974"],
            is_multi_gene=True,
            is_multi_process=False,
        )

    def test_valid_json_response(self):
        """Test parsing a valid JSON response with references."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = '{"references_found": [{"pmid": "12345678", "title": "ATM paper", "relevance": "good"}]}'
        assertion = self._make_assertion()

        refs = _parse_literature_response(response, assertion)

        assert len(refs) == 1
        assert refs[0].pmid == "12345678"
        assert refs[0].match_type == "literature"
        assert refs[0].genes_covered == ["ATM", "BRCA1"]
        assert refs[0].go_terms_covered == ["GO:0006974"]

    def test_code_fenced_json_response(self):
        """Test parsing JSON wrapped in code fences."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = """Here are the results:
```json
{"references_found": [{"pmid": "99999999", "title": "A paper"}]}
```
"""
        assertion = self._make_assertion()
        refs = _parse_literature_response(response, assertion)

        assert len(refs) == 1
        assert refs[0].pmid == "99999999"

    def test_empty_references(self):
        """Test parsing response with no references found."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = '{"references_found": [], "confidence": "low"}'
        assertion = self._make_assertion()

        refs = _parse_literature_response(response, assertion)
        assert refs == []

    def test_malformed_json(self):
        """Test graceful handling of malformed JSON."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = "This is not JSON at all, just regular text."
        assertion = self._make_assertion()

        refs = _parse_literature_response(response, assertion)
        assert refs == []

    def test_missing_pmid(self):
        """Test that references without pmid are skipped."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = '{"references_found": [{"title": "No PMID paper"}]}'
        assertion = self._make_assertion()

        refs = _parse_literature_response(response, assertion)
        assert refs == []

    def test_pmid_prefix_stripping(self):
        """Test that 'PMID:' prefix is stripped from pmid values."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = '{"references_found": [{"pmid": "PMID:12345678", "title": "Paper"}]}'
        assertion = self._make_assertion()

        refs = _parse_literature_response(response, assertion)
        assert len(refs) == 1
        assert refs[0].pmid == "12345678"

    def test_genes_and_go_terms_from_assertion(self):
        """Test that genes and GO terms come from the assertion."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = '{"references_found": [{"pmid": "111"}]}'
        assertion = self._make_assertion(
            genes=["TP53", "MDM2"], go_terms=["GO:0006915", "GO:0006281"]
        )

        refs = _parse_literature_response(response, assertion)
        assert refs[0].genes_covered == ["TP53", "MDM2"]
        assert refs[0].go_terms_covered == ["GO:0006915", "GO:0006281"]

    def test_max_refs_honored(self):
        """Test that max_refs limits the number of results."""
        from goa_semantic_tools.services.artl_literature_service import (
            _parse_literature_response,
        )

        response = '{"references_found": [{"pmid": "1"}, {"pmid": "2"}, {"pmid": "3"}, {"pmid": "4"}, {"pmid": "5"}]}'
        assertion = self._make_assertion()

        refs = _parse_literature_response(response, assertion, max_refs=2)
        assert len(refs) == 2


# =============================================================================
# Test _build_user_prompt
# =============================================================================


@pytest.mark.unit
class TestBuildUserPrompt:
    """Tests for _build_user_prompt."""

    def test_includes_assertion_text(self):
        """Test that prompt includes the assertion text."""
        from goa_semantic_tools.services.artl_literature_service import (
            _build_user_prompt,
        )

        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="ATM phosphorylates BRCA1 during DNA damage",
            genes=["ATM", "BRCA1"],
            go_term_ids=["GO:0006974"],
            is_multi_gene=True,
            is_multi_process=False,
        )

        prompt = _build_user_prompt(assertion, max_refs=3)

        assert "ATM phosphorylates BRCA1" in prompt
        assert "ATM" in prompt
        assert "BRCA1" in prompt

    def test_includes_go_terms(self):
        """Test that prompt includes GO term IDs."""
        from goa_semantic_tools.services.artl_literature_service import (
            _build_user_prompt,
        )

        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="Some assertion",
            genes=["TP53"],
            go_term_ids=["GO:0006915", "GO:0006281"],
            is_multi_gene=False,
            is_multi_process=True,
        )

        prompt = _build_user_prompt(assertion, max_refs=3)

        assert "GO:0006915" in prompt
        assert "GO:0006281" in prompt

    def test_limits_genes_to_five(self):
        """Test that only first 5 genes are included."""
        from goa_semantic_tools.services.artl_literature_service import (
            _build_user_prompt,
        )

        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="Many genes",
            genes=["G1", "G2", "G3", "G4", "G5", "G6", "G7"],
            go_term_ids=["GO:0000001"],
            is_multi_gene=True,
            is_multi_process=False,
        )

        prompt = _build_user_prompt(assertion, max_refs=3)

        assert "G5" in prompt
        assert "G6" not in prompt
        assert "G7" not in prompt


# =============================================================================
# Test prompt loading
# =============================================================================


@pytest.mark.unit
class TestPromptLoading:
    """Tests for loading the artl_literature_search.prompt.yaml file."""

    def test_prompt_file_loads(self):
        """Test that prompt YAML file loads successfully."""
        from goa_semantic_tools.services.artl_literature_service import _load_prompt

        config = _load_prompt("artl_literature_search.prompt.yaml")

        assert "system_prompt" in config
        assert "user_prompt" in config

    def test_prompt_has_required_keys(self):
        """Test that prompt has system_prompt, user_prompt, and presets."""
        from goa_semantic_tools.services.artl_literature_service import _load_prompt

        config = _load_prompt("artl_literature_search.prompt.yaml")

        assert isinstance(config["system_prompt"], str)
        assert isinstance(config["user_prompt"], str)
        assert "presets" in config


# =============================================================================
# Test resolve_assertions_via_literature (orchestration)
# =============================================================================


@pytest.mark.unit
class TestResolveAssertionsViaLiterature:
    """Tests for the main resolve_assertions_via_literature function."""

    def _make_assertion(self, text="ATM cooperates with BRCA1", genes=None):
        return AtomicAssertion(
            claim_type="EXTERNAL",
            original_text=text,
            genes=genes or ["ATM", "BRCA1"],
            go_term_ids=["GO:0006974"],
            is_multi_gene=True,
            is_multi_process=False,
        )

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    @patch("goa_semantic_tools.services.artl_literature_service.LiteLLMAgent")
    def test_single_resolved(self, mock_agent_cls, mock_mcp_cls):
        """Test resolving a single assertion successfully."""
        from goa_semantic_tools.services.artl_literature_service import (
            resolve_assertions_via_literature,
        )

        # Mock MCPToolSource context manager
        mock_source = MagicMock()
        mock_source.tools = [MagicMock(name="search_europepmc_papers")]
        mock_mcp_cls.return_value.__enter__ = MagicMock(return_value=mock_source)
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        # Mock LLM agent response
        mock_result = MagicMock()
        mock_result.text = '{"references_found": [{"pmid": "12345678", "title": "Test paper"}]}'
        mock_result.usage = None
        mock_agent = MagicMock()
        mock_agent.query_unified.return_value = mock_result
        mock_agent_cls.return_value = mock_agent

        assertions = [self._make_assertion()]
        results = resolve_assertions_via_literature(
            assertions, model="gpt-4o-mini", api_key="test-key"
        )

        assert len(results) == 1
        assertion, refs = results[0]
        assert len(refs) == 1
        assert refs[0].pmid == "12345678"
        assert refs[0].match_type == "literature"

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    @patch("goa_semantic_tools.services.artl_literature_service.LiteLLMAgent")
    def test_batch_single_session(self, mock_agent_cls, mock_mcp_cls):
        """Test that multiple assertions use a single MCPToolSource session."""
        from goa_semantic_tools.services.artl_literature_service import (
            resolve_assertions_via_literature,
        )

        mock_source = MagicMock()
        mock_source.tools = [MagicMock(name="search_europepmc_papers")]
        mock_mcp_cls.return_value.__enter__ = MagicMock(return_value=mock_source)
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        mock_result = MagicMock()
        mock_result.text = '{"references_found": [{"pmid": "111"}]}'
        mock_result.usage = None
        mock_agent = MagicMock()
        mock_agent.query_unified.return_value = mock_result
        mock_agent_cls.return_value = mock_agent

        assertions = [
            self._make_assertion("Assertion 1", ["ATM"]),
            self._make_assertion("Assertion 2", ["BRCA1"]),
            self._make_assertion("Assertion 3", ["TP53"]),
        ]
        results = resolve_assertions_via_literature(
            assertions, model="gpt-4o-mini", api_key="test-key"
        )

        assert len(results) == 3
        # MCPToolSource should only be constructed once
        assert mock_mcp_cls.call_count == 1

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    @patch("goa_semantic_tools.services.artl_literature_service.LiteLLMAgent")
    def test_mcp_failure_graceful(self, mock_agent_cls, mock_mcp_cls):
        """Test graceful degradation when MCP connection fails."""
        from goa_semantic_tools.services.artl_literature_service import (
            resolve_assertions_via_literature,
        )

        mock_mcp_cls.return_value.__enter__ = MagicMock(
            side_effect=ConnectionError("MCP subprocess failed")
        )
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        assertions = [self._make_assertion()]
        results = resolve_assertions_via_literature(
            assertions, model="gpt-4o-mini", api_key="test-key"
        )

        # Should return all assertions with empty refs, no crash
        assert len(results) == 1
        _, refs = results[0]
        assert refs == []

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    @patch("goa_semantic_tools.services.artl_literature_service.LiteLLMAgent")
    def test_llm_failure_graceful(self, mock_agent_cls, mock_mcp_cls):
        """Test graceful handling when LLM call fails for one assertion."""
        from goa_semantic_tools.services.artl_literature_service import (
            resolve_assertions_via_literature,
        )

        mock_source = MagicMock()
        mock_source.tools = [MagicMock(name="search_europepmc_papers")]
        mock_mcp_cls.return_value.__enter__ = MagicMock(return_value=mock_source)
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        # First call fails, second succeeds
        mock_result_ok = MagicMock()
        mock_result_ok.text = '{"references_found": [{"pmid": "222"}]}'
        mock_result_ok.usage = None

        mock_agent = MagicMock()
        mock_agent.query_unified.side_effect = [
            Exception("LLM timeout"),
            mock_result_ok,
        ]
        mock_agent_cls.return_value = mock_agent

        assertions = [
            self._make_assertion("Fails", ["ATM"]),
            self._make_assertion("Succeeds", ["BRCA1"]),
        ]
        results = resolve_assertions_via_literature(
            assertions, model="gpt-4o-mini", api_key="test-key"
        )

        assert len(results) == 2
        # First assertion: empty refs (LLM failed)
        assert results[0][1] == []
        # Second assertion: has refs
        assert len(results[1][1]) == 1
        assert results[1][1][0].pmid == "222"

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    @patch("goa_semantic_tools.services.artl_literature_service.LiteLLMAgent")
    def test_empty_input(self, mock_agent_cls, mock_mcp_cls):
        """Test with empty assertion list."""
        from goa_semantic_tools.services.artl_literature_service import (
            resolve_assertions_via_literature,
        )

        results = resolve_assertions_via_literature(
            [], model="gpt-4o-mini", api_key="test-key"
        )

        assert results == []
        # Should not even create MCP session
        mock_mcp_cls.assert_not_called()

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    @patch("goa_semantic_tools.services.artl_literature_service.LiteLLMAgent")
    @patch.dict("os.environ", {"OPENAI_API_KEY": "env-test-key"})
    def test_api_key_from_env(self, mock_agent_cls, mock_mcp_cls):
        """Test that api_key is resolved from environment when not provided."""
        from goa_semantic_tools.services.artl_literature_service import (
            resolve_assertions_via_literature,
        )

        mock_source = MagicMock()
        mock_source.tools = []
        mock_mcp_cls.return_value.__enter__ = MagicMock(return_value=mock_source)
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        mock_result = MagicMock()
        mock_result.text = '{"references_found": []}'
        mock_result.usage = None
        mock_agent = MagicMock()
        mock_agent.query_unified.return_value = mock_result
        mock_agent_cls.return_value = mock_agent

        assertions = [self._make_assertion()]
        resolve_assertions_via_literature(assertions, model="gpt-4o-mini")

        # Agent should be created with env key
        mock_agent_cls.assert_called_once()
        call_kwargs = mock_agent_cls.call_args
        assert call_kwargs[1]["api_key"] == "env-test-key" or call_kwargs[0][1] == "env-test-key"


# =============================================================================
# Test _parse_search_results
# =============================================================================


@pytest.mark.unit
class TestParseSearchResults:
    """Tests for _parse_search_results helper."""

    def test_bare_list_format(self):
        """Test parsing a bare JSON list of papers."""
        from goa_semantic_tools.services.artl_literature_service import _parse_search_results

        raw = '[{"pmid": "12345", "title": "Test paper", "abstractText": "An abstract."}]'
        papers = _parse_search_results(raw)

        assert len(papers) == 1
        assert papers[0]["pmid"] == "12345"
        assert papers[0]["title"] == "Test paper"
        assert papers[0]["abstract"] == "An abstract."

    def test_europe_pmc_wrapped_format(self):
        """Test parsing Europe PMC resultList.result wrapped format."""
        from goa_semantic_tools.services.artl_literature_service import _parse_search_results

        raw = '{"resultList": {"result": [{"pmid": "99999", "title": "PMC paper", "abstractText": "Abstract here."}]}}'
        papers = _parse_search_results(raw)

        assert len(papers) == 1
        assert papers[0]["pmid"] == "99999"

    def test_author_extraction(self):
        """Test that authors are extracted and formatted correctly."""
        from goa_semantic_tools.services.artl_literature_service import _parse_search_results

        raw = '[{"pmid": "1", "title": "T", "authorList": {"author": [{"lastName": "Smith"}, {"lastName": "Jones"}, {"lastName": "Brown"}, {"lastName": "Extra"}]}}]'
        papers = _parse_search_results(raw)

        assert len(papers) == 1
        assert "Smith" in papers[0]["authors"]
        assert "et al." in papers[0]["authors"]
        assert "Extra" not in papers[0]["authors"]

    def test_empty_raw_returns_empty(self):
        """Test that empty input returns empty list."""
        from goa_semantic_tools.services.artl_literature_service import _parse_search_results

        assert _parse_search_results("") == []
        assert _parse_search_results("null") == []

    def test_malformed_json_returns_empty(self):
        """Test that malformed JSON returns empty list."""
        from goa_semantic_tools.services.artl_literature_service import _parse_search_results

        assert _parse_search_results("not json at all") == []

    def test_skips_entries_without_pmid(self):
        """Test that entries without a pmid are skipped."""
        from goa_semantic_tools.services.artl_literature_service import _parse_search_results

        raw = '[{"title": "No PMID paper", "abstractText": "Abstract"}]'
        papers = _parse_search_results(raw)

        assert papers == []

    def test_year_extracted(self):
        """Test that pubYear is captured."""
        from goa_semantic_tools.services.artl_literature_service import _parse_search_results

        raw = '[{"pmid": "1", "title": "T", "pubYear": "2023", "abstractText": "A"}]'
        papers = _parse_search_results(raw)

        assert papers[0]["year"] == "2023"


# =============================================================================
# Test _build_theme_query
# =============================================================================


@pytest.mark.unit
class TestBuildThemeQuery:
    """Tests for _build_theme_query helper."""

    def _make_theme(self, anchor_name="T cell activation", genes=None):
        return {
            "anchor_term": {
                "name": anchor_name,
                "go_id": "GO:0050870",
                "genes": genes or ["RELA", "IL6", "TNF"],
            },
            "specific_terms": [],
        }

    def test_includes_anchor_name(self):
        """Test that anchor GO term name is included in query."""
        from goa_semantic_tools.services.artl_literature_service import _build_theme_query

        theme = self._make_theme(anchor_name="positive regulation of T cell activation")
        query = _build_theme_query(theme, hub_genes={})

        assert "positive regulation of T cell activation" in query

    def test_includes_top_genes(self):
        """Test that ranked genes appear in query."""
        from goa_semantic_tools.services.artl_literature_service import _build_theme_query

        theme = self._make_theme(genes=["RELA", "IL6", "TNF", "NFKB1"])
        query = _build_theme_query(theme, hub_genes={})

        # At least some of the genes should appear
        assert any(g in query for g in ["RELA", "IL6", "TNF", "NFKB1"])

    def test_returns_non_empty_string(self):
        """Test that query is always a non-empty string."""
        from goa_semantic_tools.services.artl_literature_service import _build_theme_query

        theme = self._make_theme()
        query = _build_theme_query(theme, hub_genes={})

        assert isinstance(query, str)
        assert len(query) > 0


# =============================================================================
# Test fetch_abstracts_for_themes (orchestration)
# =============================================================================


@pytest.mark.unit
class TestFetchAbstractsForThemes:
    """Tests for fetch_abstracts_for_themes orchestration function."""

    def _make_theme(self, name="T cell activation"):
        return {
            "anchor_term": {
                "name": name,
                "go_id": "GO:0050870",
                "genes": ["RELA", "IL6", "TNF"],
            },
            "specific_terms": [],
        }

    def _make_search_tool(self, return_json='[{"pmid": "12345", "title": "Paper", "abstractText": "Abstract."}]'):
        tool = MagicMock()
        tool.name = "search_europepmc_papers"
        tool.handler.return_value = return_json
        return tool

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_returns_dict_keyed_by_theme_index(self, mock_mcp_cls):
        """Test that return value is dict[int, list]."""
        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_themes

        search_tool = self._make_search_tool()
        mock_source = MagicMock()
        mock_source.tools = [search_tool]
        mock_mcp_cls.return_value.__enter__ = MagicMock(return_value=mock_source)
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        # Force lazy imports to use the mock
        import goa_semantic_tools.services.artl_literature_service as svc
        svc.MCPToolSource = mock_mcp_cls

        themes = [self._make_theme("Theme A"), self._make_theme("Theme B")]
        result = fetch_abstracts_for_themes(themes, hub_genes={})

        assert isinstance(result, dict)
        assert 0 in result
        assert 1 in result
        assert isinstance(result[0], list)

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_graceful_degradation_on_mcp_session_failure(self, mock_mcp_cls):
        """Test that MCP session failure returns all-empty dict."""
        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_themes

        mock_mcp_cls.return_value.__enter__ = MagicMock(
            side_effect=ConnectionError("MCP failed")
        )
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        import goa_semantic_tools.services.artl_literature_service as svc
        svc.MCPToolSource = mock_mcp_cls

        themes = [self._make_theme("Theme A"), self._make_theme("Theme B")]
        result = fetch_abstracts_for_themes(themes, hub_genes={})

        assert isinstance(result, dict)
        assert len(result) == 2
        assert result[0] == []
        assert result[1] == []

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_graceful_degradation_per_theme_on_tool_error(self, mock_mcp_cls):
        """Test that per-theme tool error gives empty list for that theme only."""
        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_themes

        good_tool = self._make_search_tool('[{"pmid": "111", "title": "T", "abstractText": "A"}]')
        failing_tool = MagicMock()
        failing_tool.name = "search_europepmc_papers"

        # First call raises, second succeeds
        failing_tool.handler.side_effect = [
            RuntimeError("tool error"),
            '[{"pmid": "222", "title": "T2", "abstractText": "B"}]',
        ]

        mock_source = MagicMock()
        mock_source.tools = [failing_tool]
        mock_mcp_cls.return_value.__enter__ = MagicMock(return_value=mock_source)
        mock_mcp_cls.return_value.__exit__ = MagicMock(return_value=False)

        import goa_semantic_tools.services.artl_literature_service as svc
        svc.MCPToolSource = mock_mcp_cls

        themes = [self._make_theme("Fails"), self._make_theme("Succeeds")]
        result = fetch_abstracts_for_themes(themes, hub_genes={})

        assert result[0] == []
        assert len(result[1]) == 1

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_empty_themes_returns_empty_dict(self, mock_mcp_cls):
        """Test that empty themes list returns empty dict without MCP call."""
        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_themes

        result = fetch_abstracts_for_themes([], hub_genes={})

        assert result == {}
        mock_mcp_cls.assert_not_called()


# =============================================================================
# Test fetch_abstracts_for_hub_genes
# =============================================================================


@pytest.mark.unit
class TestFetchAbstractsForHubGenes:
    """Tests for fetch_abstracts_for_hub_genes."""

    def _make_hub_genes(self, names_counts):
        """Helper: build hub_genes dict."""
        return {
            gene: {"theme_count": count, "themes": [f"theme_{i}" for i in range(min(count, 3))]}
            for gene, count in names_counts.items()
        }

    def _make_mock_source(self, return_json):
        """Helper: build mock MCPToolSource context manager."""
        mock_tool = MagicMock()
        mock_tool.name = "search_europepmc_papers"
        mock_tool.handler.return_value = return_json

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]

        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)

        return mock_ctx, mock_tool

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_empty_hub_genes_returns_empty_dict(self, mock_mcp_cls):
        """Empty hub_genes → empty dict, no MCP call."""
        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_hub_genes

        result = fetch_abstracts_for_hub_genes({})
        assert result == {}
        mock_mcp_cls.assert_not_called()

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_selects_top_n_hub_genes_by_theme_count(self, mock_mcp_cls):
        """Only top max_hub_genes genes (by theme_count) are searched."""
        import json

        paper_json = json.dumps([{"pmid": "11111", "title": "Test", "abstractText": "Abstract"}])
        mock_ctx, mock_tool = self._make_mock_source(paper_json)
        mock_mcp_cls.return_value = mock_ctx

        hub_genes = self._make_hub_genes({"GENE_A": 50, "GENE_B": 30, "GENE_C": 20, "GENE_D": 10})

        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_hub_genes
        result = fetch_abstracts_for_hub_genes(hub_genes, max_hub_genes=2)

        assert "GENE_A" in result
        assert "GENE_B" in result
        assert "GENE_C" not in result
        assert "GENE_D" not in result

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_builds_query_from_gene_and_top_theme(self, mock_mcp_cls):
        """Query should be '{gene} {top_theme_name}'."""
        import json

        paper_json = json.dumps([])
        mock_ctx, mock_tool = self._make_mock_source(paper_json)
        mock_mcp_cls.return_value = mock_ctx

        hub_genes = {"IL6": {"theme_count": 10, "themes": ["inflammatory response", "immune signaling"]}}

        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_hub_genes
        fetch_abstracts_for_hub_genes(hub_genes, max_hub_genes=5)

        call_args = mock_tool.handler.call_args[0][0]
        assert "IL6" in call_args["keywords"]
        assert "inflammatory response" in call_args["keywords"]

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_graceful_degradation_session_failure(self, mock_mcp_cls):
        """Session-level MCP failure → all genes get empty lists, no crash."""
        mock_mcp_cls.side_effect = Exception("MCP connection refused")

        hub_genes = self._make_hub_genes({"IL6": 10, "TNF": 8})

        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_hub_genes
        result = fetch_abstracts_for_hub_genes(hub_genes)

        assert result == {"IL6": [], "TNF": []}

    @patch("goa_semantic_tools.services.artl_literature_service.MCPToolSource")
    def test_graceful_degradation_per_gene_failure(self, mock_mcp_cls):
        """Per-gene tool failure → that gene gets empty list, others continue."""
        import json

        paper_json = json.dumps([{"pmid": "22222", "title": "Good paper", "abstractText": "Abstract"}])

        mock_tool = MagicMock()
        mock_tool.name = "search_europepmc_papers"
        # First call raises, second succeeds
        mock_tool.handler.side_effect = [Exception("Timeout"), paper_json]

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_mcp_cls.return_value = mock_ctx

        hub_genes = {"IL6": {"theme_count": 10, "themes": ["theme1"]},
                     "TNF": {"theme_count": 8, "themes": ["theme2"]}}

        from goa_semantic_tools.services.artl_literature_service import fetch_abstracts_for_hub_genes
        result = fetch_abstracts_for_hub_genes(hub_genes)

        assert result["IL6"] == []
        assert len(result["TNF"]) > 0
