# Product Pricing Experiment — Business Recommendation Memo

## Decision Question

Does reducing the product price from ₹999 to ₹899 create enough incremental conversion to improve revenue per visitor?

## Decision Framework

1. Statistical significance at α = 0.05
2. Positive and meaningful conversion lift
3. Revenue per visitor does not deteriorate
4. No major segment-level regression

## How to Generate the Recommendation

Run:

```bash
python src/generate_experiment.py
python src/analyze_experiment.py
```

The analysis prints the conversion lift, 95% confidence interval, p-value, revenue per visitor and a launch recommendation.

## Product Analyst Takeaway

The decision should not be based only on whether `p < 0.05`. The analyst should connect the experiment result to unit economics and customer behavior, then monitor conversion, revenue, refunds/cancellations and segment performance after rollout.
