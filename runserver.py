from saulify import app
from saulify.controllers import article

if __name__ == '__main__':
    app.register_blueprint(article.mod)
    app.run(host="0.0.0.0", port=5000, debug=True)
