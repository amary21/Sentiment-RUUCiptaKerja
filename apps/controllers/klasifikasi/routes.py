from apps import db
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
import pandas as pd

klasifikasi = Blueprint('klasifikasi', __name__)


@klasifikasi.route('/klasifikasi')
@login_required
def klasifikasi_func():
    return render_template('klasifikasi.html', contentheader='Klasifikasi', menu='klasifikasi', submenu='klasifikasi', menu_type='sidebar')
