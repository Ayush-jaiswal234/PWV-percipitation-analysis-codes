import pandas as pd

rnx_stat=pd.read_csv('~/Downloads/rinex_stations.csv')
rnx_stat=rnx_stat.drop(columns=['Height'])
rnx_stat=rnx_stat.round(2)

temp_df=pd.read_csv('2015-2016.csv')
year='2015'
tem=temp_df[temp_df['time']==f'{year}-01-01 00:00:00']
print(tem)
for index,rows in rnx_stat.iterrows():
	print(abs(tem['latitude']-rows['Lat']).idxmin(),min(abs(tem['latitude']-rows['Lat'])))
	print(abs(tem['longitude']-rows['Lon']).idxmin(),min(abs(tem['longitude']-rows['Lon'])))
	print((abs(tem['latitude']-rows['Lat'])+abs(tem['longitude']-rows['Lon'])).idxmin(),min(abs(tem['latitude']-rows['Lat'])+abs(tem['longitude']-rows['Lon'])))	
	area=(abs(tem['latitude']-rows['Lat'])+abs(tem['longitude']-rows['Lon'])).idxmin()
	req_data=temp_df.iloc[[area]]
	print(rows)
	print(temp_df.iloc[[area]])
	print(req_data['latitude'].values)	
	req_df=temp_df[(temp_df.latitude==req_data['latitude'].values[0]) &(temp_df.longitude==req_data['longitude'].values[0])]
	req_df=(req_df[req_df['time'].str.contains(year)])
	req_df.to_csv(f'ecmwf_data/{rows["Site"]}_{year}.csv')