# stocks_web_scraping
Purpose: Demonstrate how to scrape websites using Python and BeautifulSoup

-----------
-----------

## src/scrape_stocks_eod_data.py

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) is a fantastic library for parsing HTML in a sensible way. Here, I use Python, requests, Beautiful Soup, and [eoddate.com](http://eoddata.com/) to grab end-of-day (EOD) summary data on stocks symbols from the NASDAQ exchange. 

***Example:*** Scrape web pages and extract NASDAQ exchange data (high, low, close, etc.) on all available stock symbols.
```
$ python scrape_stocks_eod_data.py NASDAQ
```

The parser will iterate thru and grab all available stock data, starting with the letter, "A." A JSON object, one object per stock, will print to the terminal. For example, the first four objects from a particular day are listed here:
```
{"Code": "AABA", "Name": "Altaba Inc", "High": "68.46", "Low": "67.46", "Close": "67.96", "Volume": "2,269,599", "exchange": "NASDAQ", "date": "09/28/18 14:25"}
{"Code": "AAL", "Name": "American Airlines Gp", "High": "41.96", "Low": "40.70", "Close": "40.79", "Volume": "2,419,090", "exchange": "NASDAQ", "date": "09/28/18 14:25"}
{"Code": "AAME", "Name": "Atlantic Amer Cp", "High": "2.550", "Low": "2.550", "Close": "2.550", "Volume": "343", "exchange": "NASDAQ", "date": "09/28/18 14:25"}
{"Code": "AAOI", "Name": "Applied Optoelect", "High": "25.78", "Low": "23.80", "Close": "24.52", "Volume": "4,601,528", "exchange": "NASDAQ", "date": "09/28/18 14:25"}
```

Of course, this data can always be writting into a file for later consumption and/or further processing. For instance, I would clean up and convert the key, "Volume," such that a number is stored as a value instead of a string. Similar to the "High" and "Low" keys. To pipe data into a file:
```
$ python scrape_stocks_eod_data.py NASDAQ > nasdaq_eod.json
```

Note: The `nasdaq_eod.json` file is not a true JSON object in itself, it is a file that contains one JSON object per line. I prefer this type of file, as opposed to creating a single JSON object. This type of file may easily parsed using `jq`:
```
head nasdaq_eod.json | jq -c '[.Code, .High, .Low, .date]'
```
This returns:
```
["AABA","68.46","67.46","09/28/18 14:30"]
["AAL","41.96","40.70","09/28/18 14:30"]
["AAME","2.550","2.550","09/28/18 14:30"]
["AAOI","25.78","23.80","09/28/18 14:30"]
["AAON","38.40","37.05","09/28/18 14:30"]
["AAPL","225.8","224.0","09/28/18 14:30"]
["AAWW","64.60","63.50","09/28/18 14:30"]
["AAXJ","70.97","70.47","09/28/18 14:30"]
["AAXN","69.35","67.47","09/28/18 14:30"]
["ABAC","2.100","2.040","09/28/18 14:30"]
```

Enjoy!
-----------
