from flask import Flask, request, render_template, redirect, url_for, Markup
from newspaper import Article
from xml.etree  import ElementTree
import html2text
import markdown2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/articles/create', methods=['POST'])
def create_article():
    url_to_clean = request.form['url_to_clean']
    if not url_to_clean:
        return redirect(url_for('index'))
    return redirect(url_for('show_article', url_to_clean=url_to_clean))

@app.route('/articles/show')
def show_article():
    # TODO: Need to extract this to a module
    article = Article(request.args.get('url_to_clean'))
    article.download()
    article.parse()
    html_string = ElementTree.tostring(article.clean_top_node)
    markdown = html2text.HTML2Text().handle(html_string)
    # TODO: Need to save the markdown, but just show it for now
    # Note: Markup marks it as html safe since we're rendering it from Markdown
    article_html = Markup(markdown2.markdown(markdown))
    a = {'html': article_html, 'authors': str(', '.join(article.authors)), 'title': article.title}
    return render_template('article/index.html', article=a)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
