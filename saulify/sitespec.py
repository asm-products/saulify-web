""" Reading and representation of Instapaper spec files. """

import re
import urlparse
import lxml.html
import collections

from saulify.clean import clean_content


def parse_specfile(f):
    """
    Parses Instapaper spec file into its component directives

    Args:
      f (file): Spec file object

    Returns:
      List of (label, content) tuples representing directives
    """

    r = re.compile("(?P<label>[^#:]+):(?P<content>[^#]+)")

    for t in f.read().splitlines():
        m = r.match(t)
        if m:
            label = m.group("label").strip()
            content = m.group("content").strip()
            yield (label, content)


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


def load_testcases(f):
    """
    Reads test cases from an Instapaper spec file.

    Scans file until it reaches a line labelled "test_url", then creates a
    new ``TestCase`` object. Subsequent lines populate the test case.
    Multiple test cases in a single file are supported.

    Args:
      f (file): Spec file object

    Returns:
      A list of ``TestCase`` objects.
    """

    cases = []

    for label, content in parse_specfile(f):
        if label == "test_url":
            url = content
            case = TestCase(url)
            cases.append(case)
        elif label.startswith("test_"):
            if not cases:
                raise Exception("Invalid spec file")
            opencase = cases[-1]
            if label == "test_contains":
                opencase.add_contains(content)
            elif label == "test_contains_image":
                opencase.add_image(content)

    return cases


def load_rules(f):
    """
    Reads scraping rules from Instapaper spec file.

    The scraping rules are stored in a dictionary. For simple directives
    like `strip`, the rules are stored in a list using the directive name as
    the key. Exceptions to this storage format are detailed below.

    `find_string` / `replace_string` :
        These directives come in pairs; one find regular expression and one
        replace. Stored as a list of 2-tuples under the key `"find_replace"`.

    Args:
      f (file): Spec file object

    Returns:
      Dictionary containing scraper rules.
    """

    rules = collections.defaultdict(list)
    find_string = None

    for label, content in parse_specfile(f):

        if label.startswith("test_"):
            continue

        if label == "find_string":
            find_string = content

        elif label == "replace_string":
            if not find_string:
                raise Exception("Invalid spec file")
            rules["find_replace"].append((find_string, content))

        else:
            rules[label].append(content)

    return rules
