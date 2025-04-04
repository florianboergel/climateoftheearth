import pandas as pd
import numpy as np

def co2_hist(t):
    return 280 * (1+ ((t-1850)/220)**3)

def readDataTemp():
    datapath = "https://raw.githubusercontent.com/florianboergel/climateoftheocean/main/data/graph.txt"
    temp = pd.read_csv(datapath, header = None,
                    skiprows=5, index_col=0,
                    delimiter="     ",
                    engine="python")
    temp = temp + 14.15
    return temp

def readDataCO2():

    CO2_url = "https://raw.githubusercontent.com/florianboergel/climateoftheocean/main/data/monthly_in_situ_co2_mlo.csv"
    co2_data = pd.read_csv(CO2_url, header = 58,skiprows=8, index_col=0) 
    co2_data = co2_data.iloc[4:] 
    co2_data = pd.to_numeric(co2_data.iloc[:,5]) 
    co2_data[co2_data<= 0] = np.nan
    co2_data.index = pd.to_datetime(co2_data.index, format='%Y')
    co2_data = co2_data.groupby(co2_data.index.year).mean() 
    return co2_data

def createCO2timeSeries(co2Data2024Onwards):
    def co2_hist(t):
        return 280 * (1+ ((t-1850)/220)**3)

    co2_hist = co2_hist(np.arange(1850,1958))
    co2_hist = pd.Series(co2_hist)
    co2_hist.index = np.arange(1850,1958)
    
    co2Data = readDataCO2()
    co2levels = pd.concat([co2_hist, co2Data, co2Data2024Onwards])
    return co2levels

