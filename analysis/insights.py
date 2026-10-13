import pandas as pd
from analysis.relationships import association_label, detect_outliers_iqr

def generate_findings(df, roles, profile, relationships):
    findings = []
    rows, cols = df.shape
    findings.append(f"The dataset contains {rows:,} rows and {cols:,} columns.")

    missing_total = int(df.isna().sum().sum())
    missing_pct = (missing_total / (rows * cols) * 100) if rows and cols else 0
    findings.append(
        f"There are {missing_total:,} missing cells ({missing_pct:.2f}% of all cells)."
    )

    duplicates = int(df.duplicated().sum())
    if duplicates:
        findings.append(f"{duplicates:,} fully duplicated rows were detected.")
    else:
        findings.append("No fully duplicated rows were detected.")

    if not profile.empty:
        missing_cols = profile[profile["Missing Values"] > 0].sort_values(
            "Missing %", ascending=False
        )
        if not missing_cols.empty:
            r = missing_cols.iloc[0]
            findings.append(
                f"Highest missingness: '{r['Column']}' has {r['Missing %']:.2f}% missing values."
            )

    for col, role in roles.items():
        if role == "Numerical":
            out = detect_outliers_iqr(df[col])
            if out["count"] > 0:
                findings.append(
                    f"'{col}' has {out['count']:,} potential IQR outliers "
                    f"({out['percent']:.2f}% of its non-missing numeric values)."
                )

    if not relationships.empty:
        strong = relationships[relationships["Absolute Correlation"] >= 0.7]
        for _, r in strong.head(3).iterrows():
            findings.append(
                f"Strong {('positive' if r['Correlation'] > 0 else 'negative')} "
                f"linear association between '{r['Column 1']}' and '{r['Column 2']}' "
                f"(Pearson r = {r['Correlation']:.2f}); this does not establish causation."
            )

    return findings
