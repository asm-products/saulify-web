__all__ = ["TestCase"]

import urlparse
import lxml.html

from saulify.clean import clean_content


class TestCase(object):
    """
    Test case for the article scraper.

    Attributes:
      url (str): URL of the page being tested
    """

    def __init__(self, spec):
        """ Create a new TestCase object.

        Args:
            spec (defaultdict of list): Dictionary containing test directives
            as returned by `saulify.sitespec.load_testcases`. Must contain a
            `"test_url"` key.
        """
        self.url = spec["test_url"]
        self._spec = spec

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
        for s in self._spec["test_contains"]:
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
        for url in self._spec["test_contains_images"]:
            abs_url = urlparse.urljoin(self.url, url)
            if abs_url in img_abs_urls:
                result["found"].append(url)
            else:
                result["missing"].append(url)
        return result
