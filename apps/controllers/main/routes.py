from apps import db

from flask import Blueprint, render_template
from apps.models.dataset import Dataset
from apps.controllers.analysis.confus import performance

import pandas as pd
from sklearn.model_selection import train_test_split

main = Blueprint('main', __name__)


@main.route("/")
def index():

    accuracy, precision, recall = performance()

    dataset = db.session.query(db.func.count(Dataset.id_dataset))
    count_dataset = dataset.scalar()
    count_negatif_dataset = dataset.filter(Dataset.sentimen == "0").scalar()
    count_positif_dataset = dataset.filter(Dataset.sentimen == "1").scalar()

    dataset = db.session.query(Dataset)
    df = pd.read_sql(dataset.statement, db.session.bind)

    x_train, x_test, _, _ = train_test_split(
        df['clean_tweet'], df['sentimen'], test_size=0.2)
    return render_template('index.html', menu_type='topbar', accuracy=accuracy, precision=precision, recall=recall, dataset=count_dataset, dataset_positive=count_positif_dataset, dataset_negative=count_negatif_dataset, data_train=len(x_train), data_test=len(x_test))
