# LLM Schema Debug Findings

## Context
- Phase 1 (GO enrichment) completes successfully.
- Phase 2 (LLM explanations) fails with OpenAI structured output schema validation.

## Error Trace (Key Point)
- OpenAI error:
  - `Invalid schema for response_format 'DynamicModel': In context=('properties', 'enrichment_data'), 'additionalProperties' is required to be supplied and to be false.`
- After simplifying the response schema:
  - `Invalid schema for response_format 'DynamicModel': In context=('properties', 'explanations', 'items'), schema must have a 'type' key.`

## Current Response Schema (Simplified)
- File: `src/goa_semantic_tools/goa_semantic_tools/schemas/go_explanation_output.schema.json`
- Top-level fields: `explanations`, `overall_summary`.
- `explanations.items` includes `type: object` and properties `root_term`, `explanation`.

## Observations
- The schema on disk appears to include `type` for `explanations.items`.
- OpenAI still reports missing `type`, suggesting one of:
  1) A different schema is being loaded at runtime.
  2) The schema is transformed/dropped by the client before being sent.
  3) OpenAI strict validator expects a different structure (e.g., `$defs` + `$ref`).

## Minimal Next Steps (No Code Changes Yet)
1) Verify the exact schema sent to OpenAI by dumping `explanation_schema["properties"]["explanations"]["items"]` just before `agent.query_unified(...)`.
2) If the schema is correct on load, refactor to `$defs`/`$ref` to satisfy OpenAI strict schema validation.
3) Alternative: switch to Anthropic tool-schema mode or disable strict response_format (if supported by the client).

## Related Files
- Schema: `src/goa_semantic_tools/goa_semantic_tools/schemas/go_explanation_output.schema.json`
- Prompt: `src/goa_semantic_tools/goa_semantic_tools/services/go_explanation.prompt.yaml`
- LLM call: `src/goa_semantic_tools/goa_semantic_tools/services/go_explanation_service.py`
- CLI error handling: `src/goa_semantic_tools/goa_semantic_tools/cli.py`
