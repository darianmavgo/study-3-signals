DROP VIEW IF EXISTS combined_high_confidence_view;
CREATE VIEW combined_high_confidence_view AS
SELECT Date AS date,
       'SPXL' AS target_ticker,
       next_spxl_return AS next_return,
       proba,
       BAR,
       SPY,
       BND
FROM high_confidence_days_spxl
UNION
SELECT Date AS date,
       'SPXS' AS target_ticker,
       next_spxs_return AS next_return,
       proba,
       BAR,
       SPY,
       BND
FROM all_confidence_days_spxs
WHERE proba > 0.8
ORDER BY date; 