from flask import Blueprint, render_template, request, flash, redirect, url_for
from validator_collection import validators, checkers
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user
import re

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')


        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash("There is no user with this email.", category='error')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')



        user = User.query.filter_by(email=email).first()
        # validators.email("test.test@gmail.com", allow_empty = True) ###### Check email better. Look how google does it.
        if user:
            flash("User with this email already exists.", category='error')
        elif re.search(r"^[a-zA-Z0-9.!#$%&'*+\/=?^{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9]{0,61}[a-zA-Z0-9])?)*$", email) == None:
            flash("Email is not valid!", category='error')
        elif len(first_name) < 2:
            flash("The first name must be BETTER!", category='error')
        elif password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 4: ####### How to validate the password?
            flash("Come up with a better password!", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

