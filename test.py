from requests import get
import bs4
from math import ceil
import re
resp = get('http://www.byty.sk/bratislava/prenajom?p[param10]=18&p[distance]=50&p[param1][to]=400&p[foto]=1&p[page]=1')
soup = bs4.BeautifulSoup(resp.text, 'html.parser')
# print(soup.prettify())
soup.find_all()
pocet = soup.find(text=re.compile('''.*z celkom .*''')).strip()
max = re.findall('-\s+(\d+)\s+z\s+celkom\s+(\d+)\sinzer', pocet).pop()
print(*max)
