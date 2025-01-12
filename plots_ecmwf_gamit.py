import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import numpy as np

def subplot_fig(req,zfile,file):
	fig,ax=plt.subplots(2,1,figsize=[10,10],sharex=True)
	ax[0].plot(req['time'].values,req['Precp'].values*1000)
	ax[0].set_ylabel('Average Precipitation/mm')

	pos = np.where(np.abs(np.diff(zfile['DOY'])) > 1)[0]+1
	x = np.insert(zfile['DOY'], pos, np.nan)
	y = np.insert(zfile['PWV'], pos, np.nan)

	ax[1].plot(x,y)
	ax[1].set_xlabel('Day of Year')
	ax[1].set_ylabel('Average Precipitable Water/mm')

	fig.suptitle(f'{file}')
	plt.savefig(f'met_zfiles/{file}.png')
	#plt.show()

#change destination of zfile and req.groupby parameters to change from total to average or vice versa
path=pathlib.Path('ecmwf_data/')
for file in path.iterdir():
	df=pd.read_csv(file,usecols=['time','tp'])
	df.time=pd.to_datetime(df['time'])
	req=df.groupby([df.time.dt.strftime('%j')])['tp'].mean().reset_index(name='Precp')
	req.time=pd.to_numeric(req.time,errors='coerce')
	zfile=pd.read_csv(f'met_zfiles/{file.name[:-4].lower()}_zfile.csv',usecols=['DOY','PWV'])
	subplot_fig(req,zfile,file.name[:-4])