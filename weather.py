# -*- coding: utf-8 -*-
# @Time : 12/22/2021 11:09
# @Author : wxy
# @File : weather.py
# @Software: PyCharm


from datetime import datetime
import pandas as pd
from math import log10
from tqdm import tqdm
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

df =pd.read_excel('D:/potato_model/xfile/potato_new.xlsx')
for i in tqdm(range(len(df))):
    lon_in = round(df['LON'].iloc[i], 3)
    lat_in = round(df['LAT'].iloc[i], 3)
    site = df['NAME'].iloc[i]
    sitename ='CN000' + str(i + 1).zfill(3)
    try:
        data = pd.read_csv(r'F:/统计数据/potato_weather/'+site+'.csv',index_col=0)
        # print(data)
    except Exception as e:
        print(e)
    tmean = data[['Temperature_Air_2m_Min_24h','Temperature_Air_2m_Max_24h']].mean(axis=1)
    tmean.index = pd.to_datetime(data['time'])
    month_mean = tmean.resample('M').mean()
    amp = month_mean.max() - month_mean.min()
    tav = tmean.mean()
    wind2 = data['Wind_Speed_10m_Mean'].apply(wind10to2).apply(fmt_cul_file)
    tmin = data['Temperature_Air_2m_Min_24h'].apply(fmt_cul_file)
    tmax = data['Temperature_Air_2m_Max_24h'].apply(fmt_cul_file)

    rain = data['Precipitation_Flux'].apply(fmt_cul_file)
    srad = (data['Solar_Radiation_Flux']/1000000).apply(fmt_cul_file)
    vp = data['Vapour_Pressure_Mean'].apply(fmt_cul_file)
    tmean = tmean.apply(fmt_cul_file)
    date = data['time'].apply(d_to_jd)
    year = date.str[:4]
    day = date.str[4:]
    input=list(zip(year,day,rain,tmax,tmin,tmean,srad,wind2,vp))

    # 开始按模板格式写入
    header = []
    header.append('[weather.met.weather]')
    header.append('Site  =  %s' % (sitename))
    header.append('Latitude=%s'% (lat_in))
    header.append('Longitude=%s'% (lon_in))
    header.append('tav=%s'% (tav))
    header.append('amp=%s'% (amp))
    header.append('year  day  rain  maxt  mint  mean  radn  wind  vp')
    header.append('()  ()  (mm)  (oC)  (oC)  (oC)  (MJ/m2/d)  (m/s)  (mbar)')

    for i in range(0, len(input)):
        value_line = []
        for value in input[i]:
            value = str(value)
            new_value = value.rjust(5)
            value_line.append(new_value)
        line = ' '.join(value_line)
        header.append(line)
    header.append('')#最后加入一列空行，否则模型读不到最后一天
    with open(r'E:/APSIM/Examples/WeatherFiles/'+sitename+'.met', 'w') as f:
        f.writelines('\n'.join(header))
        # f.write('\n')
