import matplotlib.pyplot as plt 
import pandas as pd
import pathlib
import numpy as np

# Path to the directory containing the ECMWF data
path = pathlib.Path('ecmwf_data')

# Site list (same as before, you can adapt if necessary)
sites = ['chlm', 'dnsg', 'jmla', 'kkn4', 'lmjg', 'smkt', 'sybc', 'tplj']

# Defining other year ranges
other_years = ['1-59', '60-151', '152-243', '244-334', '335-365']

# Conversion factor for cm
cm = 1/2.54

# Creating the figure and axes (1 plot for all sites)


# Loop through sites and plot data
for site in sites:
    # Plot each site's data on the same axes
    fig, ax = plt.subplots(1, 1)
    for file in path.iterdir():
        if site.upper() in file.name and '.csv' in file.name:
            print(f'{file.name[:4]}')
            print(file.name)  

            # Read the ECMWF data
            r = pd.read_csv(file)

            # Convert the 'time' column to datetime and extract the day of the year (DOY)
            r['time'] = pd.to_datetime(r['time'])
            r['DOY'] = r['time'].dt.dayofyear

            # Extract the total precipitable water (tp) from the file
            mean = r['tp'].mean()

            # Find positions where there's a gap in the data (if any)
            pos = np.where(np.abs(np.diff(r['DOY'])) > 1)[0] + 1
            x = r['DOY'].to_numpy()  # Convert to numpy array
            y = r['tp'].to_numpy()*1000  # Convert to numpy array

            # Plot the data on the same axes
            ax.plot(x, y, label=f'{file.name[5:9]}')  # label is year

            # Add labels for seasons
            ax.axvline(152, linestyle='dashed', color='grey', alpha=0.5)
            ax.text(80, mean, 'Spring', fontsize=6)
            ax.axvline(244, linestyle='dashed', color='grey', alpha=0.5)
            ax.text(170, mean, 'Summer', fontsize=6)
            ax.axvline(335, linestyle='dashed', color='grey', alpha=0.5)
            ax.text(260, mean, 'Autumn', fontsize=6)
            ax.text(330, mean, 'Winter', fontsize=6)
            ax.axvline(60, linestyle='dashed', color='grey', alpha=0.5)
            ax.text(5, mean, 'Winter', fontsize=6)

            # Adjust the tick parameters
            ax.locator_params(tight=True, nbins=5, axis='x')
            ax.locator_params(tight=True, nbins=3, axis='y')

    # Set the title for the subplot (only once per site)
    ax.set_title(f'{site} - Total Precipitable Water')

    # Set labels and legend
    ax.set_xlabel('Day of Year')
    ax.set_ylabel('Total Precipitable Water (tp, mm)')
    ax.legend(loc='upper left', prop={'size': 6})

    # Optionally, save the figure to a file after all files for this site are processed
    fig.tight_layout()        
    plt.savefig(f'precp_plots/{site}_precp_plots.png')

    # Optionally, display the plot for the current site
    #plt.show()

    # Close the plot to avoid overlap between different site plots
    plt.close()

