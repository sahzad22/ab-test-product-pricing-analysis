from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "pricing_experiment.csv")

required = {"user_id", "variant", "device", "converted", "revenue"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

summary = df.groupby("variant").agg(
    visitors=("user_id", "count"),
    conversions=("converted", "sum"),
    revenue=("revenue", "sum"),
    revenue_per_visitor=("revenue", "mean"),
)
summary["conversion_rate"] = summary["conversions"] / summary["visitors"]

p_a = summary.loc["Control", "conversion_rate"]
p_b = summary.loc["Treatment", "conversion_rate"]
n_a = summary.loc["Control", "visitors"]
n_b = summary.loc["Treatment", "visitors"]

lift_abs = p_b - p_a
lift_rel = lift_abs / p_a
pooled = (
    summary.loc["Control", "conversions"]
    + summary.loc["Treatment", "conversions"]
) / (n_a + n_b)
se_null = (pooled * (1 - pooled) * (1 / n_a + 1 / n_b)) ** 0.5
z = lift_abs / se_null
p_value = 2 * norm.sf(abs(z))
se_diff = (p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b) ** 0.5
margin = norm.ppf(0.975) * se_diff
ci_low, ci_high = lift_abs - margin, lift_abs + margin

rpa_a = summary.loc["Control", "revenue_per_visitor"]
rpa_b = summary.loc["Treatment", "revenue_per_visitor"]

if p_value < 0.05 and rpa_b > rpa_a:
    recommendation = "LAUNCH"
elif p_value < 0.05:
    recommendation = "HOLD"
else:
    recommendation = "DO NOT LAUNCH YET"

print("=== EXPERIMENT SUMMARY ===")
print(summary.round(4))
print(f"Absolute conversion lift: {lift_abs:.2%}")
print(f"Relative conversion lift: {lift_rel:.2%}")
print(f"95% CI: [{ci_low:.2%}, {ci_high:.2%}]")
print(f"z-statistic: {z:.3f}")
print(f"p-value: {p_value:.6g}")
print(f"Revenue / visitor — Control: ₹{rpa_a:.2f}")
print(f"Revenue / visitor — Treatment: ₹{rpa_b:.2f}")
print(f"Recommendation: {recommendation}")

segment = (
    df.groupby(["device", "variant"])
    .agg(visitors=("user_id", "count"), conversions=("converted", "sum"))
    .reset_index()
)
segment["conversion_rate"] = segment["conversions"] / segment["visitors"]

analysis = ROOT / "analysis"
analysis.mkdir(exist_ok=True)
summary.reset_index().to_csv(analysis / "variant_summary.csv", index=False)
segment.to_csv(analysis / "segment_results.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 5))
plot_df = summary.reset_index()
ax.bar(plot_df["variant"], plot_df["conversion_rate"] * 100)
ax.set_title("Conversion Rate by Experiment Variant")
ax.set_ylabel("Conversion Rate (%)")
ax.set_xlabel("Variant")
for i, value in enumerate(plot_df["conversion_rate"] * 100):
    ax.text(i, value + 0.05, f"{value:.2f}%", ha="center")
fig.tight_layout()
fig.savefig(analysis / "conversion_rate.png", dpi=180)
plt.close(fig)

metrics = pd.DataFrame([{
    "control_conversion": p_a,
    "treatment_conversion": p_b,
    "absolute_lift": lift_abs,
    "relative_lift": lift_rel,
    "ci_low": ci_low,
    "ci_high": ci_high,
    "z_statistic": z,
    "p_value": p_value,
    "control_revenue_per_visitor": rpa_a,
    "treatment_revenue_per_visitor": rpa_b,
    "recommendation": recommendation,
}])
metrics.to_csv(analysis / "experiment_metrics.csv", index=False)
