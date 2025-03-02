# Createing a torando plot in python
# Nikolai P. Ponomarev

# Run it in google.colab
# You need to have your .csv file ready 
# with appropriate
# column and row names.


import matplotlib.pyplot as plt
import pandas as pd
import os
from google.colab import files

# Upload the file
uploaded = files.upload()

# Read the uploaded file
data = pd.read_csv(list(uploaded.keys())[0])

# Extract columns
parameters = data["Parameter"]
msp_50 = data["50% on MSP (kEUR/t)"]
msp_no_effect = data["No effect on MSP (kEUR/t)"]
msp_150 = data["150% on MSP (kEUR/t)"]

# Calculate the differences from the central point (No effect on MSP)
low = msp_no_effect - msp_50
high = msp_150 - msp_no_effect

# Calculate the percentage of "dmin" and "dmax" effect
dmin = ((msp_50 - msp_no_effect) / msp_no_effect) * 100
dmax = ((msp_150 - msp_no_effect) / msp_no_effect) * 100

# Create a DataFrame
df = pd.DataFrame({
    "Parameter": parameters,
    "50% on MSP": msp_50,
    "No effect on MSP": msp_no_effect,
    "150% on MSP": msp_150,
    "Low": low,
    "High": high,
    "dmin": dmin,
    "dmax": dmax
})

# Sort the DataFrame by "dmin" in ascending order
df = df.sort_values(by="dmin", key=abs)

# Plotting the tornado plot
fig, ax = plt.subplots(figsize=(9/2.54, 9/2.54), dpi=300)  # Convert cm to inches for figsize

# Plot bars for each parameter
for i in range(len(df)):
    ax.barh(df["Parameter"].iloc[i], df["High"].iloc[i], left=df["No effect on MSP"].iloc[i], color='green', edgecolor='black', label='+50%' if i == 0 else "")
    ax.barh(df["Parameter"].iloc[i], -df["Low"].iloc[i], left=df["No effect on MSP"].iloc[i], color='red', edgecolor='black', label='-50%' if i == 0 else "")
    
    # Add text annotations for dmin and dmax values centered on the bars for parameters after any "Parameter"
    if i > df[df['Parameter'] == 'EC'].index[0]:
        ax.text(df["No effect on MSP"].iloc[i] + df["High"].iloc[i] / 2, i, f'{df["dmax"].iloc[i]:.0f}%', va='center', ha='center', color='black', fontsize=6)
        ax.text(df["No effect on MSP"].iloc[i] - df["Low"].iloc[i] / 2, i, f'{df["dmin"].iloc[i]:.0f}%', va='center', ha='center', color='black', fontsize=6)
    else:
        # Add text annotations for dmin and dmax values on the left and right side of the bars for parameters before or equal to "IRR (%)"
        ax.text(df["No effect on MSP"].iloc[i] + df["High"].iloc[i] + 0.1, i, f'{df["dmax"].iloc[i]:.1f}%', va='center', ha='left', color='black', fontsize=6)
        ax.text(df["No effect on MSP"].iloc[i] - df["Low"].iloc[i] - 0.1, i, f'{df["dmin"].iloc[i]:.1f}%', va='center', ha='right', color='black', fontsize=6)

# Add a vertical line at the central point for each parameter
for i in range(len(df)):
    ax.axvline(x=df["No effect on MSP"].iloc[i], color='black', linewidth=1, linestyle='--')

# Set labels and title with increased font size
ax.set_xlabel('Effect on MSP (kEUR/t)', fontsize=9)
# ax.set_ylabel('Parameter', fontsize=9)


# Add legend inside the box of the figure with black frame color
legend = ax.legend(loc='center left', bbox_to_anchor=(0.65, 0.5), fontsize=9)
legend.get_frame().set_edgecolor('black')

# Save plot as png image with specified characteristics
plt.savefig('Figure5_2.png', dpi=300, bbox_inches='tight')
from google.colab import files
files.download('Figure5_2.png')

# Show plot
plt.show()
