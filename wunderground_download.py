from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import pandas as pd

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_daily_data(station_id, y, m, d):    

    global dir_path

    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(str(dir_path+'\\chromedriver.exe'), chrome_options=option)  
    
#    browser = webdriver.Chrome()
    browser.implicitly_wait(5) # seconds
    browser.get('https://www.wunderground.com/history/daily/us/ny/new-york-city/'+station_id+'/date/'+y+'-'+m+'-'+d)
    
    element = browser.find_element_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table')
    daytext=element.text    
    browser.quit()
    
    print(y+'-'+m+'-'+d)
    
    row_text=''
    day_list=[]
    columns=''
    df_dict=[]
    df=pd.DataFrame
    
    for i in daytext:
        if i=='\n':
            day_list.append(row_text)
            row_text=''
        else:
            row_text+=i
    day_list.append(row_text)
    
    time_index=day_list.index('Time')
    condition_index=day_list.index('Condition')
    
    columns=day_list[time_index:condition_index+1]
    onetime=True
    
    for eachtext in day_list[condition_index+1:]:   
        e_list=eachtext.split()
        e_list_plus=[]
        e_list_plus.append(m+'/'+d+'/'+y+'/'+e_list[0]+e_list[1])
        e_list_plus.append(e_list[2])
        e_list_plus.append(e_list[4])
        e_list_plus.append(e_list[6])
        e_list_plus.append(e_list[8])
        e_list_plus.append(e_list[9])
        e_list_plus.append(e_list[11])
        e_list_plus.append(e_list[13])
        e_list_plus.append(e_list[15])
        lastcell=''
        for i in e_list[17:]:
            lastcell+=i
        e_list_plus.append(lastcell)   
        
        if onetime:
            df_dict=np.array([e_list_plus])
            onetime=False
        else:      
            df_dict = np.append(df_dict,[e_list_plus],axis = 0)
    
    df=pd.DataFrame(df_dict,columns=columns)
    return df


def GetData(year_start, year_end, month_start, month_end, day_start, day_end, station_id):
    first_time=True
    df_all=pd.DataFrame

    global dir_path


    for yy in range(year_start, year_end+1):
        for mm in range(month_start, month_end+1):
            for dd in range(day_start, day_end+1):
                # Check if leap year
                if yy % 400 == 0:
                    leap = True
                elif yy % 100 == 0:
                    leap = False
                elif yy % 4 == 0:
                    leap = True
                else:
                    leap = False
                # print(y,leap)

                # Check if already gone through month
                if mm == 2 and leap and dd > 29:
                    continue
                elif mm == 2 and dd > 28:
                    continue
                elif mm in [4, 6, 9, 11] and dd > 30:
                    continue
                
                if first_time:
                    df_all=get_daily_data(station_id, str(yy), str(mm), str(dd))
                    first_time=False
                else:
                    df_daily=get_daily_data(station_id, str(yy), str(mm), str(dd))
                    df_all=pd.concat([df_all,df_daily])      

        df_all.reset_index(drop=True,inplace=True)
        lists = [str(year_start), str(year_end), str(month_start), str(month_end), str(day_start), str(day_end)]

        separator = '_'
        concat = separator.join(lists)

        df_all.to_csv(dir_path+'\\'+station_id+'_'+concat +'.csv')



station_id = 'KNYMOHAW4'
year_start = 2018
year_end = 2018
month_start = 1
month_end = 1
day_start = 1
day_end = 3


GetData(year_start, year_end, month_start, month_end, day_start, day_end, station_id)