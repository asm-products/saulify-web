__all__ = ["TestCase"]

import re
import urlparse
import lxml.html
import colorama

from saulify.scrapers.cascade import clean_url

colorama.init()

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
            article = clean_url(self.url, include_html=True)
        except Exception as e:
            return {
                "url": self.url,
                "status": "EXCEPTION",
                "message": e.message
            }
        else:
            if not article:
                return {
                  "url": self.url,
                  "status": "EXCEPTION",
                  "message": "Output was empty; Could be because the result was not HTML."
                }
            else:
                norm_space = re.sub(r'\s+', ' ', article.markdown)
                if "test_contains" not in self._spec:
                    return {
                            "url": self.url,
                            "status": "WARNING",
                            "message": "NO TEST CASES SPECIFIED: try testing for a string or image in the page contents"
                        }
                else:
                    return {
                        "url": self.url,
                        "status": "OK",
                        "result": {
                            "fragments": self.check_fragments(norm_space),
                            "images": self.check_images(article.markdown_html),
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
        # Remove encoding tag because lxml won't accept it for unicode objects
        if isinstance(html, bytes):
            if html.startswith(b'<?'):
               html = re.sub(b'^\<\?.*?\?\>', b'', html, flags=re.DOTALL)
        else:
            if html.startswith('<?'):
                html = re.sub(r'^\<\?.*?\?\>', '', html, flags=re.DOTALL)
                
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

    def output_markdown(self):
        """ 
        Outputs Markdown for a test_url so we can easily define a test_contains for it.
        """
        try:
            article = clean_url(self.url, include_html=True)
            if result:
                markdown = article.markdown.encode('utf-8')
        except Exception as e:
            print("Exception on URL {0}: {1}".format(self.url, e.message))
        else:
            if not result:
                output = "BAD SPEC FILE ({0}): Response was empty or was not HTML".format(self.url)
            else:
                output = 'Markdown for URL: {0}\n\n'.format(self.url) + markdown 
            print(colorama.Fore.GREEN + 'TEST_CASE_BEGINNING:\n------------------------------\n' +
                  colorama.Fore.RESET + output +
                  colorama.Fore.RED + '\nTEST_CASE_END\n------------------------------\n\n')

