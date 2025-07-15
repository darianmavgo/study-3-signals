DROP TABLE IF EXISTS daily_returns_spxl;
CREATE TABLE daily_returns_spxl AS
WITH lagged AS (
  SELECT 
    Date,
    (High - LAG(Close) OVER (ORDER BY Date)) / LAG(Close) OVER (ORDER BY Date) AS percent_change,
    LAG(Close) OVER (ORDER BY Date) AS prev_close,
    High AS high
  FROM SPXL
)
SELECT 
  Date,
  prev_close,
  high,
  percent_change,
  cast(percent_change * 10 AS int) AS bucket
FROM lagged
WHERE prev_close IS NOT NULL
ORDER BY Date; 