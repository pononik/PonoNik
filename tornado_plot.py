# Tornado plot
# to represent sensitivity analysis
# Data taken from the pre-print
# http://dx.doi.org/10.2139/ssrn.5049597
# Nikolai P. Ponomarev


import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# Data columns
parameters = ["Parameter", "Ammonium", "CAPEX", "OPEX", "IRR", "TAX", "EC", "Water", "Acid", "Coagulant", "Flocculant", "Alkali", "Electricity"]
msp_50 = ["50% on MSP (kEUR/t)", 5.709624169, 2.415928779, 2.141187106, 2.50549204, 2.899822039, 2.22435103, 2.999271236, 2.776009719, 2.985079938, 2.969651821, 2.813486236, 2.983087256]
msp_no_effect = ["No effect on MSP (kEUR/t)", 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256, 3.038077256]
msp_150 = ["150% on MSP (kEUR/t)", 2.137686195, 3.660225734, 3.934967407, 3.621156529, 3.215833964, 3.851803483, 3.076883277, 3.300144794, 3.091074575, 3.106502692, 3.262668276, 3.093067256]

# Convert lists to numpy arrays, excluding the first element (string)
msp_50_values = np.array(msp_50[1:])
msp_no_effect_values = np.array(msp_no_effect[1:])
msp_150_values = np.array(msp_150[1:])

# Calculate the differences from the central point (No effect on MSP)
low = msp_no_effect_values - msp_50_values
high = msp_150_values - msp_no_effect_values

# Calculate the percentage of "dmin" and "dmax" effect
dmin = ((msp_50_values - msp_no_effect_values) / msp_no_effect_values) * 100
dmax = ((msp_150_values - msp_no_effect_values) / msp_no_effect_values) * 100

# Create a DataFrame
df = pd.DataFrame({
    "Parameter": parameters[1:],  # Exclude the first element
    "50% on MSP": msp_50_values,
    "No effect on MSP": msp_no_effect_values,
    "150% on MSP": msp_150_values,
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
plt.savefig('tornado.png', dpi=300, bbox_inches='tight')

# Show plot
plt.show()
