import datetime
import hashids
from saulify import models

def test_create_article():
    url = "http://example.com/"
    title = "An Example Site."
    authors = "W3C"
    markdown = "*cool*"

    article = models.Article(url, title, authors, markdown)

    assert article.url == url
    assert article.title == title
    assert article.authors == authors
    assert article.markdown == markdown
    assert article.updated == None


def test_updated_date_is_set_when_article_is_saved(app):

    article = models.Article('a', 'b', 'c', 'd')
    article.put()

    #time passes during tests, so we can't be really accurate with times.
    #mocking out utcnow gives problems when saving.
    onesecago = datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
    assert onesecago < article.updated < datetime.datetime.utcnow()


def test_create_and_get_by_slug(app):
    article = models.Article('a', 'b', 'c', 'd')
    article.put()

    assert article.get_slug() == hashids.Hashids().encode(article.id)
    assert models.Article.get_by_slug(article.get_slug())