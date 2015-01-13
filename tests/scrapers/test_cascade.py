from saulify.scrapers.cascade import scraper_cascade


def test_cascade_runs():
    content = """<html><body><div>Article Content</div></body></html>"""
    scraper_cascade("http://example.com", content)
