import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from typing import List, Tuple

def determine_performance(events: pd.DataFrame, stock_history: pd.DataFrame, index_history: pd.DataFrame) -> pd.DataFrame:
    performance_data = []

    for _, event in events.iterrows():
        index_name = event['index_name']
        start_date = event['start_date']
        end_date = event['end_date']

        # Filter index history for the event
        index_data = index_history[(index_history['index_name'] == index_name) &
                                   (index_history['date'].between(start_date, end_date))]
        index_pct_change = (index_data['price'].iloc[-1] - index_data['price'].iloc[0]) / index_data['price'].iloc[0]

        # Filter stock history for the event
        stock_data = stock_history[stock_history['date'].between(start_date, end_date)]
        stock_pct_changes = stock_data.groupby('stock_name')['price'].apply(
            lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]
        ).reset_index()

        # Compute weighted percentage change
        stock_pct_changes['weighted_percentage_change'] = stock_pct_changes['price'] / abs(index_pct_change)

        # Append to performance data
        for _, stock in stock_pct_changes.iterrows():
            performance_data.append([
                index_name, start_date, end_date, stock['stock_name'], stock['price'], stock['weighted_percentage_change']
            ])

    return pd.DataFrame(performance_data, columns=[
        'index_name', 'start_date', 'end_date', 'stock_name', 'percentage_change', 'weighted_percentage_change'
    ])

def find_high_performers(performance_table: pd.DataFrame, index_names: List[str], stocks_per_event: int) -> pd.DataFrame:
    filtered_performance_table = pd.DataFrame()

    for index_name in index_names:
        index_performance = performance_table[performance_table['index_name'] == index_name]
        top_stocks = index_performance.nlargest(stocks_per_event, 'weighted_percentage_change')
        filtered_performance_table = pd.concat([filtered_performance_table, top_stocks])

    return filtered_performance_table

def find_correlations(filtered_performance_table: pd.DataFrame, stock_history: pd.DataFrame,
                      index_history: pd.DataFrame, experiment_date_range: Tuple[str, str]) -> pd.DataFrame:
    experiment_results = filtered_performance_table.copy()
    correlation_scores = []

    for _, row in experiment_results.iterrows():
        stock_name = row['stock_name']
        index_name = row['index_name']

        # Filter stock and index history for the experiment date range
        stock_data = stock_history[(stock_history['stock_name'] == stock_name) &
                                   (stock_history['date'].between(*experiment_date_range))]
        index_data = index_history[(index_history['index_name'] == index_name) &
                                   (index_history['date'].between(*experiment_date_range))]

        # Merge on date to ensure alignment
        merged_data = pd.merge(stock_data, index_data, on='date', suffixes=('_stock', '_index'))

        if merged_data.empty:
            print(f"Warning: No overlapping data for {stock_name} and {index_name} in the given date range.")
            correlation_scores.append(np.nan)
            continue

        # Compute correlation
        correlation = r2_score(merged_data['price_stock'], merged_data['price_index'])
        correlation_scores.append(correlation)

    experiment_results['correlation_score'] = correlation_scores
    return experiment_results
