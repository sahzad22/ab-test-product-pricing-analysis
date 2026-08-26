from pathlib import Path
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "pricing_experiment.csv")

summary = df.groupby("variant").agg(
    visitors=("user_id", "count"),
    conversions=("converted", "sum"),
    revenue=("revenue", "sum"),
    revenue_per_visitor=("revenue", "mean")
)
summary["conversion_rate"] = summary["conversions"] / summary["visitors"]

p_a = summary.loc["Control", "conversion_rate"]
p_b = summary.loc["Treatment", "conversion_rate"]
n_a = summary.loc["Control", "visitors"]
n_b = summary.loc["Treatment", "visitors"]

lift_abs = p_b - p_a
lift_rel = lift_abs / p_a
pooled = (summary.loc["Control", "conversions"] + summary.loc["Treatment", "conversions"]) / (n_a + n_b)
se_null = (pooled * (1-pooled) * (1/n_a + 1/n_b)) ** 0.5
z = lift_abs / se_null
p_value = 2 * norm.sf(abs(z))
se_diff = (p_a*(1-p_a)/n_a + p_b*(1-p_b)/n_b) ** 0.5
margin = norm.ppf(0.975) * se_diff
ci_low, ci_high = lift_abs - margin, lift_abs + margin

print("=== EXPERIMENT SUMMARY ===")
print(summary.round(4))
print(f"Absolute conversion lift: {lift_abs:.2%}")
print(f"Relative conversion lift: {lift_rel:.2%}")
print(f"95% CI: [{ci_low:.2%}, {ci_high:.2%}]")
print(f"z-statistic: {z:.3f}")
print(f"p-value: {p_value:.6g}")

rpa_a = summary.loc["Control", "revenue_per_visitor"]
rpa_b = summary.loc["Treatment", "revenue_per_visitor"]
print(f"Revenue / visitor — Control: ₹{rpa_a:.2f}")
print(f"Revenue / visitor — Treatment: ₹{rpa_b:.2f}")

if p_value < 0.05 and rpa_b > rpa_a:
    recommendation = "LAUNCH: Treatment improves conversion and revenue per visitor."
elif p_value < 0.05:
    recommendation = "HOLD: Conversion improves, but revenue per visitor declines."
else:
    recommendation = "DO NOT LAUNCH YET: Evidence is not statistically conclusive."
print(f"Recommendation: {recommendation}")

segment = df.groupby(["device", "variant"]).agg(visitors=("user_id","count"), conversions=("converted","sum")).reset_index()
segment["conversion_rate"] = segment["conversions"] / segment["visitors"]
analysis = ROOT / "analysis"
analysis.mkdir(exist_ok=True)
summary.reset_index().to_csv(analysis / "variant_summary.csv", index=False)
segment.to_csv(analysis / "segment_results.csv", index=False)
