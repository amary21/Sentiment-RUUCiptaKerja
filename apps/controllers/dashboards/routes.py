from apps import db

from apps.models.dataset import Dataset
from apps.models.feature import Feature

from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from sqlalchemy import func


dashboards = Blueprint('dashboards', __name__)


@dashboards.route("/dashboard")
@login_required
def dashboard():
    dataset = db.session.query(func.count(Dataset.id_dataset))
    count_dataset = dataset.scalar()
    count_negatif_dataset = dataset.filter(Dataset.sentimen == "0").scalar()
    count_positif_dataset = dataset.filter(Dataset.sentimen == "1").scalar()
    count_feature = db.session.query(func.count(Feature.id_feature)).scalar()
    return render_template('dashboard.html', contentheader='Dashboard', menu='Dashboard', menu_type='sidebar', dataset=count_dataset, neg_dataset=count_negatif_dataset, pos_dataset=count_positif_dataset, feature=count_feature)
