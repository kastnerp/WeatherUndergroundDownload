import urllib.request, urllib.parse
from typing import List, Any

from bs4 import BeautifulSoup
import string
import re
import pandas as pd

# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = open('wunder-data.txt', 'w')
station_id = "KJFK"

f.write("timestamp" + "," + "windspeed" + '\n')
print("timestamp" + "," + "windspeed" + '\n')
# Iterate through year, month, and day
for y in range(2013, 2018):
    for m in range(1, 12):
        for d in range(1, 31):

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
            if (m == 2 and leap and d > 29):
                continue
            elif (m == 2 and d > 28):
                continue
            elif (m in [4, 6, 9, 10] and d > 30):
                continue

            # Open wunderground.com url
            url = "https://www.wunderground.com/history/airport/" + str(station_id) + "/" + str(y) + "/" + str(m) + "/" + str(d) + "/DailyHistory.html"
            page = urllib.request.urlopen(url)
            print(url)

            # Get temperature from page
            soup = BeautifulSoup(page, "html.parser")
            windSpeed = soup.find("span", text="Wind Speed").parent.find_next_sibling("td").get_text(strip=True)
            windSpeedInt = re.findall(r'\d+', windSpeed)

            span = soup.find("span", text="(EST)").get_text(strip=True)

            print(span)

            #for h in range(0,23):
            #   windSpeed[h] = soup.find

            table = soup.find("table",id="obsTable")
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                pd.DataFrame([[i.text for i in tr.findAll('td')] for tr in table_rows])


                #print(row)





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

            print(timestamp,windSpeedInt)
            f.write(timestamp + "," + windSpeedInt[0] + '\n')


# Done getting data! Close file.
f.close()
