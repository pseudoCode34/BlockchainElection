import os

from flask import redirect, url_for, render_template, abort, flash
from flask_login import login_required, logout_user, login_user

from app import login_manager, bcrypt, db
from app.authentication import blueprint
from app.authentication.forms import LoginForm, RegisterForm
from app.authentication.user import User


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template("authentication/login.html", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user is None:
        flash("No user found", "error")
        return redirect(url_for("authentication.login"))

    if not bcrypt.check_password_hash(user.password, form.password.data):
        flash("Incorrect password")
        return redirect(url_for("authentication.login"))

    login_user(user)
    return redirect(url_for("vote.vote"))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if not form.validate_on_submit():
        return render_template("authentication/register.html", form=form)

    hashed_password = bcrypt.generate_password_hash(form.password.data)
    new_user = User(
        username=form.username.data,
        password=hashed_password,
        address=form.address.data,
        key=form.key.data,
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("election.home"))


@blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("election.home"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@blueprint.route("/adminLogin", methods=["GET", "POST"])
def adminLogin():
    form = LoginForm()
    if not form.validate_on_submit():
        return render_template("authentication/adminLogin.html", form=form)

    user = User.query.filter_by(username=form.username.data).first()
    if user is None:
        flash("No user found", "error")
        return redirect(url_for("authentication.login"))

    if user.username != os.getenv("ADMIN_USERNAME"):
        abort(403)

    if not bcrypt.check_password_hash(user.password, os.getenv("ADMIN_PASSWORD")):
        flash("Incorrect password")
        return redirect(url_for("authentication.adminLogin"))

    login_user(user)
    return redirect(url_for("election.admin_portal"))
