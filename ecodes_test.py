import netCDF4
import pandas as pd
import xarray as xr

def netcdf_to_csv():
	precip_nc_file = '2012-2014.nc'
	nc = netCDF4.Dataset(precip_nc_file, mode='r')
	print(nc.variables.keys())

	lat = nc.variables['latitude'][:]
	lon = nc.variables['longitude'][:]
	time_var = nc.variables['time']
	dtime = netCDF4.num2date(time_var[:],time_var.units)
	t2m = nc.variables['t2m'][:]
	sp=nc.variables['sp'][:]
	tcwv=nc.variables['tcwv'][:]
	tp=nc.variables['tp'][:]
	print(t2m)
	# a pandas.Series designed for time series of a 2D lat,lon grid
	precip_ts = pd.Series(t2m, index=dtime) 
	a=pd.Series(sp, index=dtime)
	b=pd.Series(tcwv, index=dtime)
	c=pd.Series(tp, index=dtime)
	df=pd.concat([precip_ts,a,b,c],axis=1)
	df.to_csv('2012-2014.csv',index=True, header=True)

nc = xr.open_dataset('2015-2016.nc')
#df=nc.to_dataframe()
#df.to_csv('2015-2016.csv')
print(nc.variables.keys())
