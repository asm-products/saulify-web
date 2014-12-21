__all__ = ["TestCase"]

import urlparse
import lxml.html

from saulify.clean import clean_content


class TestCase(object):
    """
    Test case for the article scraper.

    Attributes:
      url (str): URL of the page being tested
      fragments (list of str): Fragments of text that should be present in
        the output of the scraper.
      images (list of str): Urls of images that should be present in the output.
    """

    def __init__(self, url):
        self.url = url
        self.fragments = []
        self.images = []

    def add_contains(self, fragment):
        self.fragments.append(fragment)

    def add_image(self, href):
        self.images.append(href)

    def run(self):
        try:
            output = clean_content(self.url)
        except Exception as e:
            return {
                "url": self.url,
                "status": "EXCEPTION",
                "message": e.message
            }
        else:
            return {
                "url": self.url,
                "status": "OK",
                "result": {
                    "fragments": self.check_fragments(output["plaintext"]),
                    "images": self.check_images(output["html"]),
                }
            }

    def check_fragments(self, text):
        result = {"missing": [], "found": []}
        for s in self.fragments:
            if s in text:
                result["found"].append(s)
            else:
                result["missing"].append(s)
        return result

    def check_images(self, html):
        etree = lxml.html.fromstring(html)
        img_rel_urls = etree.xpath("//img/@src")
        img_abs_urls = [urlparse.urljoin(self.url, u) for u in img_rel_urls]
        result = {"missing": [], "found": []}
        for url in self.images:
            abs_url = urlparse.urljoin(self.url, url)
            if abs_url in img_abs_urls:
                result["found"].append(url)
            else:
                result["missing"].append(url)
        return result
