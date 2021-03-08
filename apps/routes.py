from flask import Flask, render_template, url_for, flash, redirect, request
from apps import app, db
from apps.models.admin import Admin
from apps.controllers.account import LoginForm, UpdateUsernameForm, UpdatePasswordForm
from flask_login import login_user, current_user, logout_user, login_required
# from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


@app.route("/")
def index():
    return render_template('index.html', menu_type='topbar')


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', contentheader='Dashboard', menu='Dashboard', menu_type='sidebar')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        hash_password = hashlib.md5(
            form.password.data.encode('utf-8')).hexdigest()
        admin = Admin.query.filter_by(
            username=form.username.data, password=hash_password).first()
        if admin:
            login_user(admin, remember=form.remember.data)
            flash(f'Selamat Datang {form.username.data}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Username atau Password Salah!', 'danger')
    return render_template('login.html', contentheader='Login', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form_username = UpdateUsernameForm()
    form_password = UpdatePasswordForm()
    if form_username.validate_on_submit():
        current_user.username = form_username.username.data
        db.session.commit()
        flash('Your username has been update!', 'success')
        return redirect(url_for('account'))
    elif form_password.validate_on_submit():
        hash_password = hashlib.md5(
            form_password.new_password.data.encode('utf-8')).hexdigest()
        current_user.password = hash_password
        db.session.commit()
        flash('Your password has been changed!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form_username.username.data = current_user.username
    return render_template('account.html', contentheader='Account', menu_type='sidebar', form_username=form_username, form_password=form_password)


@app.route('/datatrain')
@login_required
def datatrain():
    return render_template('data_train.html', contentheader='Data Train', menu='Dataset', submenu='datatrain', menu_type='sidebar')


@app.route('/datatest')
@login_required
def datatest():
    return render_template('data_test.html', contentheader='Data Test', menu='Dataset', submenu='datatest', menu_type='sidebar')
