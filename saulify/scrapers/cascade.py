import io
import os
import urlparse

import html2text

from . import download
from . import instapaper
from . import newspaper

from saulify.sitespec import load_rules


def clean_url(url):
    """ Extract article from given url using `scraper_cascade`

    Args:
        url (str): Url of article to be scraped.

    Returns:
        Dictionary detailing the extracted article.
    """

    content = download.download_url(url)
    result = scraper_cascade(url, content)

    return result


def scraper_cascade(url, content):
    """ Extract article using a fallback sequence of scrapers.

    Args:
        url (str): Url of article being scraped.

        content (str): Html source of the article page.

    Returns:
        Dictionary detailing the extracted article, or `None` if no scrapers
        could extract the article
    """

    hostname = urlparse.urlparse(url).hostname
    spec = load_superdomains(hostname)

    if spec is not None:
        # Instapaper scraper
        scraper = instapaper.InstapaperScraper(spec)
        result = scraper.clean_article(content)
    else:
        # Fallback: newspaper
        result = newspaper.clean_source(url, content)

    if result is None:
        return None

    # Add markdown (and plaintext)
    result["markdown"] = html2text.HTML2Text().handle(result["html"])
    # TODO: Investigate the most apropriate method of converting markdown
    # to plaintext.
    result["plaintext"] = result["markdown"].replace('\n', ' ')

    return result


def load_superdomains(hostname):
    """ Load the most specific spec file applicable to the given hostname.

    Peels off sub-hosts one at a time and searches for spec files defined for
    each level.

    Args:
        hostname (str): Hostname for which to find an applicable spec file.

    Returns:
        The result of the first call to `load_sitespec` that succeeds,
        or `None` if no spec files were available for the given host.
    """

    try:
        return load_sitespec(hostname)
    except IOError:
        super_domain = hostname.partition(".")[2]
        if super_domain:
            return load_superdomains(super_domain)
        else:
            return None


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
