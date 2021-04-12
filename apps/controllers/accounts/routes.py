from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from apps import db
from apps.models.admin import Admin
from apps.controllers.accounts.form import LoginForm, UpdateUsernameForm, UpdatePasswordForm
from flask_login import login_user, current_user, logout_user, login_required
import hashlib


accounts = Blueprint('accounts', __name__)


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboards.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        hash_password = hashlib.md5(
            form.password.data.encode('utf-8')).hexdigest()
        admin = Admin.query.filter_by(
            username=form.username.data, password=hash_password).first()
        if admin:
            print(form.remember.data)
            login_user(admin, remember=form.remember.data)
            flash(f'Selamat Datang {form.username.data}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboards.dashboard'))
        else:
            flash('Username atau Password Salah!', 'danger')
    return render_template('login.html', contentheader='Login', title='Login', form=form)


@accounts.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@accounts.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form_username = UpdateUsernameForm()
    form_password = UpdatePasswordForm()
    if form_username.validate_on_submit():
        current_user.username = form_username.username.data
        db.session.commit()
        flash('Your username has been update!', 'success')
        return redirect(url_for('accounts.account'))
    elif form_password.validate_on_submit():
        hash_password = hashlib.md5(
            form_password.new_password.data.encode('utf-8')).hexdigest()
        current_user.password = hash_password
        db.session.commit()
        flash('Your password has been changed!', 'success')
        return redirect(url_for('accounts.account'))
    elif request.method == 'GET':
        form_username.username.data = current_user.username
    return render_template('account.html', contentheader='Account', menu_type='sidebar', form_username=form_username, form_password=form_password)
