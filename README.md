
# Study of 3 Signals: BAR, SPY, BND to Predict SPXL Movement

This study uses historical data from 2021-01-01 to 2025-07-10 for tickers BAR, SPY, BND, SPXL.

A decision tree was trained on daily returns to predict if SPXL will increase by 5% or more the next day.

The patterns leading to 90% confidence are based on the decision tree rules where leaf nodes have >=90% probability for positive prediction.

Decision Tree Structure:

```
|--- SPY <= -0.00
|   |--- BAR <= 0.02
|   |   |--- BND <= -0.00
|   |   |   |--- class: 1
|   |   |--- BND >  -0.00
|   |   |   |--- class: 0
|   |--- BAR >  0.02
|   |   |--- BND <= 0.01
|   |   |   |--- class: 1
|   |   |--- BND >  0.01
|   |   |   |--- class: 0
|--- SPY >  -0.00
|   |--- BAR <= -0.01
|   |   |--- BND <= -0.00
|   |   |   |--- class: 0
|   |   |--- BND >  -0.00
|   |   |   |--- class: 1
|   |--- BAR >  -0.01
|   |   |--- SPY <= 0.02
|   |   |   |--- class: 0
|   |   |--- SPY >  0.02
|   |   |   |--- class: 1

```

The high confidence days are stored in the database table 'high_confidence_days' with columns for date (index), next_spxl_return, proba, and the signal returns (BAR, SPY, BND).

## Table Field Descriptions

### Ticker History Tables (BAR, SPY, BND, SPXL, SPXS)
- Date: Trading date
- Adj Close: Adjusted closing price
- Close: Closing price
- High: Highest price
- Low: Lowest price
- Open: Opening price
- Volume: Trading volume

### Confidence Tables (high_confidence_days, all_confidence_days, high_confidence_days_spxs, all_confidence_days_spxs)
- index: Auto-generated ID
- Date: Trading date
- next_[spxl/spxs]_return: Actual return of target ticker the next day
- proba: Model's predicted probability of >=5% increase
- BAR/SPY/BND: Daily returns of signal tickers

## Decision Tree Summaries

### SPXL Decision Tree
```
|--- SPY <= -0.00
|   |--- BAR <= 0.02
|   |   |--- BND <= -0.00
|   |   |   |--- class: 1
|   |   |--- BND >  -0.00
|   |   |   |--- class: 0
|   |--- BAR >  0.02
|   |   |--- BND <= 0.01
|   |   |   |--- class: 1
|   |   |--- BND >  0.01
|   |   |   |--- class: 0
|--- SPY >  -0.00
|   |--- BAR <= -0.01
|   |   |--- BND <= -0.00
|   |   |   |--- class: 0
|   |   |--- BND >  -0.00
|   |   |   |--- class: 1
|   |--- BAR >  -0.01
|   |   |--- SPY <= 0.02
|   |   |   |--- class: 0
|   |   |--- SPY >  0.02
|   |   |   |--- class: 1
```

### SPXS Decision Tree
```
|--- BAR <= -0.01
|   |--- BAR <= -0.02
|   |   |--- BAR <= -0.02
|   |   |   |--- class: 0
|   |   |--- BAR >  -0.02
|   |   |   |--- class: 1
|   |--- BAR >  -0.02
|   |   |--- BAR <= -0.02
|   |   |   |--- class: 0
|   |   |--- BAR >  -0.02
|   |   |   |--- class: 0
|--- BAR >  -0.01
|   |--- SPY <= -0.00
|   |   |--- SPY <= -0.00
|   |   |   |--- class: 1
|   |   |--- SPY >  -0.00
|   |   |   |--- class: 1
|   |--- SPY >  -0.00
|   |   |--- SPY <= 0.01
|   |   |   |--- class: 0
|   |   |--- SPY >  0.01
|   |   |   |--- class: 1
```

## Overlapping High-Confidence Days
There are no trading days where both SPXL and SPXS had high confidence (>80%) predictions simultaneously.
