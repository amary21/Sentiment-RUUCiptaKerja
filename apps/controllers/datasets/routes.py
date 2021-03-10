from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from apps import db
from apps.models.dataset import Dataset
from apps.controllers.datasets.form import DataTrainForm
from flask_login import current_user, login_required


datasets = Blueprint('datasets', __name__)


@datasets.route('/datatrain')
@login_required
def datatrain():
    data = Dataset.query.all()
    return render_template('data_train.html', contentheader='Data Train', menu='Dataset', submenu='datatrain', menu_type='sidebar', dataset=data)


@datasets.route('/datatrain/new', methods=['GET', 'POST'])
@login_required
def datatrain_create():
    form = DataTrainForm()
    if form.validate_on_submit():
        data = Dataset(id_admin=current_user.id_admin,
                        tweet=form.tweet.data, sentimen=form.sentiment.data)
        db.session.add(data)
        db.session.commit()
        flash('Dataset has been added', 'success')
        return redirect(url_for('datasets.datatrain'))
    return render_template('data_train_form.html', contentheader='Add New Data Train', menu='Dataset', submenu='datatrain', menu_type='sidebar', form=form)


@datasets.route('/datatrain/update', methods=['GET', 'POST'])
@login_required
def datatrain_update():
    id = request.args.get('id')
    datatrain = Dataset.query.get_or_404(id)
    form = DataTrainForm()
    if form.validate_on_submit():
        datatrain.tweet = form.tweet.data
        datatrain.sentimen = form.sentiment.data
        db.session.commit()
        flash('Dataset has been updated', 'success')
        return redirect(url_for('datasets.datatrain'))
    elif request.method == 'GET':
        form.tweet.data = datatrain.tweet
        form.sentiment.data = datatrain.sentimen
    return render_template('data_train_form.html', contentheader='Add New Data Train', menu='Dataset', submenu='datatrain', menu_type='sidebar', form=form)


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
