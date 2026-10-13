import pandas as pd

def profile_dataset(df, roles):
    rows = []
    for col in df.columns:
        s = df[col]
        non_null = s.dropna()
        rows.append({
            "Column": str(col),
            "Data Type": str(s.dtype),
            "Detected Role": roles[col],
            "Non-null Values": int(s.notna().sum()),
            "Missing Values": int(s.isna().sum()),
            "Missing %": round(float(s.isna().mean() * 100), 2),
            "Unique Values": int(s.nunique(dropna=True)),
            "Unique % of Non-null": round(
                float(non_null.nunique() / len(non_null) * 100), 2
            ) if len(non_null) else 0.0,
        })
    return pd.DataFrame(rows)
