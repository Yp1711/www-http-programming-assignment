import pandas as pd
import matplotlib.pyplot as plt

def plot_daily(file_path):


    data = pd.read_csv(file_path)

    # data['Date'] = pd.to_datetime(data['Date'])
    result = data.groupby('Date')['Count'].max().reset_index()
    merged_data = pd.merge(data, result, on=['Date', 'Count'], how='inner')
    dates = merged_data['Date'].unique()
    counts = merged_data['Count'].tolist()

  
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6)) 
    ax1.bar(dates, counts)
    for i in range(len(merged_data)):
        ax1.text(dates[i], counts[i], merged_data['Server_IP'][i], ha='center', va='bottom')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Count')
    ax1.set_title('Website with the Highest Count on Each Day')
    ax1.set_xticks(dates)
    ax1.set_xticklabels(dates,rotation=45)

    print()
    ax2.plot(data['Date'].drop_duplicates().tolist(),data.groupby('Date')['Count'].sum())
    ax2.set_title('Daily Count')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Visit Count')
    ax2.set_xticks(data['Date'].drop_duplicates().tolist())
    ax2.set_xticklabels(data['Date'].drop_duplicates().tolist(),rotation=45)

    plt.tight_layout()
    plt.savefig('daily_chart.png')


if __name__ == '__main__':

    file_path = 'web_usage_data.csv'
    plot_daily(file_path)
