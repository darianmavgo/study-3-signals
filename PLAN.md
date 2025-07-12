# Plan for Generating Study of Signals to Predict SPXL Movement

This document outlines the step-by-step process used to create the study analyzing signals from BAR, SPY, and BND to predict if SPXL will increase by 5% or more the next day, with a focus on days having 90% or higher confidence.

## Step 1: Set Up Environment
- Create a `requirements.txt` file listing necessary packages: yfinance, pandas, scikit-learn.
- Install the packages using `pip install -r requirements.txt`.

## Step 2: Fetch Historical Data
- Use yfinance to download daily stock data for tickers BAR, SPY, BND, and SPXL from January 1, 2021, to July 10, 2025 (up to the latest available date).

## Step 3: Create SQLite Database
- Connect to a new SQLite database named `stock_data.db`.
- Store each ticker's historical data as a separate table in the database.

## Step 4: Compute Daily Returns
- Calculate daily percentage changes (returns) for each ticker's closing prices.
- Align the data into a single DataFrame, dropping any rows with missing values.

## Step 5: Prepare Data for Modeling
- Create a target variable indicating whether SPXL's return the next day is >= 5% (1 if true, 0 otherwise).
- Use returns from BAR, SPY, and BND as features.

## Step 6: Train Decision Tree Model
- Fit a DecisionTreeClassifier with max_depth=3, min_samples_leaf=5, and balanced class weights to handle potential class imbalance.
- Compute prediction probabilities for the positive class (SPXL up >=5%).

## Step 7: Identify High-Confidence Days
- Filter days where the model's probability for positive prediction is >= 90%.
- Store these days, along with actual next-day return and signal values, in a new table `high_confidence_days` in the database.

## Step 8: Generate README
- Export the decision tree structure as text.
- Create `README.md` summarizing the study, including the date range, methodology, and tree rules that lead to high-confidence predictions.

## Step 9: Generate PLAN.md
- Create this file to document the entire process for transparency and reproducibility.

This plan ensures a systematic approach to data collection, analysis, and reporting. The script `main.py` automates Steps 2 through 8. 