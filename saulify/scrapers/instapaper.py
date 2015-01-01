__all__ = ["InstapaperScraper"]

from lxml import html
from lxml.html.clean import clean_html


class InstapaperScraper(object):

    """ Scrapes articles based on a given set of Instapaper directives """

    def __init__(self, spec):
        """
        Args:
          spec (defaultdict of list): Dictionary of Instapaper directives.
              See `saulify.sitespec.load_rules` for details on the format.
        """
        self.spec = spec

    def clean_article(self, source):
        """ Extract article according to scraping spec.

        Args:
          source (str): The article page html.

        Returns:
            lxml.ElementTree of the cleaned article.
        """

        result = {}

        # Directives acting on the html source
        source = self._find_replace(source)
        source = self._maybe_clean(source)

        etree = html.fromstring(source)

        # Directives extracting content from the DOM
        for c in ["author", "date", "title", "footnotes"]:
            result[c] = []
            for node in self._extract_all(etree, c):
                result[c].append(node.text.strip())

        # Directives acting on the article body
        maybe_body = self._extract_first(etree, "body")
        body = maybe_body if maybe_body is not None else etree
        body = self._strip_nodes(body)
        body = self._strip_id_or_class(body)
        body = self._strip_image_src(body)

        result["html"] = html.tostring(body)

        return result

    def _maybe_clean(self, source):
        if self.spec["lxml_clean"] is not False:
            return clean_html(source)
        return source

    def _find_replace(self, source):
        """ Implements the `find_string` and `replace_string` directives.

        Uses simple (non-regex) find and replace.
        """
        for find, replace in self.spec["find_replace"]:
            source = source.replace(find, replace)
        return source

    def _strip_nodes(self, etree):
        """ Implements the `strip` directive.

        Strips any elements matched by the configured xpaths.
        """
        for xpath in self.spec["strip"]:
            self._drop_by_xpath(etree, xpath)
        return etree

    def _strip_image_src(self, etree):
        """ Implements the `strip_img_src` directive.

        Strips any `img` whose @src contains certain substrings.
        """
        for substr in self.spec["strip_image_src"]:
            # The value for this field is sometimes surrounded by quotes
            substr = substr.strip(" \"'")
            xpath = '//img[contains(@src,"{0}")]'.format(substr)
            self._drop_by_xpath(etree, xpath)
        return etree

    def _strip_id_or_class(self, etree):
        """ Implements the `strip_id_or_class` directive.

        Strips any elements whose @id or @class contains certain substrings.
        Functionality is defined by the fivefilters documentation and contains
        many potential problems (e.g. this will drop elements with class equal
        to "notclass1" when the supplied string is "class1", see the unit test).

        Fixes are possible but may break compatibility with some existing site
        configuration files.
        """
        for id_or_class in self.spec["strip_id_or_class"]:
            # The value for this field is sometimes surrounded by quotes
            id_or_class = id_or_class.strip(" \"'")
            xpath = '//*[contains(@class,"{0}")] | //*[contains(@id,"{0}")]' \
                    .format(id_or_class)
            self._drop_by_xpath(etree, xpath)
        return etree

    def _drop_by_xpath(self, etree, xpath):
        """ Drop all elements matching `xpath` from `etree` """
        for elem in etree.xpath(xpath):
            elem.drop_tree()

    def _extract_all(self, etree, component):
        """ Find nodes in the DOM for all xpaths in a spec directive.

        Args:
            etree (lxml.ElementTree): DOM from which to extract data.

            component (str): A key in the spec (e.g. `"author"`),
                for which nodes will be extracted.

        Returns:
            A flat list of the matching nodes for every configured xpath.
        """
        for xpath in self.spec[component]:
            for node in etree.xpath(xpath):
                yield node

    def _extract_first(self, etree, component):
        """ Find first DOM node matching an xpath in a spec directive.

        Args:
            etree (lxml.ElementTree): DOM from which to extract node.

            component (str): Key in the spec (e.g. `"author"`).

        Returns:
            An `lxml.Element` if any nodes were matched, otherwise `None`.
        """
        g = self._extract_all(etree, component)
        return next(g, None)
