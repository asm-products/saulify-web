from flask import Flask, request, render_template, redirect, url_for, Markup, \
    abort, jsonify
from newspaper import Article
from xml.etree  import ElementTree
import html2text
import markdown2
from functools import wraps

app = Flask(__name__)

APPKEY = 'd725f96372b0d7fc4f318b0f3cc17dcd80027cb91f79b2a69ff160d0'
#TODO: need user store functional for login, password, api_key, generate api_key


# The actual decorator function
def require_appkey(function):
    @wraps(function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == APPKEY:
            return function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clean')
def show_article():
    # TODO: Need to extract this to a module
    url_to_clean = request.args.get('u')
    if not url_to_clean:
        return redirect(url_for('index'))

    article = Article(url_to_clean)
    article.download()
    article.parse()
    html_string = ElementTree.tostring(article.clean_top_node)
    markdown = html2text.HTML2Text().handle(html_string)
    # TODO: Need to save the markdown, but just show it for now
    # Note: Markup marks it as html safe since we're rendering it from Markdown
    article_html = Markup(markdown2.markdown(markdown))
    a = {'html': article_html, 'authors': str(', '.join(article.authors)), 'title': article.title}
    return render_template('article/show.html', article=a, original=url_to_clean)


@app.route('/api')
@require_appkey
def api():
    # TODO: the same todo show_article() need to extract to a separate module
    url_to_clean = request.args.get('u')
    if not url_to_clean:
        return redirect(url_for('index'))

    article = Article(url_to_clean)
    article.download()
    article.parse()
    html_string = ElementTree.tostring(article.clean_top_node)
    markdown = html2text.HTML2Text().handle(html_string)
    # TODO: Need to save the markdown, but just show it for now
    # Note: Markup marks it as html safe since we're rendering it from Markdown
    article_html = Markup(markdown2.markdown(markdown))
    return jsonify({'title': article.title,
                    'authors': str(', '.join(article.authors)),
                    'html': article_html,
                    'plaintext': html_string,
                    'markdown': markdown})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
