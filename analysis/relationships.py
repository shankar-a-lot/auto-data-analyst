import pandas as pd
import numpy as np

def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)

def association_label(value):
    if pd.isna(value):
        return "Not available"
    magnitude = abs(value)
    if magnitude >= 0.7:
        strength = "strong"
    elif magnitude >= 0.4:
        strength = "moderate"
    elif magnitude >= 0.2:
        strength = "weak"
    else:
        strength = "very weak"
    direction = "positive" if value > 0 else "negative" if value < 0 else "none"
    return f"{strength} {direction}"

def get_numeric_relationships(df, numeric_cols):
    if len(numeric_cols) < 2:
        return pd.DataFrame()
    numeric = pd.DataFrame({c: safe_numeric(df[c]) for c in numeric_cols})
    corr = numeric.corr(method="pearson")
    rows = []
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i + 1:]:
            value = corr.loc[col1, col2]
            if pd.isna(value):
                continue
            pair = numeric[[col1, col2]].dropna()
            rows.append({
                "Column 1": str(col1),
                "Column 2": str(col2),
                "Correlation": round(float(value), 4),
                "Absolute Correlation": round(abs(float(value)), 4),
                "Association": association_label(float(value)),
                "Complete Pairs": int(len(pair)),
            })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(
        ["Absolute Correlation", "Complete Pairs"], ascending=[False, False]
    ).reset_index(drop=True)

def detect_outliers_iqr(series):
    values = safe_numeric(series).dropna()
    if len(values) < 4 or values.nunique() < 2:
        return {"count": 0, "percent": 0.0, "lower": None, "upper": None}
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    if pd.isna(iqr) or iqr == 0:
        return {"count": 0, "percent": 0.0, "lower": None, "upper": None}
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    count = int(((values < lower) | (values > upper)).sum())
    return {
        "count": count,
        "percent": round(count / len(values) * 100, 2),
        "lower": float(lower),
        "upper": float(upper),
    }
