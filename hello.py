from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError, StopValidation

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'some random string'


def validate_email(form, field):
    message = field.gettext("This field is required.")
    if not "@" in field.data:
        raise StopValidation(f"Please include an '@' in the email address. '{field.data}' is missing an '@'")

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), validate_email])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    email_string=None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        old_email = session.get("email")
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
            print("Flashed name")
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
            print("Flashed email")
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    
    if not session.get('email'):
        pass
    elif "utoronto" not in session.get('email'):
        email_string = "Please use your UofT email."
    else:
        email_string = "Your UofT email is " + session.get('email')

    return render_template('form.html', form=form, name=session.get('name'), email_string=email_string)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
