import io
import pandas as pd


def load_dataset(uploaded_file):
    """Load CSV or Excel data and normalize blank/duplicate column labels."""
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".csv"):
        raw = uploaded_file.getvalue()
        try:
            df = pd.read_csv(io.BytesIO(raw))
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(raw), encoding="latin-1")
    else:
        df = pd.read_excel(uploaded_file)

    if df.empty or df.shape[1] == 0:
        raise ValueError("The uploaded file has no data rows or columns.")

    changed = False
    if df.columns.duplicated().any() or any(not str(c).strip() for c in df.columns):
        seen = {}
        new_cols = []
        for i, col in enumerate(df.columns):
            name = str(col).strip() or f"Unnamed_{i+1}"
            seen[name] = seen.get(name, 0) + 1
            new_cols.append(name if seen[name] == 1 else f"{name}_{seen[name]}")
        df.columns = new_cols
        changed = True
    return df, changed
