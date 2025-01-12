import matplotlib.pyplot as plt 
import pandas as pd
import pathlib
import numpy as np
import random

path=pathlib.Path('met_zfiles')
break_2012=['1-60','61-152','153-244','245-335','336-366']
other_years=['1-59','60-151','152-243','244-334','335-365']

sites=['chlm','dnsg','jmla','kkn4','lmjg','smkt','sybc','tplj']
for target in sites:
	fig,ax=plt.subplots(2,2,figsize=[10,10])
	colors=['#49c9c3','#5db85f','#af9000','#ff1408']
	for file in path.iterdir():
		if target in file.name and '.csv' in file.name:
			df=pd.read_csv(file,usecols=['DOY','PWV'])
			print(file)
			if '2012' in file.name:
				spring=df.iloc[60:152,:]
				summer=df.iloc[152:244,:]
				autumn=df.iloc[244:335,:]
				winter=pd.concat([df.iloc[335:,:],df.iloc[:60,:]])
			else:
				spring=df.iloc[59:151,:]
				summer=df.iloc[151:243,:]
				autumn=df.iloc[243:334,:]
				winter=pd.concat([df.iloc[334:,:],df.iloc[:59,:]])
			seasons=[spring,summer,autumn,winter]
			i,j=0,0
			color=random.choice(colors)
			colors.remove(color)
			for season in seasons:
				pos = np.where(np.abs(np.diff(season['DOY'])) > 1)[0]+1
				x = np.insert(season['DOY'], pos, np.nan)
				y = np.insert(season['PWV'], pos, np.nan)
				ax[i,j].plot(x,y,color=color,label=f'{file.name[5:9]}')
				if i==0 and j==0:
					j=1
				elif i==0 and j==1:
					i=1
					j=0
				elif i==1 and j==0:
					j=1	
	handles, labels = plt.gca().get_legend_handles_labels()
	by_label = dict(zip(labels, handles))
	fig.legend(by_label.values(), by_label.keys())
	fig.suptitle(f'{target}')
	plt.savefig(f'seasons/{target}.png')	