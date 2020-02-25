import urllib.request, urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import codecs
import config
from urllib.request import Request, urlopen

f = codecs.open('wunder_hourly_data_from_station.csv', 'w', "utf-8")

f.write(
    "Time,TemperatureF,DewpointF,PressureIn,WindDirection,WindDirectionDegrees,WindSpeedMPH,WindSpeedGustMPH,Humidity,HourlyPrecipIn,Conditions,Clouds,dailyrainin,SolarRadiationWatts/m^2,SoftwareType,DateUTC" + '\n')
# Iterate through year, month, and day
for y in range(config.year_start, config.year_end):
    for m in range(config.month_start, config.month_end):
        for d in range(config.day_start, config.day_end):
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
            site = "https://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=" + str(
                config.station_id) + "&graphspan=day&month=" + str(m) + "&day=" + str(d) + "&year=" + str(y) + "&format=1"
            #page = urllib.request.urlopen(url)

            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site,headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page, "html.parser")

            print("Fetching day: " + str(d) + ", month: " + str(m) + ", year: " + str(y))
          
            for tag in soup.find_all("br"):
                data_clean = tag.next_sibling.rstrip(os.linesep)
                #print(data_clean)                
                f.write(data_clean)
# Close file.
f.close()
