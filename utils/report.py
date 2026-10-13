import base64
import html
from datetime import datetime
import pandas as pd

def build_html_report(df, profile, relationships, findings, chart_images):
    """Create a self-contained HTML report with embedded PNG chart images."""
    esc = lambda value: str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    chart_sections = []
    for title, png_bytes, reason in chart_images:
        encoded = base64.b64encode(png_bytes).decode("ascii")
        chart_sections.append(
            f"<section><h3>{esc(title)}</h3><p>{esc(reason)}</p>"
            f'<img style="max-width:100%;height:auto" src="data:image/png;base64,{encoded}"></section>'
        )
    rel_html = relationships.head(25).to_html(index=False, escape=True) if not relationships.empty else "<p>Not enough valid numerical columns for pairwise correlation.</p>"
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Auto Data Analyst Report</title>
<style>
body{{font-family:Arial,sans-serif;max-width:1100px;margin:32px auto;padding:0 18px;color:#222;line-height:1.5}}
h1,h2{{color:#15324b}}table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #ddd;padding:7px;text-align:left}}th{{background:#f1f5f9}}
section{{page-break-inside:avoid;margin:28px 0}}.muted{{color:#666}}
</style></head><body>
<h1>Auto Data Analyst — Automated Report</h1>
<p class="muted">Generated {datetime.now().strftime("%Y-%m-%d %H:%M")} · Rule-based analysis; no AI service used.</p>
<h2>Dataset overview</h2><ul><li>Rows: {len(df):,}</li><li>Columns: {df.shape[1]:,}</li>
<li>Duplicate rows: {int(df.duplicated().sum()):,}</li><li>Missing cells: {int(df.isna().sum().sum()):,}</li></ul>
<h2>Key findings</h2><ul>{''.join('<li>'+esc(item)+'</li>' for item in findings)}</ul>
<h2>Column profile</h2>{profile.to_html(index=False, escape=True)}
<h2>Numerical relationships</h2>{rel_html}
<h2>Automatically selected visualizations</h2>{''.join(chart_sections)}
<p class="muted">Interpret findings in context. Correlation and outlier flags are screening signals, not proof of causation or errors.</p>
</body></html>"""
    return html.encode("utf-8")
