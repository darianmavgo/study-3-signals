ALTER TABLE daily_returns_spxl ADD COLUMN bucket REAL;
UPDATE daily_returns_spxl
SET bucket = CASE
  WHEN percent_change / 100 >= 0 THEN
    CASE WHEN percent_change / 100 >= 1.0 THEN 0.95
    ELSE FLOOR((percent_change / 100) / 0.1) * 0.1 + 0.05 END
  WHEN percent_change / 100 < 0 THEN
    CASE WHEN percent_change / 100 <= -1.0 THEN -0.95
    ELSE CEIL((percent_change / 100) / 0.1) * 0.1 - 0.05 END
END; 