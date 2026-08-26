-- Experiment balance
SELECT variant, COUNT(*) AS visitors, SUM(converted) AS conversions
FROM pricing_experiment
GROUP BY variant;

-- Conversion rate
SELECT variant,
       COUNT(*) AS visitors,
       SUM(converted) AS conversions,
       1.0 * SUM(converted) / COUNT(*) AS conversion_rate
FROM pricing_experiment
GROUP BY variant;

-- Revenue per visitor
SELECT variant,
       SUM(revenue) AS total_revenue,
       AVG(revenue) AS revenue_per_visitor
FROM pricing_experiment
GROUP BY variant;

-- Device-level check
SELECT device, variant, COUNT(*) AS visitors,
       AVG(converted * 1.0) AS conversion_rate
FROM pricing_experiment
GROUP BY device, variant
ORDER BY device, variant;

-- Randomization sanity check
SELECT variant,
       COUNT(DISTINCT user_id) AS unique_users,
       COUNT(*) - COUNT(DISTINCT user_id) AS duplicate_rows
FROM pricing_experiment
GROUP BY variant;
