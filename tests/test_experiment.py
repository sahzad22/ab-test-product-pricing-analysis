from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_generated_dataset_has_expected_shape_and_columns():
    path = ROOT / "data" / "pricing_experiment.csv"
    assert path.exists()
    df = pd.read_csv(path)
    assert len(df) == 30_000
    assert {"user_id", "variant", "converted", "price", "revenue"}.issubset(df.columns)
    assert df["user_id"].is_unique


def test_experiment_has_two_variants_and_valid_values():
    df = pd.read_csv(ROOT / "data" / "pricing_experiment.csv")
    assert set(df["variant"].unique()) == {"Control", "Treatment"}
    assert set(df["price"].unique()) == {899, 999}
    assert df["converted"].isin([0, 1]).all()
    assert (df["revenue"] >= 0).all()
