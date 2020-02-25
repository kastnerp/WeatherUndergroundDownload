import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import re
import pandas as pd
import codecs
import config

f = codecs.open("wunder_hourly_data_from_airport.csv", "w", "utf-8")

f.write("timestamp, Time (EST),	Temp. [C],	Dew Point [C],	Humidity,	Pressure,	Wind Dir [deg],	Wind Speed [m/s], "
        "Precip, Conditions" + '\n')
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

            # Write timestamp and temperature to file
            # Open wunderground.com url
            url = "https://www.wunderground.com/history/daily/" + str(config.station_id) + "/date/" + str(y) + "-" + str(m) + "-" + str(d)
            page = urllib.request.urlopen(url)
            #print(url)

            # Get data from page
            soup = BeautifulSoup(page, "html.parser")
            table = soup.find("table", id="history-observation-table")
            table_rows = table.find_all('tr')
            data = pd.DataFrame([[i.text for i in tr.findAll('td')] for tr in table_rows])

            time = data[0]
            temp = data[1]
            dewPoint = data[3]
            humidity = data[4]
            pressure = data[5]
            windDirection = data[7]
            windSpeed = data[8]
            windGustSpeed = data[9]
            precip = data[10]
            conditions = data[12]

            for hour in range(1, 25, 1):

                if windDirection.iloc[hour] == 'South':
                    windDirection.iloc[hour] = 180
                elif windDirection.iloc[hour] == 'SSW':
                    windDirection.iloc[hour] = 202.5
                elif windDirection.iloc[hour] == 'SW':
                    windDirection.iloc[hour] = 225
                elif windDirection.iloc[hour] == 'WSW':
                    windDirection.iloc[hour] = 247.5
                elif windDirection.iloc[hour] == 'West':
                    windDirection.iloc[hour] = 270
                elif windDirection.iloc[hour] == 'WNW':
                    windDirection.iloc[hour] = 292.5
                elif windDirection.iloc[hour] == 'NW':
                    windDirection.iloc[hour] = 315
                elif windDirection.iloc[hour] == 'NNW':
                    windDirection.iloc[hour] = 337.5
                elif windDirection.iloc[hour] == 'North':
                    windDirection.iloc[hour] = 0
                elif windDirection.iloc[hour] == 'NNE':
                    windDirection.iloc[hour] = 22.5
                elif windDirection.iloc[hour] == 'NE':
                    windDirection.iloc[hour] = 45
                elif windDirection.iloc[hour] == 'ENE':
                    windDirection.iloc[hour] = 67.5
                elif windDirection.iloc[hour] == 'E':
                    windDirection.iloc[hour] = 90
                elif windDirection.iloc[hour] == 'ESE':
                    windDirection.iloc[hour] = 112.5
                elif windDirection.iloc[hour] == 'SE':
                    windDirection.iloc[hour] = 135
                elif windDirection.iloc[hour] == 'SSE':
                    windDirection.iloc[hour] = 157.5
                elif windDirection.iloc[hour] == 'Calm':
                    windDirection.iloc[hour] = ''
                else:
                    windDirection.iloc[hour] = windDirection.iloc[hour]

                # Check if value is 'calm'
                if windSpeed.iloc[hour].strip() == 'Calm':
                    windSpeed.iloc[hour] = '0.0 mph'
                else:
                    windSpeed.iloc[hour] = windSpeed.iloc[hour].strip()

                # Check conditions

                windSpeedInt = float(re.findall("\d+\.\d+", windSpeed.iloc[hour].strip())[0])
                windSpeedIntMetric = round(windSpeedInt * 0.44704, 1)
                tempInt = float(re.findall('\d+\.\d+', temp.iloc[hour].strip())[0])
                tempIntMetric = round((tempInt - 32) * 5 / 9, 1)
                dewPointInt = float(re.findall("\d+\.\d+", dewPoint.iloc[hour].strip())[0])
                dewPointIntMetric = round((dewPointInt - 32) * 5 / 9, 1)
                pressureInt = float(re.findall("\d+\.\d+", pressure.iloc[hour].strip())[0])
                #precipInt = float(re.findall("\d+\.\d+", precip.iloc[hour].strip()))

                f.write(str(hour) + str(d) + str(m) + str(y) + "," + str(time.iloc[hour]) + "," + str(tempIntMetric) + "," + str(dewPointIntMetric) + "," + str(
                humidity.iloc[hour]) + "," + str(pressureInt) + "," + str(windDirection.iloc[hour]) + "," + str(
                windSpeedIntMetric) + "," + str(precip.iloc[hour].strip()) + ',' + str(conditions.iloc[hour]) + '\n')
                print("hour: " + str(hour) + ", day: " + str(d) + ", month: " + str(m) + ", year: " + str(y))

# Done getting data! Close file.
f.close()
