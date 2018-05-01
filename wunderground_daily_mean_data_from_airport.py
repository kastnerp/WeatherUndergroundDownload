import urllib.request, urllib.parse
from typing import List, Any

from bs4 import BeautifulSoup
import string
import re
import pandas as pd
import os

# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = open('wunder_daily_mean_data_from_airport.csv', 'w')

#Settings
station_id = "KJFK"
year_start = 2017
year_end = 2018
month_start = 1
month_end = 2
day_start = 1
day_end = 3


f.write("timestamp" + "," + "windspeed" + '\n')
print("timestamp" + "," + "windspeed" + '\n')
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

            # Open wunderground.com url
            url = "https://www.wunderground.com/history/airport/" + str(station_id) + "/" + str(y) + "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
            page = urllib.request.urlopen(url)

            # Get temperature from page
            soup = BeautifulSoup(page, "html.parser")
            windSpeed = soup.find("span", text="Wind Speed").parent.find_next_sibling("td").get_text(strip=True)
            windSpeedInt = re.findall(r'\d+', windSpeed)

            #dayTemp = str(soup.body.b.string)

            # Format month for timestamp
            if len(str(m)) < 2:
                mStamp = '0' + str(m)
            else:
                mStamp = str(m)

            # Format day for timestamp
            if len(str(d)) < 2:
                dStamp = '0' + str(d)
            else:
                dStamp = str(d)

            # Build timestamp
            timestamp = str(y) + mStamp + dStamp
            # Write timestamp and temperature to file

            print("day: " + str(d) + ", month: " + str(m) + ", year: " + str(y))
            f.write(timestamp + "," + windSpeedInt[0] + '\n')


# Done getting data! Close file.
f.close()
