import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier, export_text

# Define tickers and dates
tickers = ['BAR', 'SPY', 'BND', 'SPXL']
start_date = '2021-01-01'
end_date = '2025-07-10'

# Create DB
conn = sqlite3.connect('stock_data.db')

# Fetch data
data = {}
for ticker in tickers:
    try:
        df = pd.read_sql(f'SELECT * FROM {ticker}', conn, index_col='Date', parse_dates=['Date'])
        if not df.empty:
            data[ticker] = df
            continue
    except:
        pass
    data[ticker] = yf.download(ticker, start=start_date, end=end_date)
    data[ticker].to_sql(ticker, conn, if_exists='replace')

# Compute daily returns
closes_list = []
for ticker in tickers:
    s = data[ticker]['Close']
    s.name = ticker
    closes_list.append(s)
closes = pd.concat(closes_list, axis=1)
returns = closes.pct_change()
df = returns.dropna()

# Target: next day SPXL return >= 0.05
df['next_spxl_return'] = df['SPXL'].shift(-1)
df['target'] = (df['next_spxl_return'] >= 0.05).astype(int)
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
high_conf_df = df.loc[df['proba'] >= 0.9, ['next_spxl_return', 'proba', 'BAR', 'SPY', 'BND']]
high_conf_df.reset_index().to_sql('high_confidence_days', conn, if_exists='replace')

# Store all days with confidence
all_conf_df = df[['next_spxl_return', 'proba', 'BAR', 'SPY', 'BND']]
all_conf_df.reset_index().to_sql('all_confidence_days', conn, if_exists='replace')

# Generate study.html and monthly reports
import os

# Query high confidence days
high_df = pd.read_sql('SELECT * FROM high_confidence_days', conn, parse_dates=['index'])
if 'index' in high_df.columns:
    high_df = high_df.set_index('index')
if not high_df.empty:
    # Group by month
    high_df['month'] = high_df.index.map(lambda x: x.to_period('M'))
    months = high_df['month'].unique()
    months = sorted(months)
    
    # Create monthly HTML files
    for month in months:
        month_df = high_df[high_df['month'] == month].drop('month', axis=1)
        month_str = str(month)
        month_html = f'{month_str}.html'
        month_df.to_html(month_html, escape=False)
    
    # Create study.html
    links = '\n'.join([f'<li><a href="{str(m)}.html">{m}</a></li>' for m in months])
    html_content = f"""
    <html>
    <head><title>High Confidence Trading Months</title></head>
    <body>
    <h1>Months with 90% Confidence Days for SPXL +5% Move</h1>
    <ul>
    {links}
    </ul>
    </body>
    </html>
    """
    with open('study.html', 'w') as f:
        f.write(html_content)
else:
    with open('study.html', 'w') as f:
        f.write('<html><body><h1>No high confidence days found.</h1></body></html>')

# Generate README
tree_text = export_text(dt, feature_names=['BAR', 'SPY', 'BND'])
readme = f"""
# Study of 3 Signals: BAR, SPY, BND to Predict SPXL Movement

This study uses historical data from {start_date} to {end_date} for tickers BAR, SPY, BND, SPXL.

A decision tree was trained on daily returns to predict if SPXL will increase by 5% or more the next day.

The patterns leading to 90% confidence are based on the decision tree rules where leaf nodes have >=90% probability for positive prediction.

Decision Tree Structure:

```
{tree_text}
```

The high confidence days are stored in the database table 'high_confidence_days' with columns for date (index), next_spxl_return, proba, and the signal returns (BAR, SPY, BND).
"""
with open('README.md', 'w') as f:
    f.write(readme)

conn.close() 