import os, io
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, send_file
from boredgamers import app, db, bcrypt
from boredgamers.forms import RegistrationForm, LoginForm, UpdateAccountForm
from boredgamers.models import User, Game
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", home_bg="home-bg")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        default_pic_path = os.path.join(app.root_path, "static/profile_pics/default.jpg")
        default = save_picture(default_pic_path)
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password, image_file=default,
            location=form.location.data, age=form.age.data, favourite_games=form.favourite_games.data, 
            about=form.about.data, availability=form.availability.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Please check username and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))



def save_picture(form_picture):
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    buf = io.BytesIO()
    i.save(buf, format=i.format)
    bts = buf.getvalue()
    return bts
    

@app.route("/picture/<int:userid>")
def picture(userid):
    user = User.query.filter_by(id=userid).first()
    picture = user.image_file
    image = Image.open(io.BytesIO(picture))
    return send_file(io.BytesIO(picture), mimetype=f"image/{image.format}")


@app.route("/account")
@login_required
def account():
    userid = current_user.id
    profile_pic = picture(userid)
    return render_template(
        "account.html", title="Account", userid=userid
    )


@app.route("/update-account/<int:user_id>", methods=["GET", "POST"])
@login_required
def update_account(user_id):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        current_user.age = form.age.data
        current_user.favourite_games = form.favourite_games.data
        current_user.about = form.about.data
        current_user.availability = form.availability.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.location.data = current_user.location
        form.age.data = current_user.age
        form.favourite_games.data = current_user.favourite_games
        form.about.data = current_user.about
        form.availability.data = current_user.availability
    return render_template(
        "update_account.html", title="Update account", user_id=user_id, form=form
    )


@app.route("/games")
def games():
    games = Game.query.order_by(Game.rank).all()
    return render_template("games.html", title="Games", games=games)
