import numpy as np
import pandas as pd
from pathlib import Path

SEED = 20260827
rng = np.random.default_rng(SEED)
N = 30000

df = pd.DataFrame({
    "user_id": np.arange(1000001, 1000001 + N),
    "device": rng.choice(["Mobile", "Desktop", "Tablet"], N, p=[0.62, 0.32, 0.06]),
    "country": rng.choice(["IN", "US", "UK", "AU"], N, p=[0.62, 0.18, 0.12, 0.08]),
    "variant": rng.choice(["Control", "Treatment"], N, p=[0.5, 0.5]),
})

base = np.where(df["device"].eq("Mobile"), 0.095, 0.125)
base += np.where(df["country"].eq("IN"), 0.005, 0)
treatment_effect = np.where(df["variant"].eq("Treatment"), 0.018, 0)
prob = np.clip(base + treatment_effect, 0.01, 0.50)

df["converted"] = rng.binomial(1, prob)
df["price"] = np.where(df["variant"].eq("Control"), 999, 899)
df["revenue"] = df["converted"] * df["price"]

out = Path(__file__).resolve().parents[1] / "data"
out.mkdir(exist_ok=True)
df.to_csv(out / "pricing_experiment.csv", index=False)
print(f"Generated {len(df):,} experiment rows")
