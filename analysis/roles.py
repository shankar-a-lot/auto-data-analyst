import pandas as pd

def detect_column_role(series):
    """Infer a broad column role from values and dtype, not business names."""
    non_null = series.dropna()

    if non_null.empty:
        return "Empty"

    if pd.api.types.is_bool_dtype(series):
        return "Categorical"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "Date/Time"

    # Treat month-like values as categories instead of parsing them as dates.
    month_names = {
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december",
        "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep",
        "oct", "nov", "dec",
    }
    string_values = non_null.astype(str).str.strip().str.lower()
    month_ratio = string_values.isin(month_names).mean()
    if month_ratio >= 0.8:
        return "Categorical"

    if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
        parsed = pd.to_datetime(non_null, errors="coerce",format ="mixed")
        if len(non_null) >= 3 and parsed.notna().mean() >= 0.9:
            return "Date/Time"

        unique_ratio = non_null.nunique() / len(non_null)
        # Detect identifier-like text from data characteristics only.
        if unique_ratio >= 0.95 and len(non_null) >= 10:
            return "Identifier-like"
        return "Categorical"

    if pd.api.types.is_numeric_dtype(series):
        unique_count = non_null.nunique()
        unique_ratio = unique_count / len(non_null)

        if unique_count <= 2:
            return "Categorical"
        if unique_ratio >= 0.98 and len(non_null) >= 20:
            return "Identifier-like"
        return "Numerical"

    return "Other"

def infer_roles(df):
    return {col: detect_column_role(df[col]) for col in df.columns}
