from __future__ import absolute_import

from newspaper import Article
from xml.etree import ElementTree


def clean_url(url_to_clean):
    """ Parse an article at a given url using newspaper.

    Args:
        url (str): Url where the article is found.

    Returns:
        Dictionary providing cleaned article and extracted content
        (see `construct_result`), or `None` if newspaper could not extract
        the article.
    """

    article = Article(url_to_clean)
    article.download()
    article.parse()

    if article.top_node is None:
        return None

    return construct_result(article)


def clean_source(url, source):
    """ Parse a pre-downloaded article using newspaper.

    Args:
        url (str): The url where the article was sourced (necessary for the
                newspaper API).

        source (str): Html source of the article page.

    Returns:
        Dictionary providing cleaned article and extracted content
        (see `construct_result`), or `None` if newspaper could not extract
        the article.
    """
    article = Article(url)
    article.set_html(source)
    article.parse()

    if article.top_node is None:
        return None

    return construct_result(article)


def construct_result(article):
    """ Construct article extraction result dictionary in standard format.

    Args:
        article (Article): A parsed `newspaper` `Article` object.

    Returns:
        Dictionary providing cleaned article and extracted content;
        author, title, markdown, plaintext, html.
    """

    html_string = ElementTree.tostring(article.clean_top_node)

    return {
        'html': html_string,
        'authors': str(', '.join(article.authors)),
        'title': article.title,
    }
