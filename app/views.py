from flask import render_template, flash, redirect, request, send_file, jsonify
from app import app, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import Database, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.csv_reader import CsvReader
import os
import glob

users_db = Database()

# main route
@app.route('/')
@app.route('/index')
def index() -> str:
    return render_template("index.html", title='Home')


# login and registration
@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login() -> str:
    form = LoginForm()

    if form.validate_on_submit():
        user_id = users_db.sign_in(form.username.data, form.password.data)
        user = User(user_id)

        if user_id == -1:
            flash('Login Incorrect')
        else:
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully.')
            next_page: str = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = 'index'
            return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout() -> str:
    logout_user()
    return redirect('index')

@app.route('/register', methods=['GET', 'POST'])
def register() -> str:
    form = RegisterForm()

    if form.validate_on_submit():
        users_db = Database()
        user_ID: int = users_db.sign_in(form.username.data, form.password.data)

        if user_ID == -1:
            users_db.add_user(form.username.data, form.password.data)
            return redirect('/index')
        else:
            flash('User: "' + form.username.data + '" Already exists')

    return render_template('register.html', title='Register', form=form)


# Profile
@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile() -> str:
    return render_template('profile.html', title='Profile')

# file upload and download
@app.route('/upload', methods=['GET', 'POST'])
def csv_upload() -> str:
    if request.method == 'POST':
        files: list[str] = []

        for filename in request.files.getlist('file'):
            f = filename

            if f.filename == '':
                flash('No files selected!')
                return redirect(request.url)

            f.save(f"{app.config['UPLOAD_FOLDER']}/{f.filename}")
            files.append(filename.filename)

        return redirect('csv_app')

    return render_template('upload.html')

@app.route('/download/<name>', methods=['GET', 'POST'])
def download_file(name):
    return send_file(f'static/tmp_upload/{name}')


# csv app
@app.route('/csv_app', methods=['GET', 'POST'])
def csv_app() -> str:

    files: list[str] = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('csv_app.html', title='CSV App', files=files)

# API
@app.route('/api/set_table/<uuid>', methods=['POST', 'GET'])
def set_table(uuid):
    content = request.get_json(silent=True)
    reader = CsvReader(app.config['UPLOAD_FOLDER'] + '/' + content["table"])
    csv_html = reader.csv_to_html()
    csv_columns = reader.get_columns()

    result_dict: dict = {
        "csv_table": csv_html,
        "columns": csv_columns
    }
    return jsonify(result_dict)

@app.route('/api/update_table/<uuid>', methods=['POST', 'GET'])
def update_table(uuid):
    content = request.get_json(silent=True)
    reader = CsvReader(app.config['UPLOAD_FOLDER'] + '/' + content['table'])
    csv_html = reader.sel_columns(content["sel_columns"])

    result_dict: dict = {
        "csv_table": csv_html
    }

    return jsonify(result_dict)

@app.route('/api/delete_file/<uuid>', methods=['GET', 'POST'])
def delete_file(uuid):
    content = request.get_json(silent=True)
    os.remove(f'{app.config["UPLOAD_FOLDER"]}/{content["sel_table"]}')

    return {"success": 1}

@app.route('/api/delete_all_files/', methods=['GET', 'POST'])
def delete_all_files():
    content = request.get_json(silent=True)

    files = glob.glob(app.config["UPLOAD_FOLDER"] + "/*")
    for f in files:
        os.remove(f)

    return {"success": 1}

