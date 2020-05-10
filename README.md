# WeatherUndergroundDownload

I tried to scrape weather data from Weather Underground and found two deprecated scripts online.
It seems like WU changes their setup every now and then so I had to change a couple of things to make them work again.

# Installation

> pip install beautifulsoup4

# How to run this

- Change the setting in config.py
- Run the individual scripts as for example:
> python wunderground_hourly_data_from_station.py

# Current issues

As of March 2019, WU seems to have changed their airport data websites that now seem to only work when a browser dynamically requests the data.

Update: As of May 2020, all three script stopped working.

## Broken

- wunderground_daily_mean_data_from_airport.py	
- wunderground_hourly_data_from_airport.py
- wunderground_hourly_data_from_station.py







