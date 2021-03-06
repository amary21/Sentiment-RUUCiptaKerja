from flask import Flask, render_template, url_for, flash, redirect, request
from apps import app, db
from apps.models.admin import Admin
from apps.controllers.login import LoginForm
from flask_login import login_user, current_user, logout_user, login_required
# from werkzeug.security import generate_password_hash, check_password_hash
import hashlib


@app.route("/")
def index():
    return render_template('index.html', menu='topbar')


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', contentheader='Dashboard', menu='sidebar')


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
