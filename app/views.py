from flask import render_template, flash, redirect, request
from app import app, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import Database, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.csv_reader import CsvReader

users_db = Database()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Home')


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User()
        user.id = users_db.sign_in(form.username.data, form.password.data)
        user.username = form.username.data

        if user.id == -1:
            flash('Login Incorrect')
        else:
            login_user(user, remember=form.remember_me.data)
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


@app.route('/csv_app', methods=['GET', 'POST'])
def csv_app():
    checkbox_sort = request.form.get('checkbox_sort')

    if request.method == 'POST':
        files = []

        for filename in request.files.getlist('file'):
            f = filename
            f.save(secure_filename(f.filename))
            files.append(filename.filename)
        
        menu_item = request.form.get('select-menu')

        if (menu_item != None):
            reader = CsvReader(files[menu_item])     
            csv_html_table = reader.csv_to_html()
        else:
            csv_html_table=''
        return render_template('csv_app.html', title='CSV App', files=files, csv_html_table=csv_html_table)
    
    return render_template('csv_app.html', title='CSV App')

