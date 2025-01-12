import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import pathlib
###DON"T FORGET TO CHANGE TCWV TO PRECPITATION BEFORE RUNNING AGAIN
sites=['chlm','dnsg','jmla','kkn4','lmjg','smkt','sybc','tplj']
path=pathlib.Path('ecmwf_data')
cm=1/2.54
index=0
fig,ax=plt.subplots(4,2,figsize=(13.97*cm,21.14*cm))
for i in range(0,4):
	for j in range(0,2):
		site=sites[index]
		print(site)
		site_df=pd.DataFrame()
		for file in path.iterdir():
			if site.upper() in file.name:
				#print(f'{file.name[:-4].lower()}')
				PW_df=pd.read_csv(f'met_zfiles/{file.name[:-4].lower()}_zfile.csv')
				precp_df=pd.read_csv(file)
				precp_df.time=pd.to_datetime(precp_df['time'])
				#print(precp_df)
				req=precp_df.groupby([precp_df.time.dt.strftime('%j')])['tp'].mean().reset_index(name='Precp')
				req.time=pd.to_numeric(req.time,errors='coerce')
				req['Precp']=req['Precp'].values*1000
				req=req.rename(columns={"time":"DOY"})
				merge=PW_df.merge(req[['DOY','Precp']])
				#merge=merge[(merge['PWV']>1) & (merge['Precp']>1)]
				site_df=pd.concat([site_df,merge])
		#print(len(site_df))
		result=scipy.stats.linregress(site_df['PWV'].values,site_df['Precp'].values)
		#print(result)
		print(f"R-Squared:{result.rvalue**2:.6f}")
		print(np.corrcoef(site_df['PWV'].values,site_df['Precp'].values)[1][0])
		x= np.arange(site_df['PWV'].min(),site_df['PWV'].max()+1,1)
		y=result[0]*x+result[1]
		ax[i,j].plot(x,y,color='black')
		ax[i,j].scatter(site_df['PWV'].values,site_df['Precp'].values)
		#ax[i,j].set_xlabel('Average Precipitable Water/mm',fontsize=8)
		#ax[i,j].set_ylabel('Average Total Column Water Vapor/mm',fontsize=8)
		ax[i,j].title.set_text(f'{site}')
		index+=1

fig.supylabel('Average Precipitation/mm')
fig.supxlabel('Average Precipitable Water/mm')
fig.tight_layout()	
plt.show()
	
fig.savefig(f'tp_avg vs pwv_avg .png')
#
plt.close()