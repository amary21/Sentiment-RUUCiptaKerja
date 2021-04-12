from apps import db
from apps.models.dataset import Dataset
from apps.models.bobot_idf import BobotIdf
from apps.models.tfidf_pos import TFIDFPos
from apps.models.tfidf_neg import TFIDFNeg
from flask import Blueprint, render_template
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
    count_idf = db.session.query(func.count(BobotIdf.id_bobot)).scalar()
    return render_template('dashboard.html', contentheader='Dashboard', menu='Dashboard', menu_type='sidebar', dataset=count_dataset, neg_dataset=count_negatif_dataset, pos_dataset=count_positif_dataset, idf=count_idf)
