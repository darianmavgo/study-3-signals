
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
