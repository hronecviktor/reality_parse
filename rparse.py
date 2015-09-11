from functools import partial
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import requests
import bs4

BS = partial(bs4.BeautifulSoup, features='html.parser')


class UrlGetter(object):
    instance = None
    single_page_instance = None

    @staticmethod
    def get_instance(thread_count: int = 8):
        if not UrlGetter.instance:
            UrlGetter.instance = UrlGetter.UrlGetterSubClass(thread_count=thread_count)
        return UrlGetter.instance

    @staticmethod
    def get_single_page_instance():
        if not UrlGetter.single_page_instance:
            UrlGetter.single_page_instance = UrlGetter.UrlGetterSubClass(thread_count=1)
        return UrlGetter.single_page_instance

    class UrlGetterSubClass(object):
        def __init__(self, thread_count: int = 8):
            self.pool = ThreadPool(thread_count)

        def get_urls(self, urls: list = None):
            if not urls:
                return None
            results = self.pool.map(requests.get, urls)
            self.pool.close()
            self.pool.join()
            UrlGetter.instance = None
            return results


if __name__ == '__main__':
    urls = ['http://omz-software.com/pythonista/docs/ios/beautifulsoup_guide.html',
            'http://www.crummy.com/software/BeautifulSoup/bs4/doc/',
            'https://www.google.sk/search?client=ubuntu&channel=fs&q=bs4+tutorial&ie=utf-8&oe=utf-8&gws_rd=cr&ei=bfvtVd\
            uWFcussgHU8b3YCw',
            'http://www.byty.sk/bratislava/prenajom?p[param10]=18&p[distance]=50&p[param1][to]=400&p[foto]=1&p[page]=1',
            'http://chriskiehl.com/article/parallelism-in-one-line/']

    responses = UrlGetter.get_instance().get_urls(urls)
    print(responses)
