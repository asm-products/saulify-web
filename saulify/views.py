from flask import request, render_template, redirect, url_for, Markup, \
    abort, jsonify, g, flash, make_response, current_app, session
from newspaper import Article
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from flask.ext.principal import Permission, RoleNeed, Identity, \
    AnonymousIdentity, identity_changed, UserNeed, identity_loaded
from saulify import app, login_manager, db, principals
from models import User
from xml.etree import ElementTree
import html2text
import markdown2
from functools import wraps
from common import api_key_gen, ratelimit, get_rate_limit, LIMIT_METHOD_USER, LIMIT_METHOD_API
from forms import AdUserForm
import json


MEMBER = 100
ADMIN = 101
admin = Permission(RoleNeed('admin'))



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user
    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if current_user.role == MEMBER:
            identity.provides.add(RoleNeed('member'))
        if current_user.role == ADMIN:
            identity.provides.add(RoleNeed('admin'))


@app.before_request
def before_request():
    g.user = current_user


def createkey(user):
    user.api_key = api_key_gen()
    db.session.commit()


def revokekey(user):
    user.api_key = None
    db.session.commit()


@app.route('/dashboard', methods=['GET', 'POST'])
@admin.require(401)
def dashboard():
    form = AdUserForm(request.form)
    users = User.query.filter_by(role=100).all()
    return render_template('dashboard.html',
                           users=users, form=form)


@app.route('/adduser', methods=['POST'])
@admin.require(401)
def add_user():
    form = AdUserForm(request.form)
    if form.validate():
        result = {}
        result['iserror'] = False
        if not form.id.data:
            if True:
                newuser = User(email=form.email.data)
                newuser.hash_password(form.password.data)
                db.session.add(newuser)
                db.session.commit()
                result['savedsuccess'] = True
            else:
                result['savedsuccess'] = False
            return json.dumps(result)
        else:
            edituser = User.query.get(form.id.data)
            edituser.email = form.email.data
            edituser.hash_password(form.password.data)
            db.session.commit()
            result['savedsuccess'] = True
            return json.dumps(result)
    else:
        form.errors['iserror'] = True
        print form.errors
        return json.dumps(form.errors)


@app.route('/user/<id>', methods=['GET', 'DELETE'])
@admin.require(401)
def user_mod(id):
    user = User.query.get(id)
    if request.method == 'GET':
        return jsonify({"id": user.id,
                        "email": user.email})
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        result = {}
        result['result'] = 'success'
        return jsonify(result)


@app.route('/dashboard/key/<int:user_id>', methods=['PUT', 'POST'])
@admin.require(401)
def dash_createkey(user_id):
    user = User.query.get(user_id)
    createkey(user)
    return jsonify({"result": "success"})


@app.route('/dashboard/key/<int:user_id>', methods=['DELETE'])
@admin.require(401)
def dash_revokekey(user_id):
    user = User.query.get(user_id)
    revokekey(user)
    return jsonify({"result": "success"})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email).first()
    if not registered_user or not registered_user.verify_password(password):
        flash('Email or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(current_user.id))
    flash('Logged in successfully')
    if registered_user.role == ADMIN:
        return redirect(url_for('dashboard'))
    return redirect(url_for('user'))


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    user = g.user
    return render_template('user.html',
                           user=user)


@app.route('/user/key', methods=['PUT', 'POST'])
@login_required
def user_createkey():
    createkey(g.user)
    return jsonify({"result": "success"})


@app.route('/user/key', methods=['DELETE'])
@login_required
def user_revokekey():
    revokekey(g.user)
    return jsonify({"result": "success"})


@app.route('/logout')
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('index'))


# The actual decorator function
def require_appkey(function):
    @wraps(function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and \
           User.query.filter_by(api_key=request.args.get('key')).first():
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
    a = {'html': article_html,
         'authors': str(', '.join(article.authors)),
         'title': article.title}
    return render_template('article/show.html',
                           article=a,
                           original=url_to_clean)


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
                    'plaintext': markdown.replace('\n', ' '),
                    'markdown': markdown})


@app.errorhandler(401)
def unauthorized(error):
    return 'Please login as admin to see this page'
    # TODO: template 401 unauthorised


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.after_request
def inject_x_rate_headers(response):
    '''
    Add headers before responding to user
    .'''
    limit = get_rate_limit()
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response
