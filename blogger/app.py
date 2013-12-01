# coding: utf-8
import datetime as dt

from flask import Flask, request, url_for, abort, redirect, \
    render_template, flash, session

#noinspection PyUnresolvedReferences
from flask.ext.sqlalchemy import SQLAlchemy
#noinspection PyUnresolvedReferences
from flask.ext.wtf import CsrfProtect

from blogger.models import db, Post, Comment, User
from blogger.forms import RegistrationForm, LoginForm, PostForm, CommentForm

# Создание объекта Flask
app = Flask(__name__)

# Загрузка параметров из файла settings.py
app.config.from_pyfile('settings.py')

CsrfProtect(app)
db.init_app(app)



@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user'] = {'id': user.id, 'username': user.username}
            return redirect(url_for('home'))

        error = 'Invalid username or password'

    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.clear()
    flash('Good bye! See you later.')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        session['user'] = {'id': user.id, 'username': user.username}

        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id).all()
    return render_template('home.html', posts=posts)


@app.route('/post/new', methods=['GET', 'POST'])
def add_post():
    form = PostForm(request.form)
    if not session.get('user'):
        abort(401)

    if request.method == 'GET':
        return render_template('new_post.html', form=form)

    post = Post(title=request.form['title'],
                content=request.form['content'],
                author_id=session['user']['id'],
                created_at=dt.datetime.utcnow())
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/post/<post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm(request.form)
    if not session.get('user'):
        abort(401)
    post = Post.query.get(post_id)

    if request.method == 'GET':
        return render_template('edit_post.html', post=post, form=form)

    post.title = request.form['title']
    post.content = request.form['content']
    post.updated_at = dt.datetime.utcnow()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/post/<post_id>/delete')
def delete_post(post_id):
    if not session.get('user'):
        abort(401)
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post was deleted')
    return redirect(url_for('home'))


@app.route('/post/<post_id>/')
def show_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        abort(404)
    return render_template('show_post.html', post=post)


@app.route('/post/<post_id>/add_comment/', methods=['GET', 'POST'])
def add_comment(post_id):
    form = CommentForm(request.form)
    post = Post.query.get(post_id)

    if request.method == 'GET':
        return render_template('add_comment.html', post=post, form=form)

    user_id = session.get('user', {}).get('id')

    comment = Comment(
        content=request.form['content'],
        author_id=user_id,
        created_at=dt.datetime.utcnow())

    post.comments.append(comment)
    db.session.commit()
    flash('Comment was added to post')
    return redirect(url_for('show_post', post_id=post.id))


#noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404


@app.errorhandler(400)
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400


if __name__ == '__main__':
    app.run(port=8000, debug=True)