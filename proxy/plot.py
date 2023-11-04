import subprocess
import matplotlib.pyplot as plt
import webbrowser 
import os

# Run the individual scripts
subprocess.run(["python3", "daily.py"])
subprocess.run(["python3", "weekly.py"])
subprocess.run(["python3", "monthly.py"])

# Load the saved charts
chart1 = plt.imread('daily_chart.png')
chart2 = plt.imread('weekly_chart.png')
chart3 = plt.imread('monthly_chart.png')

# Create a new figure for combining the charts vertically
fig, ax = plt.subplots(3, 1, figsize=(8, 12))

# Plot the individual charts vertically
ax[0].imshow(chart1)
ax[0].set_title('Daily Statistics')
ax[1].imshow(chart2)
ax[1].set_title('Weekly Statistics')
ax[2].imshow(chart3)
ax[2].set_title('Monthly Statistics')

# Hide axis labels and ticks for the subplots
for a in ax:
    a.axis('off')

# Save or display the combined chart
plt.savefig('combined_chart.png')
wants_to_open = input("Do you want to open the plotted image(Y/n):")
if wants_to_open.lower() == 'y':
    webbrowser.open('file://' + os.getcwd()+ '/combined_chart.png' , new=2)
else:
    print("Thanks")
