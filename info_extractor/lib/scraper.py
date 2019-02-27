import urllib.request
from lxml import etree


def get_scraper(market):
    scraper_market = {
        'NZX': NZXScraper
    }
    return scraper_market[market]()


class Scraper:
    def scrape_analysis(self, instrument):
        pass


class NZXScraper(Scraper):
    def scrape_analysis(self, instrument):
        response = urllib.request.urlopen(
            "https://www.nzx.com/companies/%s/analysis" % instrument.name
        )
        html = response.read().decode("utf8")
        response.close()

        tree = etree.fromstring(html, parser=etree.HTMLParser())
        content_html = repr(etree.tostring(tree.xpath(".//*[contains(@class, 'content')][1]")[0]))\
            .replace("\\n", "")\
            .replace("b'", "")

        return content_html
