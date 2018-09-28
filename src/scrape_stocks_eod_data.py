import requests
import json
import string
import sys
from bs4 import BeautifulSoup
import argparse

# Define and parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('exchange',
    choices=['AMEX', 'NASDAQ', 'NYSE'],
    type=str,
    help='Symbol for exchange. All EOD stock quotes will be grabbed from this exchange.')
args = parser.parse_args()

# Define functions
def get_date_of_latest_exhange_data(exchange):
	""" Grab reported date of latest data """
	req = requests.get("http://eoddata.com/")
	# Create a BeautifulSoup object for parsing
	soup = BeautifulSoup(req.text, 'lxml')
	# Extract a specific table from the BeautifulSoup object
	tb = soup.find('table', {'class': 'quotes'})
	# Extract all rows from a table
	tr = tb.find_all('tr')
	# Isolate header
	header = tr.pop(0)
	header_categories = header.find_all('th')
	header_categories = [item.get_text() for item in header_categories]
	header_categories = header_categories[0:3]
	# Iterate of rows in table, extract and print content
	for row in tr:
		# Extract all table data (td)
		stock_data = row.find_all('td')
		# Get text from table data
		content = [item.get_text() for item in stock_data]
		# Prune content to mimic headers
		content = content[0:3]
		# Store content in dictionary
		stocks = dict()
		count = 0
		for item in content:
			stocks[header_categories[count]] = item
			count += 1
		if stocks['Exchange'] == exchange:
			dt = stocks['Date']
			break
	try:
		return(dt)
	except:
		print('Error: Cannot locate exchange on site. Exiting')
		sys.exit(0)

def generate_list_of_links(exchange):
	""" eoddata.com splits into different web pages based on
		the first letter of the stock symbol. One method would
		be to comb the site for links to all symbols, however we
		can shortcut this as the URLs are well structured and
		systematic in generating. If we know the exchange 
		symbol, we can get all EOD stock quotes from the exchance. """
	alphabet = list(string.ascii_uppercase)
	base_url = "http://eoddata.com/stocklist/" + exchange + "/"
	urls = [base_url + letter + '.htm' for letter in alphabet]
	return(urls)

def get_eod_stock_quotes_from_table(exchange):
	""" Function to grab stock content from a table in HTML. This
		function is formatted specifically for eoddata.com """
	# Point to data source and exchange
	date_of_data = get_date_of_latest_exhange_data(exchange)
	urls = generate_list_of_links(exchange)
	for url in urls:
		req = requests.get(url)
		# Create a BeautifulSoup object for parsing
		soup = BeautifulSoup(req.text, 'lxml')
		# Extract a specific table from the BeautifulSoup object
		tb = soup.find('table', {'class': 'quotes'})
		# Extract all rows from a table
		tr = tb.find_all('tr')
		# Isolate header
		header = tr.pop(0)
		header_categories = header.find_all('th')
		header_categories = [item.get_text() for item in header_categories]
		header_categories = header_categories[0:6]
		# Iterate of rows in table, extract and print stock content
		for row in tr:
			# Extract all table data (td)
			stock_data = row.find_all('td')
			# Get text from table data
			content = [item.get_text() for item in stock_data]
			# Prune content to mimic headers
			content = content[0:6]
			# Store content in dictionary
			stocks = dict()
			count = 0
			for item in content:
				stocks[header_categories[count]] = item
				count += 1
			stocks['exchange'] = exchange
			stocks['date'] = date_of_data
			# Print JSON form
			j = json.dumps(stocks)
			print(j)

# Run functions
get_eod_stock_quotes_from_table(args.exchange)