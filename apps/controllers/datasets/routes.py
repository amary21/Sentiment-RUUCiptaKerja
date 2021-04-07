from apps import db
from apps.models.dataset import Dataset
from apps.controllers.datasets.form import DataTrainForm, UpdateDataTrainForm, DataCSVForm
from apps.controllers.datasets.convert_csv import LoadData
from flask import Blueprint, request
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
import csv


datasets = Blueprint('datasets', __name__)


@datasets.route('/datatrain', methods=['GET', 'POST'])
@login_required
def datatrain():
    data = Dataset.query.all()

    form_adddataset = DataTrainForm()
    form_updatedataset = UpdateDataTrainForm()
    form_importdataset = DataCSVForm()

    if form_adddataset.validate_on_submit():
        add_data = Dataset(id_admin=current_user.id_admin, tweet=form_adddataset.tweet.data, sentimen=form_adddataset.sentiment.data)
        db.session.add(add_data)
        db.session.commit()
        flash('Dataset has been added', 'success')
        return redirect(url_for('datasets.datatrain'))

    if form_updatedataset.validate_on_submit():
        id = form_updatedataset.update_id.data
        datatrain = Dataset.query.get_or_404(id)
        datatrain.tweet = form_updatedataset.update_tweet.data
        datatrain.sentimen = form_updatedataset.update_sentiment.data
        db.session.commit()
        flash('Dataset has been updated', 'success')
        return redirect(url_for('datasets.datatrain'))

    if form_importdataset.validate_on_submit():
        # filename = form_importdataset.csv_file.data
        # csv_data = csv.reader(filename)
        # for row in csv_data:
        #     print(row)

        # file_data = LoadData(filename)
        # print(file_data)

        flash('Dataset has been imported', 'success')
        return redirect(url_for('datasets.datatrain'))

    return render_template('data_train.html', contentheader='Data Train', menu='Dataset', submenu='datatrain', menu_type='sidebar', dataset=data, form_adddataset=form_adddataset, form_updatedataset=form_updatedataset, form_importdataset=form_importdataset)


# @datasets.route('/datatrain/new', methods=['GET', 'POST'])
# @login_required
# def datatrain_create():
#     form = DataTrainForm()
#     if form.validate_on_submit():
#         data = Dataset(id_admin=current_user.id_admin,
#                         tweet=form.tweet.data, sentimen=form.sentiment.data)
#         db.session.add(data)
#         db.session.commit()
#         flash('Dataset has been added', 'success')
#         return redirect(url_for('datasets.datatrain'))
#     return render_template('data_train_form.html', contentheader='Add New Data Train', menu='Dataset', submenu='datatrain', menu_type='sidebar', form=form)


# @datasets.route('/datatrain/update', methods=['GET', 'POST'])
# @login_required
# def datatrain_update():
#     id = request.args.get('id')
#     datatrain = Dataset.query.get_or_404(id)
#     form = DataTrainForm()
#     if form.validate_on_submit():
#         datatrain.tweet = form.tweet.data
#         datatrain.sentimen = form.sentiment.data
#         db.session.commit()
#         flash('Dataset has been updated', 'success')
#         return redirect(url_for('datasets.datatrain'))
#     elif request.method == 'GET':
#         form.tweet.data = datatrain.tweet
#         form.sentiment.data = datatrain.sentimen
#     return render_template('data_train_form.html', contentheader='Add New Data Train', menu='Dataset', submenu='datatrain', menu_type='sidebar', form=form)


@datasets.route('/datatrain/delete')
@login_required
def datatrain_delete():
    id = request.args.get('id')
    datatrain = Dataset.query.get_or_404(id)
    db.session.delete(datatrain)
    db.session.commit()
    flash('Dataset has been deleted!', 'success')
    return redirect(url_for('datasets.datatrain'))


@datasets.route('/datatest')
@login_required
def datatest():
    return render_template('data_test.html', contentheader='Data Test', menu='Dataset', submenu='datatest', menu_type='sidebar')
