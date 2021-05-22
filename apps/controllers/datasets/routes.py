import os
import pandas as pd

from apps import db, celery, ROOT_DIR

from apps.models.dataset import Dataset
from apps.models.feature import Feature
from apps.models.analysisresult import AnalysisResult

from apps.controllers.datasets.form import DataTrainForm, UpdateDataTrainForm, DataCSVForm, ViewDataTrainForm
from apps.controllers.datasets.preprocessing import Preprocessing

from flask import Blueprint, render_template, url_for, flash, redirect, request, make_response, jsonify
from flask_login import current_user, login_required


datasets = Blueprint('datasets', __name__)


@datasets.route('/dataset', methods=['GET', 'POST'])
@login_required
def datatrain():
    data = Dataset.query.all()

    form_adddataset = DataTrainForm()
    form_updatedataset = UpdateDataTrainForm()
    form_importdataset = DataCSVForm()
    form_viewdataset = ViewDataTrainForm()

    return render_template('dataset.html', contentheader='Dataset', menu='Dataset', menu_type='sidebar', dataset=data, form_adddataset=form_adddataset, form_updatedataset=form_updatedataset, form_importdataset=form_importdataset, form_viewdata=form_viewdataset)


@datasets.route('/dataset/upload', methods=['POST'])
@login_required
def datatrain_upload():
    stream = request.files['csv_file']
    df = pd.read_csv(stream)
    df.to_csv(ROOT_DIR + '/static/assets/files/datasets.csv')
    result = task_upload.apply_async()
    print(result)
    # result.wait()
    flash('Dataset has been imported', 'success')
    return jsonify({}), 202, {'Location': url_for('datasets.dataset_upload_stat', task_id=result.id)}


@datasets.route('/dataset/upload/status/<task_id>', methods=['GET'])
def dataset_upload_stat(task_id):
    task = task_upload.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
        }
    return jsonify(response)
    

@celery.task()
def task_upload():
    dir_path = os.path.abspath(ROOT_DIR + '/static/assets/files/datasets.csv')
    preprocessing = Preprocessing()
    preprocessing.from_csv(dir_path, 1)
    return {'result': 'success'}


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
