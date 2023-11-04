import pandas as pd
import matplotlib.pyplot as plt

def plot_weekly(file_path):


    data = pd.read_csv(file_path)

    # Create a figure with two subplots (1 row, 2 columns)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot the stacked bar chart on the first subplot
    grouped = data.groupby(['Week', 'Server_IP'])['Count'].sum().unstack(fill_value=0)
    grouped.plot(kind='bar', stacked=True, ax=axes[0])
    axes[0].set_xlabel('Week')
    axes[0].set_ylabel('Count')
    axes[0].set_title('Stacked Bar Chart of Visits by Server IPs')

    # Plot the box plot on the second subplot
    data.boxplot(column='Count', by='Week', vert=False, ax=axes[1])
    axes[1].set_xlabel('Count')
    axes[1].set_ylabel('Week')
    axes[1].set_title('Box Plot of Visits per Week')
    axes[1].set_title('')

    # Adjust the layout
    plt.tight_layout()

    plt.savefig('weekly_chart.png')


if __name__ == '__main__':

    file_path = 'web_usage_data.csv'
    plot_weekly(file_path)
