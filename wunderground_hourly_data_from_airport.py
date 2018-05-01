import urllib.request, urllib.parse
from typing import List, Any

from bs4 import BeautifulSoup
import string
import re
import pandas as pd
import os

# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = open('wunder_hourly_data_from_airport.csv', 'w')

#Settings
station_id = "KJFK"
year_start = 2017
year_end = 2018
month_start = 1
month_end = 2
day_start = 1
day_end = 3


f.write("timestamp" + "," + "winddir" + "," + "windspeed" + '\n')
# Iterate through year, month, and day
for y in range(year_start, year_end):
    for m in range(month_start, month_end):
        for d in range(day_start, day_end):

            # Check if leap year
            if y % 400 == 0:
                leap = True
            elif y % 100 == 0:
                leap = False
            elif y % 4 == 0:
                leap = True
            else:
                leap = False
            #print(y,leap)

            # Check if already gone through month
            if m == 2 and leap and d > 29:
                continue
            elif m == 2 and d > 28:
                continue
            elif m in [4, 6, 9, 10] and d > 30:
                continue

            # Write timestamp and temperature to file
            # Open wunderground.com url
            url = "https://www.wunderground.com/history/airport/" + str(station_id) + "/" + str(y) + "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
            page = urllib.request.urlopen(url)


            # Get temperature from page
            soup = BeautifulSoup(page, "html.parser")
            windSpeed = soup.find("span", text="Wind Speed").parent.find_next_sibling("td").get_text(strip=True)
            windSpeedInt = re.findall(r'\d+', windSpeed)

            table = soup.find("table", id="obsTable")
            table_rows = table.find_all('tr')
            windspeed = pd.DataFrame([[i.text for i in tr.findAll('td')] for tr in table_rows])#[8]
            winddir = pd.DataFrame([[i.text for i in tr.findAll('td')] for tr in table_rows])#[7]
            time = pd.DataFrame([[i.text for i in tr.findAll('td')] for tr in table_rows])#[0]
            for hour in range(1, 25, 1):
                f.write(time.iat[hour,0].strip() + ","+ winddir.iat[hour,7].strip() + ","+ windspeed.iat[hour,8].strip() + '\n')
                #print(time.iat[i,0].strip() + "," + windspeed.iat[i,8].strip())
                print("hour: " + str(hour) + ", day: " + str(d) + ", month: " + str(m) + ", year: " + str(y))

# Done getting data! Close file.
f.close()
