import pandas as pd

from analysis.roles import infer_roles
from analysis.profiling import profile_dataset
from analysis.relationships import detect_outliers_iqr, get_numeric_relationships
from analysis.insights import generate_findings


def test_profile_and_roles_work_for_generic_dataset():
    df = pd.DataFrame({
        "amount": [10, 20, 30, 40, 500],
        "segment": ["A", "B", "A", "B", "A"],
    })
    roles = infer_roles(df)
    assert roles["amount"] == "Numerical"
    assert roles["segment"] == "Categorical"
    assert len(profile_dataset(df, roles)) == 2


def test_iqr_outlier_screening_detects_extreme_value():
    result = detect_outliers_iqr(pd.Series([10, 11, 10, 12, 11, 500]))
    assert result["count"] >= 1


def test_numeric_relationships_handles_one_numeric_column():
    df = pd.DataFrame({"amount": [1, 2, 3]})
    result = get_numeric_relationships(df, ["amount"])
    assert result.empty
