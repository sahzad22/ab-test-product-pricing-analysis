# A/B Test Analysis: Product Pricing Experiment

> **Python • SQL • Statistics • Product Analytics**

## Executive Summary

This project evaluates a simulated pricing experiment designed to answer a real product question:

> **Does a lower product price improve conversion enough to justify the reduction in revenue per order?**

Users are randomly assigned to **Control (₹999)** or **Treatment (₹899)**. The analysis covers experiment design, SQL aggregation, conversion rate, hypothesis testing, 95% confidence intervals, revenue per visitor, segmentation, and a business recommendation.

## Experiment Design

| Item | Design |
|---|---|
| Population | Eligible product-page visitors |
| Control | ₹999 |
| Treatment | ₹899 |
| Assignment | Random 50/50 split |
| Primary metric | Purchase conversion |
| Secondary metric | Revenue per visitor |
| Test | Two-proportion z-test |
| Confidence level | 95% |

## Analysis Flow

```text
Simulated Visitor Events
        ↓
CSV / SQL
        ↓
Data Quality Checks
        ↓
SQL Aggregation
        ↓
Conversion Rate
        ↓
Hypothesis Test + 95% CI
        ↓
Revenue Impact
        ↓
Business Recommendation
```

## Run It

```bash
pip install -r requirements.txt
python src/generate_experiment.py
python src/analyze_experiment.py
```

The generator creates 30,000 realistic visitor records. The analysis produces variant-level results, confidence intervals, p-value, revenue per visitor and device-level results.

## Product Analyst Thinking

A statistically significant conversion lift is **not automatically a launch decision**. The analysis also evaluates whether the price reduction improves revenue per visitor and whether the effect is consistent across segments.

## Repository Contents

- `src/generate_experiment.py` — experiment data generator
- `src/analyze_experiment.py` — statistical and business analysis
- `sql/experiment_queries.sql` — reusable SQL analysis
- `analysis/variant_summary.csv` — generated experiment summary
- `analysis/segment_results.csv` — device-level analysis
- `docs/BUSINESS_MEMO.md` — decision-oriented recommendation framework

## Resume-ready statement

> Designed and analyzed a simulated product-pricing A/B test using Python and SQL; applied hypothesis testing and confidence intervals to quantify conversion lift and revenue impact, then translated statistical results into a product launch recommendation.
