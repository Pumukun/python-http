from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from app.models import Database

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Nickname' }
    
    return render_template("index.html",
        title='Home', user=user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm() 

    if form.validate_on_submit():
        users_db = Database()
        users_db.add_user(form.username.data, form.password.data)

        flash('Login Username: "' + form.username.data + '", Password: "' + form.password.data + '" remember_me=' + str(form.remember_me.data))
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)
