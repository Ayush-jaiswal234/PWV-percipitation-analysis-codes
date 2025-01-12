import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import numpy as np

year='2012'
path=pathlib.Path('sum')
for file in path.iterdir():
	if year in file.name and '.csv' in file.name:
		print(f'{file.name[:4]}')
		r=pd.read_csv(file)
		pos = np.where(np.abs(np.diff(r['DOY'])) > 1)[0]+1 #position with gaps in the data
		x = np.insert(r['DOY'], pos, np.nan)
		y = np.insert(r['PWV'], pos, np.nan)
		plt.plot(x,y,label=f'{file.name[:4]}')
		plt.xlabel('Day of Year')
		plt.ylabel('Total Precipitable Water/mm')
		plt.title(year)
		plt.legend()
plt.savefig(f'sum/{year}_all_stations.png')		
plt.show()