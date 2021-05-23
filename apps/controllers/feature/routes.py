import pandas as pd

from apps import db

from apps.controllers.feature.feature_tf_idf import TfidfFeature

from apps.models.dataset import Dataset
from apps.models.feature import Feature

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required

feature = Blueprint('feature', __name__)


@feature.route('/feature')
@login_required
def view_df_idf_dict():
    count = db.session.query(Dataset.id_dataset).count()
    dataset = db.session.query(Dataset)
    data_feature = Feature.query.all()
    return render_template('feature.html', contentheader='Feature', menu='Feature', menu_type='sidebar', data=dataset, data_count=count, data_feature=data_feature)


@feature.route('/feature/process')
@login_required
def process_df_idf_dict():
    db.session.query(Feature).delete()
    data = db.session.query(Dataset)
    dataframe = pd.read_sql(data.statement, db.session.bind)
    feature = TfidfFeature()
    feature.set_tf_idf_dict(dataframe)
    flash('IDF has been processed!', 'success')
    return redirect(url_for('feature.view_df_idf_dict'))


@feature.route('/feature/deleteall')
@login_required
def deleteall():
    db.session.query(Feature).delete()
    db.session.commit()
    flash('Feature has been deleted!', 'success')
    return redirect(url_for('feature.view_df_idf_dict'))

