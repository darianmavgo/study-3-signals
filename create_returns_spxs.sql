DROP TABLE IF EXISTS daily_returns_spxs;
CREATE TABLE daily_returns_spxs AS
WITH lagged AS (
  SELECT 
    Date,
    ("('High', 'SPXS')" - LAG("('Close', 'SPXS')") OVER (ORDER BY Date)) / LAG("('Close', 'SPXS')") OVER (ORDER BY Date) * 100 AS percent_change,
    LAG("('Close', 'SPXS')") OVER (ORDER BY Date) AS prev_close
  FROM SPXS
)
SELECT 
  Date,
  percent_change,
  cast(percent_change * 10 AS int) AS bucket
FROM lagged
WHERE prev_close IS NOT NULL
ORDER BY Date; 