import requests
import lxml
from bs4 import BeautifulSoup
from urllib.request import urlopen
html = urlopen("https://www.nordpoolgroup.com/api/marketdata/page/59?currency=,,,EUR").read()
print(html)

