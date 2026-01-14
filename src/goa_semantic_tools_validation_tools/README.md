# goa_semantic_tools - Validation Tools

**Status**: OPTIONAL

Validation and analysis tools for comparing runs, computing metrics, and visualizing results.

## Delete This Package If

Your Ring 0 MVP doesn't need:
- Workflow output comparison
- Quality metrics (precision, recall, etc.)
- Visualizations and analysis

See `SCAFFOLD_GUIDE.md` for guidance.

## Installation

```bash
pip install goa_semantic_tools-validation-tools
```

## Structure

- **comparisons/** - Compare workflow outputs across runs
- **metrics/** - Quality metrics (precision, recall, F1, etc.)
- **visualizations/** - Plots, heatmaps, ROC curves

## Usage

This package imports schemas and models from the core package:

```python
from goa_semantic_tools.schemas import load_schema
from goa_semantic_tools_validation_tools.metrics import calculate_f1
from goa_semantic_tools_validation_tools.visualizations import plot_heatmap
```

## Development

This package is part of a UV workspace. See repository root for development instructions.
