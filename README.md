# Auto Data Analyst

A lightweight, rule-based Streamlit app that profiles structured datasets, detects column roles, explores numerical relationships, screens for potential outliers, chooses visualizations, and exports a self-contained HTML report.

## Project structure

- `app.py` — application entry point and page composition
- `components/` — reusable dashboard UI: styles, header, sidebar
- `analysis/` — column-role detection, profiling, relationships, and findings
- `utils/` — data loading, chart generation, and HTML report export
- `tests/` — tests for reusable analysis functions

## Setup (Windows)

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Supported files

- CSV
- Excel `.xlsx`
- Excel `.xls`

## Design principles

- No external AI API or API key is required.
- Analysis uses general data characteristics rather than assuming one business domain.
- Correlations and IQR outlier flags are exploratory signals, not proof of causation or data errors.

## Limitations

This is an early-stage prototype. Validate outputs against the context and meaning of your dataset, especially for date parsing, identifier-like columns, and small samples.
