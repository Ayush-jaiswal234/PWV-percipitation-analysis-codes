import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pathlib
import pandas as pd 
cm = 1/2.54

sites = ['chlm', 'dnsg', 'jmla', 'kkn4', 'lmjg', 'smkt', 'sybc', 'tplj']
path = pathlib.Path('ecmwf_data')

# Loop through sites
for site in sites:
    # Create a new figure for each site
    fig, ax = plt.subplots()  # Adjust size as needed

    # Loop through files to find those matching the current site
    for file in path.iterdir():
        if site in file.name.lower():
            print(f'{file.name[:-4].lower()}')

            # Read the precipitation and PWV data
            PW_df = pd.read_csv(f'met_zfiles/{file.name[:-4].lower()}_zfile.csv')
            precp_df = pd.read_csv(file)
            precp_df['time'] = pd.to_datetime(precp_df['time'])

            # Group by Day of Year (DOY) and compute average precipitation
            req = precp_df.groupby([precp_df['time'].dt.strftime('%j')])['tp'].mean().reset_index(name='Precp')
            req['time'] = pd.to_numeric(req['time'], errors='coerce')
            req['Precp'] = req['Precp'] * 1000  # Convert to mm
            req = req.rename(columns={"time": "DOY"})

            # Merge PWV and precipitation data on DOY
            merge = PW_df.merge(req[['DOY', 'Precp']], on='DOY')

            # Compute the cross-correlation between PWV and Precipitation
            corr = signal.correlate(merge['PWV'].values, merge['Precp'].values)
            lags = signal.correlation_lags(len(merge['Precp'].values), len(merge['PWV'].values))
            corr /= np.max(corr)

            # Plot the correlation for this file
            ax.plot(lags, corr, label=f'{file.name[5:9]}')  # Label by year (e.g., '2012')

    # Customize plot for the site
    ax.set_title(f'{site}')
    ax.set_xlabel('Lag')
    ax.set_ylabel('Correlation Coefficient')
    ax.legend()

    # Save the figure for the site
    plt.tight_layout()
    plt.savefig(f'cross_correlation_plots/{site}.png')  # Save for the current site
    plt.close()  # Close the figure to avoid creating new ones for each site
