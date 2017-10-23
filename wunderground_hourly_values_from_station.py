import urllib.request, urllib.error, urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import Comment
import os

# Create/open a file called wunder.txt (which will be a comma-delimited file)
f = open('wunder_hourly_temp.txt', 'w')
station_id = "KMACAMBR9"


# Iterate through year, month, and day
for y in range(2016, 2017):
    for m in range(1, 13):
        for d in range(1, 32):
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
            url = "https://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=" + str(station_id) + "&graphspan=day&month=" + str(m) +  "&day=" + str(
                d) + "&year=" + str(y) + "&format=1"
            page = urllib.request.urlopen(url)
            print(url)
            soup = BeautifulSoup(urlopen(url), "html.parser")
            #print(soup)
            #print(type(soup))

            # for i in soup:
            #     data
            #     clean_data = soup.replace("br", "")

            #soup('br', limit=2)
            # Define each page
            #soup = BeautifulSoup(page, "html.parser")
            #data = soup.find_all("br").get_text(strip=True)


            #Retrieves all br tags
            #data = soup.find("br")
            #print(data)
            #print(type(data))


            for tag in soup.find_all("br"):
                data_clean = tag.next_sibling.rstrip(os.linesep)
                print(data_clean)
                f.write(data_clean)



# Close file.
f.close()
