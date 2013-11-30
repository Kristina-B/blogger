# coding: utf-8
import datetime as dt

from sqlalchemy import create_engine
from flask import Flask, request, url_for, abort, redirect, render_template, flash, session

from blogger.models import Session, Post, Comment, User
from blogger.forms import RegistrationForm, LoginForm, PostForm, CommentForm

from flask_wtf.csrf import CsrfProtect

# Создание объекта Flask
app = Flask(__name__)
CsrfProtect(app)

# Загрузка параметров из файла settings.py
app.config.from_pyfile('settings.py')

# Создание engine. Engine - менеджер подключений к базе данных
engine = create_engine(app.config['DBURI'], echo=True)

# Привязка класса Session к существующему engine
Session.configure(bind=engine)

# Удаление сессии при остановке приложения
@app.teardown_appcontext
def teardown_db(exception):
    Session.remove()


@app.route('/login', methods=('GET', 'POST'))
def login():
    error = None
    dbs = Session()
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = dbs.query(User).filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user'] = {'id': user.id, 'username': user.username}
            return redirect(url_for('home'))

        error = 'Invalid username or password'

        # if request.form['username'] != app.config['LOGIN']:
        #     error = 'Invalid username'
        # elif request.form['password'] != app.config['PASSWORD']:
        #     error = 'Invalid password'
        # else:
        #     session['logged_in'] = True
        #     flash ('You were logged in successfully')
        #     return redirect(url_for('home'))
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    session.clear()
    flash('Good bye! See you later.')
    return redirect(url_for('home'))


#@app.route('/register', methods=['GET', 'POST'])
#def registration():
#    error = None
#    if request.method == 'POST':
#        dbs = Session()
#        user = dbs.query(User).filter(User.username == request.form['username']).first()
#        if user.username == request.form['username']:
#            flash ('Uppsss, we have already this user')
#            return redirect (url_for('login'))
#
#        dbs.add(user)
#        dbs.commit()
#        session['user_'id] = user.id
#        flash('Thanks for registration!')
#
#
#    return render_template('registration.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        dbs = Session()
        user = User(form.username.data, form.password.data)
        dbs.add(user)
        dbs.commit()
        session['user'] = {'id': user.id, 'username': user.username}

        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/')
def home():
    dbs = Session()
    posts = dbs.query(Post).order_by(Post.id).all()
    return render_template('home.html', posts=posts)


@app.route('/post/new', methods=['GET', 'POST'])
def add_post():
    form = PostForm(request.form)
    if not session.get('user'):
        abort(401)

    if request.method == 'GET':
        return render_template('new_post.html', form=form)

    dbs = Session()
    post = Post(title=request.form['title'],
                author_id=session['user']['id'],
                content=request.form['content'],
                created_at=dt.datetime.utcnow())
    dbs.add(post)
    dbs.commit()
    return redirect(url_for('home'))


@app.route('/post/<post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm(request.form)
    if not session.get('user'):
        abort(401)
    dbs = Session()
    post = dbs.query(Post).get(post_id)

    if request.method == 'GET':
        return render_template('edit_post.html', post=post, form=form)

    post.title = request.form['title']
    post.content = request.form['content']
    post.updated_at = dt.datetime.utcnow()
    dbs.commit()
    return redirect(url_for('home'))

@app.route('/post/<post_id>/delete')
def delete_post(post_id):
    if not session.get('user'):
        abort(401)
    dbs = Session()
    post = dbs.query(Post).get(post_id)
    dbs.delete(post)
    dbs.commit()
    flash('Post was deleted')
    return redirect(url_for('home'))

@app.route('/post/<post_id>/')
def show_post(post_id):
    dbs = Session()
    post = dbs.query(Post).get(post_id)
    if post is None:
        abort(404)
    return render_template ('show_post.html', post=post)

@app.route('/post/<post_id>/add_comment/', methods=['GET', 'POST'])
def add_comment(post_id):
    form = CommentForm(request.form)
    dbs = Session()
    post = dbs.query(Post).get(post_id)

    if request.method == 'GET':
        return render_template('add_comment.html', post=post, form=form)
    
    comment = Comment(
        content=request.form['content'],
        created_at=dt.datetime.utcnow())
    post.comments.append(comment)
    dbs.commit()
    flash('Comment was added to post')
    return redirect(url_for('show_post', post_id=post.id))

@app.errorhandler(404)
def page_not_found(error):
    return render_template ('error_404.html'), 404

@app.errorhandler(400)
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400

if __name__ == '__main__':
    app.run(port=8000, debug=True)