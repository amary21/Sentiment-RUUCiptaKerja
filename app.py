from flask import Flask, render_template, url_for, flash, redirect
from controllers.login import LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '19f714e604daf22d7689ebd80964265f'


@app.route("/")
def index():
    return render_template('index.html', contentheader='Dashboard', menu=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin123' and form.password.data == 'admin123':
            flash(f'Selamat Datang {form.username.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau Password Salah!', 'danger')
    return render_template('login.html', contentheader='Login', menu=False, title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
