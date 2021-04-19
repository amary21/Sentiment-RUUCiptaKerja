from apps import db
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required

from apps.controllers.analysis.naivebayes import NaiveBayes
from apps.controllers.feature.feature_tf_idf import TfidfFeature
from apps.controllers.analysis.confus import performance, cloud

from apps.models.dataset import Dataset
from apps.models.feature import Feature
from apps.models.confusmatrix import ConfusMatrix

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix



analysis = Blueprint('analysis', __name__)


@analysis.route('/analysis')
@login_required
def analysis_func():
    accuracy, precision, recall = performance()

    dataset = db.session.query(db.func.count(Dataset.id_dataset))
    count_dataset = dataset.scalar()
    count_negatif_dataset = dataset.filter(Dataset.sentimen == "0").scalar()
    count_positif_dataset = dataset.filter(Dataset.sentimen == "1").scalar()

    dataset = db.session.query(Dataset)
    df = pd.read_sql(dataset.statement, db.session.bind)

    x_train, x_test, _, _ = train_test_split(df['clean_tweet'], df['sentimen'], test_size=0.2)

    return render_template('analysis.html', contentheader='Analysis', menu='analysis', menu_type='sidebar', accuracy=accuracy, precision=precision, recall=recall, dataset=count_dataset, dataset_positive=count_positif_dataset, dataset_negative=count_negatif_dataset, data_train=len(x_train), data_test=len(x_test))


@analysis.route('/analysis/process')
@login_required
def analysis_process():
    data = db.session.query(Dataset)
    dataframe = pd.read_sql(data.statement, db.session.bind)
    cloud(dataframe['clean_tweet'])

    tfidf = TfidfFeature()
    ft = tfidf.calc_tf_idf(dataframe)

    x_train, x_test, y_train, y_test = train_test_split(ft, dataframe['sentimen'], test_size=0.2)

    nb = NaiveBayes()
    model = nb.fit(x_train, y_train)
    predict = nb.predict(x_test)

    cm = confusion_matrix(y_test, predict)
    print('confusion matrix =', cm)
    print('TP =', type(int(cm[0][0])))
    print('FP =', cm[0][1])
    print('FN =', cm[1][0])
    print('TN =', cm[1][1])

    data_cm = ConfusMatrix(true_positive=int(cm[0][0]), false_positive=int(cm[0][1]), false_negative=int(cm[1][0]), true_negative=int(cm[1][1]))
    db.session.add(data_cm)
    db.session.commit()

    ac = accuracy_score(y_test, predict)
    print('accuracy =', ac)

    print('score =', nb.score(x_test, y_test))

    return redirect(url_for('analysis.analysis_func'))
