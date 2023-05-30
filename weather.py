# -*- coding: utf-8 -*-
# @Time : 12/22/2021 11:09
# @Author : wxy
# @File : weather.py
# @Software: PyCharm


from datetime import datetime
import time
import pandas as pd
from math import log10
from tqdm import tqdm
import numpy as np
import pymongo
from math import log10, cos, sin, asin, sqrt, exp, pi, radians

def fmt_cul_file(x):
    # format data
    if isinstance(x, float):
        if x == -999:
            x = int(-99)
        # elif x <100:
        #     x= "{0:5.2f}".format(x)
        #     x = str(x).zfill(5)
        else:
            x = "{0:6.2f}".format(x)
            x = str(x).zfill(5)
    return x
def d_to_jd(time):
    fmt = '%Y-%m-%d'
    dt = datetime.strptime(time, fmt)
    tt = dt.timetuple()
    return str(tt.tm_year * 1000 + tt.tm_yday)

def jd_to_time(time):
    dt = datetime.strptime(time, '%Y%j').date()
    fmt = '%Y-%m-%d'
    return dt.strftime(fmt)

def wind10to2(wind10):
    """Converts windspeed at 10m to windspeed at 2m using log. wind profile
    """
    wind2 = wind10 * (log10(2./0.033) / log10(10/0.033))
    return wind2






for y in [2010,2005]:
    for i in tqdm(range(0,97711)):
        sitename = 'CN' + str(i + 1).zfill(6)
        df = pd.read_csv(r'G:/apsim_weather/'+str(y)+'/'+sitename+'.csv',index_col=0, sep=",", parse_dates=False)
        df = df[df['time'] != 'time']
        # site = df['NAME'].iloc[i]
        lon= df.iloc[0]['lon']
        lat = df.iloc[0]['lat']
        # print(lon,lat)
        df['dtime'] = pd.to_datetime(df['time'], errors='coerce', format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d')
        # tmean.index = pd.to_datetime(data['time'])
        # df['dtime'] = df['time'].apply(lambda x: x.strftime("%Y-%m-%d")).dt.strftime('%Y-%m-%d')
        # datetime.strptime(df.iloc[0]['ddate'], "%Y-%m-%d %H:%M:%S")
        # print(df)
        df['prec'] = pd.to_numeric(df['prec']) * 3  # 3小时降水
        df['srad'] = pd.to_numeric(df['srad']) * 3 / 1000 * 3.6  # W/m2 ->Mj/m2
        df['temp'] = pd.to_numeric(df['temp']) - 273.15
        # #
        da = pd.DataFrame(columns=['date', 'srad', 'tmax', 'tmin', 'prec'])
        # #
        da[['date', 'tmax']] = df.groupby(by=['dtime'], as_index=False)['temp'].max()
        da['tmin'] = df.groupby(by=['dtime'], as_index=False)['temp'].min()['temp']
        da['prec'] = df.groupby(by=['dtime'], as_index=False)['prec'].sum()['prec']
        da['srad'] = df.groupby(by=['dtime'], as_index=False)['srad'].sum()['srad']
        tmean = df.groupby(by=['dtime'], as_index=False)['temp'].mean()['temp']
        # print(da)
        tmean.index = pd.to_datetime(da['date'])
        month_mean = tmean.resample('M').mean()
        amp = month_mean.max() - month_mean.min()
        tav = tmean.mean()
        date = da['date'].apply(d_to_jd)
        year = date.str[:4]
        day = date.str[4:]
        tmin = da['tmin'].apply(fmt_cul_file)
        tmax = da['tmax'].apply(fmt_cul_file)

        rain = da['prec'].apply(fmt_cul_file)
        srad = (da['srad']).apply(fmt_cul_file)
        input=list(zip(year,day,rain,tmax,tmin,srad))
        # #
        # # # # try:
        # # # #     data = pd.read_csv(r'F:/统计数据/potato_weather_new/'+site+'.csv',index_col=0)
        # # # #     # print(data)
        # # # # except Exception as e:
        # # # #     print(e)
        # # # # # tmean = data[['Temperature_Air_2m_Min_24h','Temperature_Air_2m_Max_24h']].mean(axis=1)
        # # # # # tmean.index = pd.to_datetime(data['time'])
        # # # # # month_mean = tmean.resample('M').mean()
        # # # # # amp = month_mean.max() - month_mean.min()
        # # # # # tav = tmean.mean()
        # # # # # wind2 = data['Wind_Speed_10m_Mean'].apply(wind10to2).apply(fmt_cul_file)
        # # # # # tmin = data['Temperature_Air_2m_Min_24h'].apply(fmt_cul_file)
        # # # # # tmax = data['Temperature_Air_2m_Max_24h'].apply(fmt_cul_file)
        # # # # #
        # # # # # rain = data['Precipitation_Flux'].apply(fmt_cul_file)
        # # # # # srad = (data['Solar_Radiation_Flux']/1000000).apply(fmt_cul_file)
        # # # # # vp = data['Vapour_Pressure_Mean'].apply(fmt_cul_file)
        # # # # tmean = tmean.apply(fmt_cul_file)
        # # # date = data['time'].apply(d_to_jd)
        # # # year = date.str[:4]
        # # # day = date.str[4:]
        # # # input=list(zip(year,day,rain,tmax,tmin,tmean,srad,wind2,vp))
        # # #
        # 开始按模板格式写入
        header = []
        header.append('[weather.met.weather]')
        header.append('Site= %s' % (sitename))
        header.append('Latitude= %s'% (lat))
        header.append('Longitude= %s'% (lon))
        header.append('tav= %s'% (round(tav,2)))
        header.append('amp= %s'% (round(amp,2)))
        # header.append('year   day   rain   maxt   mint   mean   radn   wind     vp')
        # header.append(' ()    ()    (mm)   (oC)   (oC)   (oC) (MJ/m2/d) (m/s) (mbar)')
        header.append('year   day   rain   maxt   mint   radn   ')
        header.append(' ()    ()    (mm)   (oC)   (oC)   (MJ/m2/d) ')
        for i in range(0, len(input)):
            value_line = []
            for value in input[i]:
                value = str(value)
                new_value = value.rjust(5)
                value_line.append(new_value)
            line = ' '.join(value_line)
            header.append(line.lstrip())
        header.append('')#最后加入一列空行，否则模型读不到最后一天
        with open(r'G:\apsim_weather/'+str(y)+'a/'+sitename+'.met', 'w') as f:
            f.writelines('\n'.join(header))
            # f.write('\n')
