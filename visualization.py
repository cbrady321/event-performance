import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_results(experiment_results: pd.DataFrame):
    plt.figure(figsize=(12, 8))

    # Scatter plot of weighted percentage change vs correlation score
    sns.scatterplot(data=experiment_results, x='weighted_percentage_change', y='correlation_score', hue='index_name')
    plt.title('Weighted Percentage Change vs Correlation Score')
    plt.xlabel('Weighted Percentage Change')
    plt.ylabel('Correlation Score')
    plt.legend(title='Index Name')
    plt.grid(True)
    plt.show()

    # Bar plot of average correlation score by index
    avg_correlation = experiment_results.groupby('index_name')['correlation_score'].mean().reset_index()
    sns.barplot(data=avg_correlation, x='index_name', y='correlation_score')
    plt.title('Average Correlation Score by Index')
    plt.xlabel('Index Name')
    plt.ylabel('Average Correlation Score')
    plt.show()

