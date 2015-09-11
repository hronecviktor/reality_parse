import re
from math import ceil

from bs4 import BeautifulSoup

from sites import BaseRealitySite
from rparse import UrlGetter, BS


class Byty_sk(BaseRealitySite):
    def __init__(self, price_low: int = 0, price_high: int = 1000, range: int = 50, with_photo: bool = False):
        super(Byty_sk, self).__init__(price_low=price_low, price_high=price_high)
        self.range = range
        self.base_url = '''http://www.byty.sk/bratislava/prenajom?p[param10]=18&p[distance]={range}&p[param1]\
[from]={price_low}&p[param1][to]={price_high}'''.format(
            price_low=self.price_low,
            price_high=self.price_high,
            range=self.range)+'''&p[page]={page_number}'''
        self.with_photo = with_photo
        if self.with_photo:
            self.base_url += '&p[foto]=1'
        self.offer_num = None
        self.page_num = None
        self.offers = None

    def get_page_url(self, page_number: int = 1):
        return self.base_url.format(page_number=page_number)

    def number_of_pages(self):
        if self.page_num is not None:
            return self.page_num
        resp = UrlGetter.get_single_page_instance().get_urls([self.get_page_url(1)]).pop()
        soup = BS(resp.text)
        count_info = soup.find(text=re.compile('''.*z celkom .*''')).strip()
        start, stop, total = [int(val) for val in re.findall('(\d+)\s-\s+(\d+)\s+z\s+celkom\s+(\d+)\sinzer', count_info).pop()]
        self.offer_num = total
        self.page_num = ceil(total / (stop - start + 1))


    def number_of_offers(self):
        if self.offer_num is None:
            self.number_of_pages()
        return self.offer_num

    def get_offer_urls(self):
        urls = [self.get_page_url(number) for number in range(1,self.number_of_pages()+1)]
        responses = [resp.text for resp in UrlGetter.get_instance().get_urls(urls)]
        offer_urls = []
        for response in responses:
            bs = BeautifulSoup(response, 'html.parser')
            link_elems = bs.find_all(class_='advertisement-head')
            hrefs = [elem.find_all(lambda tag: 'href' in tag.attrs).pop()['href'] for elem in link_elems]
            offer_urls.extend(hrefs)
        return offer_urls

    def get_offers(self):
        urls = self.get_offer_urls()
        responses = UrlGetter.get_instance().get_urls(urls)
        re_price = re.compile('\s*(\d+)\s*')
        for resp in responses:
            bs = BeautifulSoup(resp.text, 'html.parser')
            elem_price = bs.find(id='data-price')
            price = int(*re_price.findall(elem_price.text))
            print("Price: {}".format(price))
            elem_title = bs.find(class_='advTop')
            title = elem_title.h1.text.strip()
            print("Title: {}".format(title))


x = Byty_sk(50, 400)
print(x.base_url)
print("total: {}\npage nums: {}\nurls: {}".format(x.number_of_offers(), x.number_of_pages(), x.get_offers()))
