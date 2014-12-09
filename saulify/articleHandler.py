__author__ = 'adriano'
from flask import current_app

'''
Article handler module. Will handle the add hashing of the url, as well as saving and
restoring of content

It is created as a flask extension.
'''

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class ArticleHandler(object):
    '''
    Handle shortening of urls
    '''
    def __init__(self, app=None, db=None, redis=none):
        '''
        Initialize the class with the app that will be used later

        :param app: Flask app
        :param db: overwrite app db
        :param redis:
        :return: None
        '''
        self.app = app
        if app is not None:
            self.init_app(app)

        def init_app(self, app):
            # Use the newstyle teardown_appcontext if it's available,
            # otherwise fall back to the request context
            if hasattr(app, 'teardown_appcontext'):
                app.teardown_appcontext(self.teardown)
            else:
                app.teardown_request(self.teardown)

        def teardown(self, exception):
            ctx = stack.top
            if hasattr(ctx, 'short'):
                ctx.sqlite3_db.close()