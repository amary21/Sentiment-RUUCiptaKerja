from apps import db
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required

from apps.controllers.classification.naivebayes import NaiveBayes
from apps.controllers.feature.feature_tf_idf import TfidfFeature
from apps.controllers.classification.confus import performance, cloud

from apps.models.dataset import Dataset
from apps.models.feature import Feature
from apps.models.confusmatrix import ConfusMatrix
from apps.models.analysisresult import AnalysisResult

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split



classification = Blueprint('classification', __name__)


@classification.route('/classification/analysis')
@login_required
def analysis_func():
    #performance dengan confuss matrix
    data = db.session.query(AnalysisResult)
    df_analysis = pd.read_sql(data.statement, db.session.bind)
    accuracy, precision, recall = performance(df_analysis)

    #cek jumlah data negatif dan data positif
    dataset = db.session.query(db.func.count(Dataset.id_dataset))
    count_dataset = dataset.scalar()
    count_negatif_dataset = dataset.filter(Dataset.sentimen == "0").scalar()
    count_positif_dataset = dataset.filter(Dataset.sentimen == "1").scalar()

    #cek jumlah data latih dan data uji
    dataset = db.session.query(Dataset)
    df = pd.read_sql(dataset.statement, db.session.bind)
    x_train, x_test, _, _ = train_test_split(df['clean_tweet'], df['sentimen'], test_size=0.2, shuffle=False)

    return render_template('analysis.html', contentheader='Analysis', menu='classification',submenu='analysis', menu_type='sidebar', accuracy=accuracy, precision=precision, recall=recall, dataset=count_dataset, dataset_positive=count_positif_dataset, dataset_negative=count_negatif_dataset, data_train=len(x_train), data_test=len(x_test))


@classification.route('/classification/process')
@login_required
def analysis_process():
    #get dataset from db
    data = db.session.query(Dataset)
    dataframe = pd.read_sql(data.statement, db.session.bind)

    #get wordcloud from clean dataset
    cloud(dataframe['clean_tweet'])

    #split original dataset for insert data test to db
    _, x_tweet_test, _, _ = train_test_split(dataframe['tweet'], dataframe['sentimen'], test_size=0.2, shuffle=False)

    #split clean dataset for classification
    x_train, x_test, y_train, y_test = train_test_split(dataframe['clean_tweet'], dataframe['sentimen'], test_size=0.2, shuffle=False)
    #feature tf-idf
    tfidf = TfidfFeature()
    ft_train = tfidf.calc_tf_idf(x_train)
    ft_test = tfidf.calc_tf_idf(x_test)

    #classification with nbc
    nb = NaiveBayes()
    model = nb.fit(ft_train, y_train)
    predict = nb.predict(ft_test)

    #insert the result data into db, first delete the existing data
    db.session.query(AnalysisResult).delete()
    db.session.commit()
    y_test = np.array(y_test)
    for i, row in enumerate(x_tweet_test):
        result = AnalysisResult(tweet=row, analysis_manual=y_test[i], analysis_system=predict[i])
        db.session.add(result)
        db.session.commit()

    return redirect(url_for('classification.analysis_func'))


@classification.route('/classification/datatest_result')
@login_required
def datatest_func():
    data = AnalysisResult.query.all()
    return render_template('result.html', contentheader='Data Test Result', menu='classification',submenu='result', menu_type='sidebar', data=data)
