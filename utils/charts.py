import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from analysis.relationships import safe_numeric, get_numeric_relationships

def make_chart(chart_type, data, title, x_label=None, y_label=None):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    try:
        if chart_type == "hist":
            vals = safe_numeric(data).dropna()
            ax.hist(vals, bins="auto", edgecolor="white")
        elif chart_type == "box":
            vals = safe_numeric(data).dropna()
            ax.boxplot(vals, vert=True, showfliers=True)
            ax.set_xticks([1])
            ax.set_xticklabels([str(x_label or "Values")])
        elif chart_type == "bar":
            data.plot(kind="bar", ax=ax)
            ax.tick_params(axis="x", labelrotation=45)
        elif chart_type == "scatter":
            x, y = data
            valid = pd.DataFrame({"x": safe_numeric(x), "y": safe_numeric(y)}).dropna()
            if len(valid) > 5000:
                valid = valid.sample(5000, random_state=42)
            ax.scatter(valid["x"], valid["y"], alpha=0.55, s=18)
        elif chart_type == "line":
            x, y = data
            valid = pd.DataFrame({"x": x, "y": safe_numeric(y)}).dropna()
            valid = valid.sort_values("x")
            if len(valid) > 5000:
                valid = valid.iloc[np.linspace(0, len(valid) - 1, 5000).astype(int)]
            ax.plot(valid["x"].astype(str), valid["y"], marker="o", linewidth=1.5)
            ax.tick_params(axis="x", labelrotation=45)
        elif chart_type == "stacked":
            data.plot(kind="bar", stacked=True, ax=ax)
            ax.tick_params(axis="x", labelrotation=45)
        ax.set_title(title)
        if x_label:
            ax.set_xlabel(str(x_label))
        if y_label:
            ax.set_ylabel(str(y_label))
        fig.tight_layout()
        return fig
    except Exception:
        plt.close(fig)
        raise

def create_visualizations(df, roles, max_charts=12):
    """Select charts from detected data roles and basic data characteristics."""
    charts = []
    numeric_cols = [c for c, r in roles.items() if r == "Numerical"]
    categorical_cols = [c for c, r in roles.items() if r == "Categorical"]
    date_cols = [c for c, r in roles.items() if r == "Date/Time"]

    # Univariate numeric charts: distribution + outlier view.
    for col in numeric_cols:
        values = safe_numeric(df[col]).dropna()
        if len(values) >= 2 and values.nunique() > 1:
            charts.append({
                "title": f"Distribution of {col}",
                "kind": "hist",
                "data": df[col],
                "reason": "Shows the shape and spread of a numerical variable.",
            })
            if len(values) >= 4:
                charts.append({
                    "title": f"Outlier overview: {col}",
                    "kind": "box",
                    "data": df[col],
                    "reason": "Shows the median, spread, and potential outliers.",
                })

    # Categorical frequency charts; cap category count to prevent unreadable charts.
    for col in categorical_cols:
        counts = df[col].astype("string").fillna("(Missing)").value_counts(dropna=False)
        if 2 <= len(counts) <= 20:
            charts.append({
                "title": f"Most frequent values: {col}",
                "kind": "bar",
                "data": counts.head(15),
                "reason": "Compares the frequency of categories with manageable cardinality.",
            })

    # Numeric relationships: top non-redundant candidates by absolute Pearson correlation.
    relationships = get_numeric_relationships(df, numeric_cols)
    if not relationships.empty:
        for _, row in relationships.iterrows():
            c1, c2 = row["Column 1"], row["Column 2"]
            if row["Absolute Correlation"] < 0.25:
                continue
            if len(charts) >= max_charts:
                break
            charts.append({
                "title": f"{c1} vs {c2}",
                "kind": "scatter",
                "data": (df[c1], df[c2]),
                "reason": (
                    f"Pearson correlation {row['Correlation']:.2f} "
                    f"({row['Association']}); association is not proof of causation."
                ),
            })

    # Date/numeric trends: aggregate by date, limiting pair count.
    for date_col in date_cols:
        parsed_dates = pd.to_datetime(df[date_col], errors="coerce")
        if parsed_dates.notna().sum() < 3:
            continue
        for num_col in numeric_cols[:3]:
            trend = pd.DataFrame({
                "date": parsed_dates,
                "value": safe_numeric(df[num_col]),
            }).dropna()
            if len(trend) < 3:
                continue
            trend["period"] = trend["date"].dt.to_period("M").dt.to_timestamp()
            aggregated = trend.groupby("period", as_index=False)["value"].mean()
            if len(aggregated) >= 2:
                charts.append({
                    "title": f"Average {num_col} over time",
                    "kind": "line",
                    "data": (aggregated["period"], aggregated["value"]),
                    "reason": "Shows the monthly mean over a detected date/time column.",
                })
                if len(charts) >= max_charts:
                    break
        if len(charts) >= max_charts:
            break

    # Categorical vs numeric group comparisons: choose modest-cardinality categories.
    for cat_col in categorical_cols:
        counts = df[cat_col].nunique(dropna=True)
        if not (2 <= counts <= 12):
            continue
        for num_col in numeric_cols[:3]:
            grouped = pd.DataFrame({
                "group": df[cat_col].astype("string").fillna("(Missing)"),
                "value": safe_numeric(df[num_col]),
            }).dropna(subset=["value"])
            means = grouped.groupby("group")["value"].mean().sort_values(ascending=False)
            if 2 <= len(means) <= 12:
                charts.append({
                    "title": f"Mean {num_col} by {cat_col}",
                    "kind": "bar",
                    "data": means,
                    "reason": "Compares group means; group sizes and context should be considered.",
                })
            if len(charts) >= max_charts:
                break
        if len(charts) >= max_charts:
            break

    # Categorical pair: normalized crosstab for a compact association overview.
    for i, col1 in enumerate(categorical_cols):
        found = False
        for col2 in categorical_cols[i + 1:]:
            if 2 <= df[col1].nunique(dropna=True) <= 8 and 2 <= df[col2].nunique(dropna=True) <= 8:
                ct = pd.crosstab(
                    df[col1].astype("string").fillna("(Missing)"),
                    df[col2].astype("string").fillna("(Missing)"),
                    normalize="index",
                )
                charts.append({
                    "title": f"Category proportions: {col1} by {col2}",
                    "kind": "stacked",
                    "data": ct,
                    "reason": "Compares within-row category proportions.",
                })
                found = True
                break
        if found or len(charts) >= max_charts:
            break

    return charts[:max_charts]
