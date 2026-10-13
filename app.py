import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from analysis.roles import infer_roles
from analysis.profiling import profile_dataset
from analysis.relationships import safe_numeric, get_numeric_relationships, detect_outliers_iqr
from analysis.insights import generate_findings
from utils.charts import make_chart, create_visualizations
from utils.report import build_html_report
from utils.data_loader import load_dataset
from components.styles import apply_styles
from components.header import render_header, render_footer
from components.sidebar import render_sidebar


st.set_page_config(page_title="Auto Data Analyst", page_icon="📊", layout="wide")

apply_styles()

render_header()

uploaded_file, max_charts = render_sidebar()

if uploaded_file is None:
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("### Welcome to your analysis workspace")
        st.write("Upload a dataset from the sidebar to automatically inspect data quality, explore relationships, detect potential outliers, and generate charts.")
        st.markdown("""
        <div class="ada-insight"><b>01 · Understand</b><br>Rows, columns, missing values, duplicates, and inferred column roles.</div>
        <div class="ada-insight"><b>02 · Explore</b><br>Statistical associations, distributions, category comparisons, and trends when supported by the data.</div>
        <div class="ada-insight"><b>03 · Share</b><br>Download a self-contained HTML report with findings and embedded visualizations.</div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("### What you can upload")
        st.info("CSV files and Excel workbooks (.xlsx, .xls)")
        st.markdown("**Works with many kinds of structured data**")
        st.write("Sales · HR · Finance · Operations · Education · Marketing · Customer data · and more")
        st.caption("These are examples, not hard-coded analysis categories.")
    st.markdown('<div class="ada-footer">Auto Data Analyst · Local, rule-based analysis · No external AI API</div>', unsafe_allow_html=True)
    st.stop()

try:
    df, columns_renamed = load_dataset(uploaded_file)
    if columns_renamed:
        st.warning("Duplicate or blank column labels were made unique internally for reliable analysis.")

    empty_rows = int(df.isna().all(axis=1).sum())
    empty_cols = int(df.isna().all(axis=0).sum())
    if empty_rows or empty_cols:
        st.info(f"Detected {empty_rows} fully empty rows and {empty_cols} fully empty columns. They remain in the analysis.")

    roles = infer_roles(df)
    profile = profile_dataset(df, roles)
    numeric_cols = [c for c, r in roles.items() if r == "Numerical"]
    categorical_cols = [c for c, r in roles.items() if r == "Categorical"]
    date_cols = [c for c, r in roles.items() if r == "Date/Time"]
    relationships = get_numeric_relationships(df, numeric_cols)
    findings = generate_findings(df, roles, profile, relationships)
    charts = create_visualizations(df, roles, max_charts=max_charts)

    st.markdown(f"**Loaded:** `{uploaded_file.name}` &nbsp; · &nbsp; **Analysis ready**", unsafe_allow_html=True)
    a, b, c, d = st.columns(4)
    a.metric("Total rows", f"{df.shape[0]:,}")
    b.metric("Total columns", f"{df.shape[1]:,}")
    c.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
    d.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")

    overview_tab, profile_tab, visuals_tab, findings_tab, report_tab = st.tabs([
        "✨ Overview", "🧭 Data Profile", "📈 Visualizations", "💡 Findings", "📄 Report"
    ])

    with overview_tab:
        st.markdown("### Dataset preview")
        st.dataframe(df.head(12), use_container_width=True, hide_index=True)
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown("### Detected column roles")
            role_counts = pd.Series(roles).value_counts().rename_axis("Role").reset_index(name="Columns")
            st.dataframe(role_counts, use_container_width=True, hide_index=True)
            if not role_counts.empty:
                st.bar_chart(role_counts.set_index("Role"))
        with col_b:
            st.markdown("### Data quality snapshot")
            missing_by_col = df.isna().sum().sort_values(ascending=False)
            missing_by_col = missing_by_col[missing_by_col > 0].head(12)
            if missing_by_col.empty:
                st.success("No missing cells detected.")
            else:
                st.bar_chart(missing_by_col)
            duplicate_count = int(df.duplicated().sum())
            if duplicate_count:
                st.warning(f"{duplicate_count:,} fully duplicated rows found.")
            else:
                st.success("No fully duplicated rows found.")

    with profile_tab:
        st.markdown("### Column-level profile")
        st.dataframe(profile, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download column profile (CSV)",
            data=profile.to_csv(index=False).encode("utf-8"),
            file_name="auto_data_analyst_column_profile.csv",
            mime="text/csv",
        )
        st.markdown("### Missingness overview")
        missing_pct = (df.isna().mean() * 100).sort_values(ascending=False)
        missing_pct = missing_pct[missing_pct > 0].head(20)
        if missing_pct.empty:
            st.caption("All columns are complete based on pandas missing-value detection.")
        else:
            st.bar_chart(missing_pct)

    with visuals_tab:
        st.markdown("### Automatically selected charts")
        st.caption("Charts are selected from detected data roles, category counts, available observations, and numerical association.")
        rendered_chart_images = []
        if not charts:
            st.info("No charts met the current selection rules for this dataset.")
        else:
            for index in range(0, len(charts), 2):
                chart_cols = st.columns(2)
                for slot, chart in enumerate(charts[index:index + 2]):
                    with chart_cols[slot]:
                        with st.container(border=True):
                            st.markdown(f"#### {chart['title']}")
                            st.caption(chart["reason"])
                            try:
                                fig = make_chart(
                                    chart["kind"], chart["data"], chart["title"],
                                    x_label=chart.get("x_label"), y_label=chart.get("y_label")
                                )
                                st.pyplot(fig, use_container_width=True)
                                buffer = io.BytesIO()
                                fig.savefig(buffer, format="png", dpi=125, bbox_inches="tight")
                                rendered_chart_images.append((chart["title"], buffer.getvalue(), chart["reason"]))
                                plt.close(fig)
                            except Exception as chart_error:
                                st.warning(f"Chart skipped: {chart_error}")

    with findings_tab:
        st.markdown("### What stands out in this dataset")
        st.caption("These are automatically generated statistical observations. Validate important findings in context.")
        for i, finding in enumerate(findings, start=1):
            st.markdown(f'<div class="ada-insight"><b>Finding {i:02d}</b><br>{finding}</div>', unsafe_allow_html=True)
        st.markdown("### Numerical relationships")
        if len(numeric_cols) >= 2 and not relationships.empty:
            st.dataframe(relationships.head(20), use_container_width=True, hide_index=True)
            st.caption("Pearson correlation captures linear association and can be influenced by outliers. It does not establish causation.")
            with st.expander("View correlation matrix"):
                numeric = pd.DataFrame({c: safe_numeric(df[c]) for c in numeric_cols})
                st.dataframe(numeric.corr().round(3), use_container_width=True)
            with st.expander("View covariance matrix"):
                st.dataframe(numeric.cov().round(3), use_container_width=True)
        else:
            st.info("At least two usable numerical columns are needed for pairwise correlations.")
        st.markdown("### Potential outliers")
        outlier_rows = []
        for col in numeric_cols:
            out = detect_outliers_iqr(df[col])
            outlier_rows.append({
                "Column": str(col),
                "Potential Outliers": out["count"],
                "Outlier %": out["percent"],
                "IQR Lower Bound": out["lower"],
                "IQR Upper Bound": out["upper"],
            })
        if outlier_rows:
            outlier_df = pd.DataFrame(outlier_rows).sort_values("Potential Outliers", ascending=False)
            st.dataframe(outlier_df, use_container_width=True, hide_index=True)
            st.caption("IQR flags are screening signals, not proof that values are errors.")
        else:
            st.info("No columns were classified as numerical.")

    with report_tab:
        st.markdown("### Your analytical report is ready")
        st.write("The HTML report includes the dataset overview, key findings, column profile, numerical relationships, and generated charts.")
        st.download_button(
            "⬇️ Download full analytical report (HTML)",
            data=build_html_report(df, profile, relationships, findings, locals().get("rendered_chart_images", [])),
            file_name="auto_data_analyst_report.html",
            mime="text/html",
            type="primary",
            use_container_width=True,
        )
        if not relationships.empty:
            st.download_button(
                "⬇️ Download numerical relationships (CSV)",
                data=relationships.to_csv(index=False).encode("utf-8"),
                file_name="auto_data_analyst_relationships.csv",
                mime="text/csv",
            )
        st.info("Open the downloaded HTML file in a browser. The report is self-contained, including embedded chart images.")

    st.markdown('<div class="ada-footer">Auto Data Analyst · Rule-based analysis · No external AI API · Interpret statistical flags in context</div>', unsafe_allow_html=True)

except Exception as exc:
    st.error(f"Unable to analyze this dataset: {exc}")
    st.info("Check that the file is a valid CSV/Excel workbook containing tabular data.")
