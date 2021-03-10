from flask import Blueprint, render_template
from flask_login import login_required


dashboards = Blueprint('dashboards', __name__)


@dashboards.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', contentheader='Dashboard', menu='Dashboard', menu_type='sidebar')
