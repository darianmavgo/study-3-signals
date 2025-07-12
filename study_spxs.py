import yfinance as yf
import pandas as pd
import sqlite3
from sklearn.tree import DecisionTreeClassifier, export_text

# Define tickers and dates
tickers = ['BAR', 'SPY', 'BND', 'SPXS']
start_date = '2021-01-01'
end_date = '2025-07-10'

# Create DB
conn = sqlite3.connect('stock_data.db')

# Fetch data
data = {}
for ticker in tickers:
    loaded = False
    try:
        df = pd.read_sql(f'SELECT * FROM {ticker}', conn, index_col='Date', parse_dates=['Date'])
        if not df.empty and ('Adj Close' in df.columns or 'Close' in df.columns):
            data[ticker] = df
            loaded = True
    except:
        pass
    if not loaded:
        data[ticker] = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
        data[ticker].to_sql(ticker, conn, if_exists='replace')

# Compute daily returns
closes_list = []
for ticker in tickers:
    df_t = data[ticker]
    if 'Adj Close' in df_t.columns:
        s = df_t['Adj Close']
    elif 'Close' in df_t.columns:
        s = df_t['Close']
    else:
        raise ValueError(f'No closing price column for {ticker}')
    s.name = ticker
    closes_list.append(s)
closes = pd.concat(closes_list, axis=1)
returns = closes.pct_change()
df = returns.dropna()

# Target: next day SPXS return >= 0.05
df['next_spxs_return'] = df['SPXS'].shift(-1)
df['target'] = (df['next_spxs_return'] >= 0.05).astype(int)
df = df.dropna()  # remove last row

# Features: BAR, SPY, BND returns
X = df[['BAR', 'SPY', 'BND']]
y = df['target']

# Fit decision tree
dt = DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, class_weight='balanced')
dt.fit(X, y)

# Get probabilities
probs = dt.predict_proba(X)
proba = [p[1] for p in probs]
df['proba'] = proba

# Find days with >=0.9 prob
high_conf_df = df.loc[df['proba'] >= 0.9, ['next_spxs_return', 'proba', 'BAR', 'SPY', 'BND']]
high_conf_df.reset_index().to_sql('high_confidence_days_spxs', conn, if_exists='replace')

# Generate README_SPXS
tree_text = export_text(dt, feature_names=['BAR', 'SPY', 'BND'])
readme = f"""
# Study of 3 Signals: BAR, SPY, BND to Predict SPXS Movement

This study uses historical data from {start_date} to {end_date} for tickers BAR, SPY, BND, SPXS.

A decision tree was trained on daily returns to predict if SPXS will increase by 5% or more the next day.

The patterns leading to 90% confidence are based on the decision tree rules where leaf nodes have >=90% probability for positive prediction.

Decision Tree Structure:

```
{tree_text}
```

The high confidence days are stored in the database table 'high_confidence_days_spxs' with columns for date (index), next_spxs_return, proba, and the signal returns (BAR, SPY, BND).
"""
with open('README_SPXS.md', 'w') as f:
    f.write(readme)

conn.close() 