import secrets
import os
import config
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddPlant, PlantButtons
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Plant
from datetime import datetime
from pathlib import Path

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Menu')
 

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/catalogue')
@login_required
def catalogue():
    form = PlantButtons()
    plants = Plant.query.all()
    image_path = Path('static/flowers')
    if form.validate_on_submit:
        pass
    
    return render_template('plants.html', title='Catalogue', plants=plants, image_path=image_path, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Bravo, vous êtes maintenant inscrit !')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='images/' + current_user.image_file)

    return render_template('user.html', title= 'Profil', user=user, image_file = image_file)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(config.basedir, 'app\\static\\flowers\\', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/add_plant', methods=['GET', 'POST'])
@login_required
def add_plant():
    form = AddPlant()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data)
            plant = Plant(name=form.name.data, description=form.description.data, author=current_user.username, image_file=image_file)
        else:
            plant = Plant(name=form.name.data, description=form.description.data, author=current_user.username)
        db.session.add(plant)
        db.session.commit()
        flash('La plante/fleur à bien été ajoutée !')
        return redirect(url_for('catalogue'))
    return render_template("add_plant.html", title='Add Plants', form=form)


@app.route('/admin_pannel', methods=['GET', 'POST'])
@login_required
def clean():
    if current_user.username == 'administrator' or current_user.username == 'simon':
        plants = Plant.query.all()
        for plant in plants:
            db.session.delete(plant)
            db.session.commit()
        return redirect(url_for('catalogue'))
    
        
        
