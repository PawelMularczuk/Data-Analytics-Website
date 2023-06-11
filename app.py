from flask import Flask, render_template, url_for, request ,redirect, flash, send_file, Response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, ValidationError
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from wtforms.validators import DataRequired, Email, Regexp, EqualTo,Length, email_validator
from analize import commonalty1,produce_death,death,produce,women, plot_data6, age2040,age2050,age2030, age2014
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import matplotlib.pyplot as plt 
import seaborn as sns
import urllib
import matplotlib
from functional_age_groups2014 import plot_data5
import pandas as pd
import numpy as np


matplotlib.use('agg')
value = list(produce_death.values)


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'First, please log in'

class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)


    @property  
    def password(self):
        raise AttributeError('The password attribute could not be read ')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)    
    
    def __repr__(self):
        return 'User: {},{}'.format(self.name)


class Registrationform(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Nazwa użytkownika może składać sie....')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must be identical')])
    password2 = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Register')

  

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('this e-mail is already registered.')
        
    def validate_username(self, field):
        if User.query.filter_by(username= field.data).first():
            raise ValidationError('This username is already used')    

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


class LoginForm(FlaskForm):
    username = StringField('User name')
    password = PasswordField('Password')
    remember = BooleanField('Remember me')


@app.route('/init')
def init():
    db.create_all()

    admin = User.query.filter(User.name == 'admin').first()
    if admin == None:
        admin = User(id=1, name='admin', password_hash=generate_password_hash('1234'), email='nic@o2.pl', username='admin')
    db.session.add(admin) 
    db.session.commit()

    return '<h1>Initial configuration Done!</h1>'


@app.route('/')
def index():
    return'<h1>Hello!!!</h1>'


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user != None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)

            next = request.args.get('next')
            if next and is_safe_url(next):
                return redirect(next)
            else:
                return '<h1>You are logged in</h1>'

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET','POST'])
def register():

    form = Registrationform()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Register complete')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout')
def logout():

    logout_user()
    flash('You are logged out')
    return redirect(url_for('login'))


@app.route('/secred') 
@login_required
def secred():

    fig,ax = plt.subplots(figsize=(10,8))
    ax=sns.set_style(style = 'whitegrid')

    sns.lineplot(commonalty1)
    plt.ticklabel_format(axis='y', style='plain')
    plt.xticks(range(0,37,2))
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data1 = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))


    fig,ax = plt.subplots(figsize=(9,6))
    ax=sns.set_style(style = 'whitegrid')

    sns.barplot(x='Rok', y='Zgony', data=death)
    plt.xticks(range(0,37,2))
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data2 = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))


    fig,ax = plt.subplots(figsize=(9,6))
    ax=sns.set_style(style = 'whitegrid')

    sns.barplot(x='Rok', y='Urodzenia', data=produce, color='blue')
    plt.xticks(range(0,37,2))
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data3 = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))



    fig,ax= plt.subplots(figsize=(9,8))
    ax=sns.set_style(style = 'whitegrid')
    plt.ticklabel_format(axis='y', style='plain')
    sns.barplot(data=produce_death)
    
    for x in produce_death.values:
        label = [x[0], x[1]]

    for index, value in enumerate(label):
        plt.text(index, value, str("{:,}".format(value)), ha='center')

    sns.lineplot(produce_death)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    
    # return render_template('secred.html')
    # # return '<h1>You have access to protected secrets. You are {}</h1>'.format(current_user.username)


    fig,ax = plt.subplots(figsize=(9,6))
    plt.ticklabel_format(axis='y', style='plain')
    ax=sns.set_style(style = 'whitegrid')


    sns.barplot(x=women.index, y='Kobiety w wieku 25-35', data=women)
    plt.xticks(range(0,37,2))
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data4 = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))



    return render_template('secred.html', plot_url=plot_data, plot_url1=plot_data1, plot_url2=plot_data2, plot_url3=plot_data3, plot_url4=plot_data4)


@app.route('/png')
def pie_png():
    
    fig = Figure(figsize=(5,3))
    axis = fig.add_subplot()
    axis.pie(age2014['Ogółem'], labels=age2014.index, autopct='%1.2f%%')
    axis.set_title('Rok 2014')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='img/png')

@app.route('/png2')
def pie2_png():

    fig = Figure(figsize=(5,3))
    axis = fig.add_subplot()
    axis.pie(age2030['Ogółem'], labels=age2030.index, autopct='%1.2f%%')
    axis.set_title('Rok 2030')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='img/png')

@app.route('/png3')
def pie3_png():

    fig = Figure(figsize=(5,3))
    axis = fig.add_subplot()
    axis.pie(age2040['Ogółem'], labels=age2040.index, autopct='%1.2f%%')
    axis.set_title('Rok 2040')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='img/png')

@app.route('/png4')
def pie4_png():
    
    fig = Figure(figsize=(5,3))
    axis = fig.add_subplot()
    axis.pie(age2050['Ogółem'], labels=age2050.index, autopct='%1.2f%%')
    axis.set_title('Rok 2050')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='img/png')


if __name__ =='main':
    app.run(debug=True)

