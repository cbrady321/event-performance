import pandas as pd
from pathlib import Path
from performance import determine_performance, find_high_performers, find_correlations
from visualization import plot_results

# Define paths
DATA_DIR = Path(__file__).parent / 'data'
EXPORT_DIR = Path(__file__).parent / 'export'

# Ensure export directory exists
EXPORT_DIR.mkdir(exist_ok=True)

def main():
    # Load data
    events = pd.read_csv(DATA_DIR / 'events.csv', parse_dates=['start_date', 'end_date'])
    stock_history = pd.read_csv(DATA_DIR / 'stock_history.csv', parse_dates=['date'])
    index_history = pd.read_csv(DATA_DIR / 'index_history.csv', parse_dates=['date'])

    # Determine performance
    performance_table = determine_performance(events, stock_history, index_history)
    performance_table.to_csv(EXPORT_DIR / 'performance_table.csv', index=False)

    # Find high performers
    filtered_performance_table = find_high_performers(performance_table, events['index_name'].unique(), stocks_per_event=1)
    filtered_performance_table.to_csv(EXPORT_DIR / 'filtered_performance_table.csv', index=False)

    # Find correlations
    experiment_date_range = ('2020-01-01', '2021-01-01')
    experiment_results = find_correlations(filtered_performance_table, stock_history, index_history, experiment_date_range)
    experiment_results.to_csv(EXPORT_DIR / 'experiment_results.csv', index=False)

    # Plot results
    plot_results(experiment_results, export_dir=EXPORT_DIR)

if __name__ == "__main__":
    main()
