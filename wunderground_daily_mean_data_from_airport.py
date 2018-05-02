import urllib.request, urllib.parse
from typing import List, Any

from bs4 import BeautifulSoup
import string
import re
import pandas as pd
import os
import codecs

# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = codecs.open('wunder_daily_mean_data_from_airport.csv', 'w', "utf-8")

# Settings
station_id = "KJFK"
year_start = 2013
year_end = 2015
month_start = 1
month_end = 13
day_start = 1
day_end = 2

f.write("timestamp" + "," + "temperature[C]" + "," + "windspeed[m/s]" + "," + "winddirection[deg]" + '\n')
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
            # print(y,leap)

            # Check if already gone through month
            if m == 2 and leap and d > 29:
                continue
            elif m == 2 and d > 28:
                continue
            elif m in [4, 6, 9, 10] and d > 30:
                continue

            # Open wunderground.com url
            url = "https://www.wunderground.com/history/airport/" + str(station_id) + "/" + str(y) + "/" + str(
                m) + "/" + str(d) + "/DailyHistory.html"
            page = urllib.request.urlopen(url)

            # Get data from page
            soup = BeautifulSoup(page, "html.parser")
            windSpeed = soup.find("span", text="Wind Speed").parent.find_next_sibling("td").get_text(strip=True)
            windSpeedInt = int(re.findall(r'\d+', windSpeed)[0])
            windSpeedIntMetric = round(windSpeedInt * 0.44704, 1)
            meanTemp = soup.find("span", text="Mean Temperature").parent.find_next_sibling("td").get_text(strip=True)
            meanTempInt = int(re.findall(r'\d+', meanTemp)[0])
            meanTempIntMetric = round((meanTempInt - 32) * 5 / 9, 1)
            windDirection = windSpeed[windSpeed.find("(") + 1:windSpeed.find(")")]
            if windDirection == 'South':
                windDirection = 180
            elif windDirection == 'SSW':
                windDirection = 202.5
            elif windDirection == 'SW':
                windDirection = 225
            elif windDirection == 'WSW':
                windDirection = 247.5
            elif windDirection == 'West':
                windDirection = 270
            elif windDirection == 'WNW':
                windDirection = 292.5
            elif windDirection == 'NW':
                windDirection = 315
            elif windDirection == 'NNW':
                windDirection = 337.5
            elif windDirection == 'North':
                windDirection = 0
            elif windDirection == 'NNE':
                windDirection = 22.5
            elif windDirection == 'NE':
                windDirection = 45
            elif windDirection == 'ENE':
                windDirection = 67.5
            elif windDirection == 'E':
                windDirection = 90
            elif windDirection == 'ESE':
                windDirection = 112.5
            elif windDirection == 'SE':
                windDirection = 135
            elif windDirection == 'SSE':
                windDirection = 157.5
            else:
                windDirection = windDirection

            # dayTemp = str(soup.body.b.string)

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
            # Write timestamp and data to file

            print("day: " + str(d) + ", month: " + str(m) + ", year: " + str(y))
            f.write(timestamp + "," + str(meanTempIntMetric) + "," + str(windSpeedIntMetric) + "," + str(
                windDirection) + '\n')

# Done getting data! Close file.
f.close()
