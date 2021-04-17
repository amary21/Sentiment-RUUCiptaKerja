from apps import db
from apps.models.dataset import Dataset
from apps.models.bobot_idf import BobotIdf
from apps.models.tfidf_pos import TFIDFPos
from apps.models.tfidf_neg import TFIDFNeg
from apps.controllers.bobot.bobot_tfidf import BobotTFIDF
from apps.controllers.bobot.features import Features
from apps.controllers.klasifikasi.naivebayes import NaiveBayes
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
import pandas as pd

bobot = Blueprint('bobot', __name__)


@bobot.route('/bobot')
@login_required
def bobot_idf():
    count = db.session.query(Dataset.id_dataset).count()
    data = db.session.query(Dataset)
    bobot = BobotIdf.query.all()

    feature = Features()
    data = db.session.query(Dataset)
    dataframe = pd.read_sql(data.statement, db.session.bind)
    # feature.set_tf_idf_dict(dataframe)
    ft = feature.calc_tf_idf(dataframe)

    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB

    x_train, x_test, y_train, y_test = train_test_split(ft, dataframe['sentimen'], test_size=0.2)
    nb = NaiveBayes()
    model = nb.fit(x_train, y_train)
    predict = nb.predict(x_test)

    # model = MultinomialNB().fit(x_train, y_train)
    # predict = model.predict(x_test)

    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, predict)
    print(cm)

    from sklearn.metrics import accuracy_score
    from sklearn.metrics import classification_report, confusion_matrix

    ac = accuracy_score(y_test, predict)
    print(ac)

    print(nb.score(x_test, y_test))

    return render_template('bobot_idf.html', contentheader='Bobot IDF', menu='Bobot', submenu='bobotidf', menu_type='sidebar', data=data, data_count=count, bobot=bobot)


@bobot.route('/bobot/process')
@login_required
def bobot_idf_process():
    bobot = BobotTFIDF()
    data = db.session.query(Dataset)
    dataframe = pd.read_sql(data.statement, db.session.bind)
    bobot.bobot_idf(dataframe)
    flash('IDF has been processed!', 'success')
    return redirect(url_for('bobot.bobot_idf'))


@bobot.route('/bobot/tfidf_positif')
@login_required
def tfidf_positif():
    bobot = BobotIdf.query.all()
    tfidf_pos = TFIDFPos.query.all()
    return render_template('bobot_tfidf_positif.html', contentheader='TF-IDF Positif', menu='Bobot', submenu='tfidfpos', menu_type='sidebar', bobot=bobot, tfidf_pos=tfidf_pos)


@bobot.route('/bobot/tfidf_positif/process')
@login_required
def tfidf_positif_process():
    bobot = BobotTFIDF()
    data = db.session.query(Dataset)
    dataframe = pd.read_sql(data.statement, db.session.bind)
    bobot.tfidf_positif(dataframe)
    flash('TF-IDF Positif has been processed!', 'success')
    return redirect(url_for('bobot.tfidf_positif'))


@bobot.route('/bobot/tfidf_negatif')
@login_required
def tfidf_negatif():
    bobot = BobotIdf.query.all()
    tfidf_neg = TFIDFNeg.query.all()
    return render_template('bobot_tfidf_negatif.html', contentheader='TF-IDF Negatif', menu='Bobot', submenu='tfidfneg', menu_type='sidebar', bobot=bobot, tfidf_neg=tfidf_neg)


@bobot.route('/bobot/tfidf_negatif/process')
@login_required
def tfidf_negatif_process():
    bobot = BobotTFIDF()
    data = db.session.query(Dataset)
    dataframe = pd.read_sql(data.statement, db.session.bind)
    bobot.tfidf_negatif(dataframe)
    flash('TF-IDF Negatif has been processed!', 'success')
    return redirect(url_for('bobot.tfidf_negatif'))
