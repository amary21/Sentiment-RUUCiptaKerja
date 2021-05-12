import io
import pandas as pd

from apps import db

from apps.models.dataset import Dataset
from apps.models.feature import Feature
from apps.models.analysisresult import AnalysisResult

from apps.controllers.datasets.form import DataTrainForm, UpdateDataTrainForm, DataCSVForm, ViewDataTrainForm
from apps.controllers.datasets.preprocessing import Preprocessing

from flask import Blueprint, render_template, url_for, flash, redirect, request, make_response
from flask_login import current_user, login_required


datasets = Blueprint('datasets', __name__)


@datasets.route('/dataset', methods=['GET', 'POST'])
@login_required
def datatrain():
    print('id user', current_user.id_user)
    data = Dataset.query.all()
    preprocessing = Preprocessing()

    form_adddataset = DataTrainForm()
    form_updatedataset = UpdateDataTrainForm()
    form_importdataset = DataCSVForm()
    form_viewdataset = ViewDataTrainForm()

    if form_importdataset.validate_on_submit():
        file_name = form_importdataset.csv_file.data
        stream = io.StringIO(
            file_name.stream.read().decode("UTF8"), newline=None)
        preprocessing.from_csv(stream, current_user.id_user)
        flash('Dataset has been imported', 'success')
        return redirect(url_for('datasets.datatrain'))

    return render_template('dataset.html', contentheader='Dataset', menu='Dataset', menu_type='sidebar', dataset=data, form_adddataset=form_adddataset, form_updatedataset=form_updatedataset, form_importdataset=form_importdataset, form_viewdata=form_viewdataset)


@datasets.route('/dataset/deleteall')
@login_required
def datatrain_deleteall():
    db.session.query(Dataset).delete()
    db.session.query(Feature).delete()
    db.session.query(AnalysisResult).delete()
    db.session.commit()
    flash('Dataset has been deleted!', 'success')
    return redirect(url_for('datasets.datatrain'))

@datasets.route('/dataset/download')
@login_required
def download_csv():
    data = db.session.query(Dataset)
    df = pd.read_sql(data.statement, db.session.bind)
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export_dataset.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
