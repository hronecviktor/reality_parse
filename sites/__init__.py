from abc import ABCMeta, abstractmethod, abstractproperty
from json import dumps


class BaseRealitySite:
    __metaclass__ = ABCMeta

    @abstractproperty
    def number_of_pages(self):
        raise NotImplementedError()

    @abstractproperty
    def number_of_offers(self):
        raise NotImplementedError

    def __init__(self, price_low: int = 0, price_high: int = 1000):
        self.price_low = price_low
        self.price_high = price_high

    @abstractmethod
    def get_offer_urls(self):
        raise NotImplementedError()

    @abstractmethod
    def get_offers(self):
        raise NotImplementedError()

    @abstractmethod
    def get_page_url(self, page_number: int = 1):
        raise NotImplementedError()


class Offer(object):
    pprint_template = '''Title: {title}
Type: {type}
Price: {price}
Energies: {energies}
Locality: {locality}
Area: {area}
Price/m2: {ratio}
State: {state}
Desc: {desc}
'''

    def __init__(self, price: int = 0, area: int = 0, locality: str = "N/A", energies: int = 0, type: str = "N/A",
                 state: str = "N/A", desc: str = "N/A", title:str = 'N/A', url: str = "N/A"):
        self.price = price
        self.area = area
        self.locality = locality
        self.energies = energies
        self.type = type
        self.state = state
        self.desc = desc
        self.title = title
        self.url = url
        self.ratio = self.price / self.area if self.area else 0

    def pprint(self, json: bool = False):
        pprint_dict = dict(type=self.type,
                           price=self.price,
                           energies=self.energies,
                           locality=self.locality,
                           area=self.area,
                           ratio=self.ratio,
                           state=self.state,
                           desc=self.desc,
                           title=self.title)
        if not json:
            return Offer.pprint_template.format(**pprint_dict)
        return dumps(pprint_dict, indent=4)

if __name__ == '__main__':
    o = Offer(type="Garzonka", price=1500, area=100, title='Kutica')
    print(o.pprint())
    print(o.pprint(json=True))
