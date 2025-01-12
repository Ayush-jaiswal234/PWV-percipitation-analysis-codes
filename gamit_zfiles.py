import pandas as pd
import matplotlib.pyplot as pyplot
import pathlib
import re

sites=['chlm','dnsg','jmla','kkn4','lmjg','smkt','sybc','tplj']
paths=pathlib.Path('/home/ayush/Desktop/lsra/')
for site in sites:
	for year in paths.iterdir():
		errors=[]
		site_year_df=pd.DataFrame(columns=['DOY','PWV'])
		if year.name.isnumeric() and '2016' not in year.name:
			for day in year.iterdir():
				if day.name.isnumeric():
					#print(year.name[2:],day.name)
					if pathlib.Path(f'{day}/met_{site}.{year.name[2:]}{day.name}').exists():
						good_fit=False
						with open(f'{day}/sh_gamit_{day.name}.summary') as summary:
							for line in summary:
								good_fit=False
								if re.search(' Phase ambiguities WL fixed  [0-7][0-9].[0-9]%',line):
									print(f'{year.name[2:]},{day.name}')
									good_fit=True
						#print(good_fit)
						if not good_fit:
							errors.append(f'{year.name[2:]},{day.name}')
						#if good_fit:			
							#day_data=pd.read_csv(f'{day}/met_{site}.{year.name[2:]}{day.name}',sep='\s+',names=['Yr','Doy','Hr','Mn','Sec','Total Zen','Wet Zen','Sig Zen','PW','Sig PW (mm)','Press (hPa)','Temp (K)','ZHD (mm)','Grad NS','Sig NS','Grad EW','Sig EW (mm)'],skiprows=4)
							#change sum to mean for average
							#site_year_df.loc[len(site_year_df.index)]=[day_data['Doy'][0],day_data['PW'].mean()]
			
			#site_year_df=site_year_df.sort_values('DOY').reset_index(drop=True)
			#site_year_df.to_csv(f'correction/{site}_{year.name}_zfile.csv')				
			#used for testing
		print(errors)