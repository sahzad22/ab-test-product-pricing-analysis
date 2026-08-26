from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "pricing_experiment.csv"


def test_experiment_dataset_exists():
    assert DATA.exists()


def test_experiment_schema_and_size():
    df = pd.read_csv(DATA)
    assert len(df) == 30_000
    assert {"user_id", "device", "country", "variant", "converted", "price", "revenue"}.issubset(df.columns)


def test_assignment_and_metrics_are_valid():
    df = pd.read_csv(DATA)
    assert df["user_id"].is_unique
    assert set(df["variant"].unique()) == {"Control", "Treatment"}
    assert set(df["price"].unique()) == {899, 999}
    assert df["converted"].isin([0, 1]).all()
    assert (df["revenue"] >= 0).all()
