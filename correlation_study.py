import pandas as pd
import sqlite3
import scipy.stats
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

conn = sqlite3.connect('stock_data.db')

# Load data
logging.info('Loading SPXL confidence data')
spxl_df = pd.read_sql('SELECT Date, proba AS spxl_proba FROM all_confidence_days_spxl', conn, parse_dates=['Date'])
logging.info('Loading SPXS confidence data')
spxs_df = pd.read_sql('SELECT Date, proba AS spxs_proba FROM all_confidence_days_spxs', conn, parse_dates=['Date'])

# Join on Date
merged_df = pd.merge(spxl_df, spxs_df, on='Date', how='inner')

if merged_df.empty:
    summary = 'No overlapping dates found between SPXL and SPXS confidence data.'
else:
    # Define low and high
    merged_df['low_spxl'] = (merged_df['spxl_proba'] <= 0.2).astype(int)
    merged_df['high_spxs'] = (merged_df['spxs_proba'] >= 0.8).astype(int)
    
    # Count overlaps
    overlap_count = ((merged_df['low_spxl'] == 1) & (merged_df['high_spxs'] == 1)).sum()
    total_days = len(merged_df)
    overlap_pct = (overlap_count / total_days) * 100 if total_days > 0 else 0
    
    # Correlation between inverse SPXL proba and SPXS proba
    corr, pval = scipy.stats.spearmanr(1 - merged_df['spxl_proba'], merged_df['spxs_proba'])
    
    summary = f"""
# Correlation Study: Low Probability Days for SPXL vs High Probability Days for SPXS

Total overlapping days: {total_days}

Days with low SPXL proba (<=0.2) and high SPXS proba (>=0.8): {overlap_count} ({overlap_pct:.2f}%)

Spearman correlation between (1 - SPXL proba) and SPXS proba: {corr:.4f} (p-value: {pval:.4f})

Interpretation: {'Significant' if pval < 0.05 else 'Not significant'} correlation.
"""

with open('README_correlation.md', 'w') as f:
    f.write(summary)

conn.close() 