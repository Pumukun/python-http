from flask import render_template, flash, redirect, request
from app import app, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import Database, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


users_db = Database()


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title='Home')


@login_manager.user_loader
def load_user(user_id):
    return User().from_db(user_id, users_db)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = users_db.sign_in(form.username.data, form.password.data)
        
        user_login = User().create(user)

        if user == -1:
            flash('Login Incorrect')
        else:
            login_user(user_login, remember=form.remember_me.data)
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = 'index'
            return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        users_db = Database()
        user_ID = users_db.sign_in(form.username.data, form.password.data)

        if user_ID == -1:
            users_db.add_user(form.username.data, form.password.data)
            return redirect('/index')
        else:
            flash('User: "' + form.username.data + '" Already exists')

    return render_template('register.html', title='Register', form=form)
