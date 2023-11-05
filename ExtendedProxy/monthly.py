import pandas as pd
import matplotlib.pyplot as plt

def plot_montly(file_path):


    data = pd.read_csv(file_path)

    monthly_unique_users = data.groupby('Month')['Client_IP'].nunique()

    # Define a mapping of month numbers to month names
    month_names = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

    # Create a pie chart
    fig = plt.figure(figsize=(8, 8))
    plt.pie(monthly_unique_users, labels=[month_names[month] for month in monthly_unique_users.index], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Number of Users per Month',y=1.08)

    plt.savefig('monthly_chart.png')

if __name__ == '__main__':

    file_path = 'web_usage_data.csv'
    plot_montly(file_path)
