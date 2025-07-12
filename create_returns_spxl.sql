DROP TABLE IF EXISTS daily_returns_spxl;
CREATE TABLE daily_returns_spxl AS
WITH lagged AS (
  SELECT 
    Date,
    ("('High', 'SPXL')" - LAG("('Close', 'SPXL')") OVER (ORDER BY Date)) / LAG("('Close', 'SPXL')") OVER (ORDER BY Date) * 100 AS percent_change,
    LAG("('Close', 'SPXL')") OVER (ORDER BY Date) AS prev_close
  FROM SPXL
)
SELECT 
  Date,
  percent_change,
  cast(percent_change * 10 AS int) AS bucket
FROM lagged
WHERE prev_close IS NOT NULL
ORDER BY Date; 