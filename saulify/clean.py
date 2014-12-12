from flask import Markup
from newspaper import Article
from xml.etree import ElementTree

import markdown2
import html2text


def clean_content(url_to_clean):

    article = Article(url_to_clean)
    article.download()
    article.parse()

    html_string = ElementTree.tostring(article.clean_top_node)
    markdown = html2text.HTML2Text().handle(html_string)
    article_html = Markup(markdown2.markdown(markdown))

    return {
        'html': article_html,
        'authors': str(', '.join(article.authors)),
        'title': article.title,
        'plaintext': markdown.replace('\n', ' '),
        'markdown': markdown
    }
