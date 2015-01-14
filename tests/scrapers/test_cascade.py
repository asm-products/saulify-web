from saulify.scrapers.cascade import scraper_cascade

def _assert_html_to_markdown(html, markdown):
    assert scraper_cascade("http://example.com", html).get('markdown') == markdown


def test_cascade_runs():
    content = """<html><body><div>Article Content</div></body></html>"""
    scraper_cascade("http://example.com", content)


def test_cascade_markdown_headers():
    for i in xrange(1, 7):
        content = '<h{0}>import antigravity</h{0}>'.format(i)
        markdown = "#" * i + ' import antigravity\n\n'
        _assert_html_to_markdown(content, markdown)


def test_cascade_markdown_blockquote():
    html = '<blockquote>So long, and thanks for all the fish!</blockquote>'
    markdown = '> So long, and thanks for all the fish!\n\n'
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_unordered_list():
    html = '<ul><li>Ruby<ul><li>Gem</li><li>Stuff</li></ul></li><li>Objective-C</li></ul>'
    markdown = '  * Ruby\n    * Gem\n    * Stuff\n  * Objective-C\n\n'
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_ordered_list():
    html = '<ol><li>World Domination<ol><li>Python</li><li>...</li><li>Profit!</li></ol></li><li>Swim in money</li></ol>'
    markdown = '  1. World Domination\n    1. Python\n    2. ...\n    3. Profit!\n  2. Swim in money\n\n'
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_code_block():
    html = '<pre>print "Hello Ada Lovelace"</pre>'
    markdown = '\n    print "Hello Ada Lovelace"\n\n'
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_horizontal_rule():
    _assert_html_to_markdown("<hr/>", "* * *\n\n")


def test_cascade_markdown_link():
    html ='<a href="http://xkcd.com/353/">import antigravity</a>'
    markdown = '[import antigravity](http://xkcd.com/353/)\n\n'
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_emphasis():
    html = '<em>Important</em>'
    markdown = '_Important_\n\n'
    _assert_html_to_markdown(html, markdown)

    html = '<b>Important</b>'
    markdown = '**Important**\n\n'
    _assert_html_to_markdown(html, markdown)

    html = '<strong>Important</strong>'
    _assert_html_to_markdown(html, markdown)

    html = "<b><i>important</i></b>"
    markdown = "**_important_**\n\n"
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_underline():
    html = '<u>Over the line!</u>'
    markdown = '_Over the line!_\n\n'
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_bold_underline():
    html = "<u><b>OVER THE LINE!</b></u>\n\n"
    markdown = "_**OVER THE LINE!**_\n\n"
    _assert_html_to_markdown(html, markdown)

    html = '<b><u>underline</u></b>'
    markdown = '**_underline_**\n\n'
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_code():
    html = '<code>assert life & universe & everything == 42</code>'
    markdown = "`assert life & universe & everything == 42`\n\n"
    _assert_html_to_markdown(html, markdown)


def test_cascade_markdown_image():
    html = '<img src="http://imgur.com/witty.png">'
    markdown = '![](http://imgur.com/witty.png)\n\n'
    _assert_html_to_markdown(html, markdown)

    html = '<img alt="witty" src="http://imgur.com/witty.png">'
    markdown = '![witty](http://imgur.com/witty.png)\n\n'
    _assert_html_to_markdown(html, markdown)
