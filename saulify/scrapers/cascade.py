import io
import os
import urlparse

import markdown2
import html2text

from flask import Markup

from . import download
from . import instapaper
from . import newspaper

from saulify.sitespec import load_rules
from saulify import cache
from saulify import models


def _serializer_cleaned_article(article):
    # This is necessary because we don't store markdown_html with the article.
    s = models.Article.serialize(article)
    return cache.serialize_expression((s, hasattr(article, 'markdown_html'),))


def _deserialize_cleaned_article(s):
    articlestr, include_html = cache.deserialize_expression(s)
    article = models.Article.deserialize(articlestr)
    if include_html:
        article.markdown_html = markdown_to_html(article.markdown)
    return article


@cache.cached_function(namespace="cascade",
                       serializer=_serializer_cleaned_article,
                       deserializer=_deserialize_cleaned_article)
def clean_url(url, include_html=True):
    """ Extract article from given url using `scraper_cascade`

    Args:
        url (str): Url of article to be scraped.

    Returns:
        Dictionary detailing the extracted article.
    """
    article = models.Article.get_by_url(url)
    if article:
        if include_html:
            article.markdown_html = markdown_to_html(article.markdown)
        return article

    content = download.download_url(url)
    result = scraper_cascade(url, content, include_html)

    article = models.Article(url, result['title'], result['authors'], result['markdown'])
    article.put()
    if include_html:
        article.markdown_html = result['markdown_html']

    return article


def scraper_cascade(url, content, include_html=True):
    """ Extract article using a fallback sequence of scrapers.

    If no scrapers are able to extract the article body, the original page
    will be converted to markdown.

    Args:
        url (str): Url of article being scraped.

        content (str): Html source of the article page.

    Returns:
        Dictionary detailing the extracted article.
    """

    hostname = urlparse.urlparse(url).hostname
    spec = load_superdomains(hostname)

    # Pre-populate fields such as author and title using newspaper,
    # and return complete html page by default if newspaper does not work.
    result = newspaper.clean_source(url, content) or {"html": content}

    if spec is not None:
        # Instapaper scraper
        scraper = instapaper.InstapaperScraper(spec)
        for k, v in scraper.clean_article(content).items():
            if v:
                result[k] = v

    # Add markdown (and plaintext)
    h = html2text.HTML2Text()
    h.unicode_snob = True
    result['markdown'] = h.handle(result["html"])
    if include_html:
        result['markdown_html'] = markdown_to_html(result['markdown'])

    return result


def markdown_to_html(markdown):
    return Markup(markdown2.markdown(markdown))


def load_superdomains(hostname):
    """ Load the most specific spec file applicable to the given hostname.

    Peels off sub-hosts one at a time and searches for spec files defined for
    each level. Does not accept spec files that contain no rules.

    Args:
        hostname (str): Hostname for which to find an applicable spec file.
            The validity of the string as a hostname is not verified.

    Returns:
        The result of the first call to `load_sitespec` that succeeds,
        or `None` if no spec files were available for the given host.

        If `hostname` is invalid, the function will attempt to find a spec file
        matching it anyway, and return `None` if it fails.
    """

    try:
        d = load_sitespec(hostname)
    except IOError:
        d = {}

    # If `d` is empty, file for `hostname` could not be loaded or was empty;
    # in either case, we go on to the next superdomain.
    if not d:
        super_domain = hostname.partition(".")[2]
        if super_domain:
            return load_superdomains(super_domain)
        else:
            return None

    return d


def load_sitespec(hostname):
    """ Load sitespec file for a given host.

    Args:
        hostname (str): Hostname for which to load associated spec file.

    Raises:
        IOError if there is no sitespec file for the exact hostname.
    """

    fpath = os.path.join("sitespecs", hostname + ".txt")

    with io.open(fpath) as f:
        return load_rules(f)
