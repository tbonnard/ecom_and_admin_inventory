from app import db

from flask import redirect, url_for, render_template, flash, Blueprint, request
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from .forms import UserForm, UserLoginForm
from .models import User

from flask_login import LoginManager

login_manager = LoginManager()

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.type != "User":
            return redirect(url_for('ecom.index'))
        return f(*args, **kwargs)
    return decorated_function


# ROUTES ADMIN
@auth.route("/admin/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                flash("Sorry, those credentials (pwd) info do not allow an access")
        else:
            flash("Sorry, those credentials (email) info do not allow an access ")
    return render_template('login.html', form=form)


@auth.route("/admin/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("It seems an error occurred. Try with other credentials or try to login if you already have an account!")
            return redirect(url_for('auth.register'))

        else:
            pwd_hashed = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
            new_user = User(email=form.email.data, password=pwd_hashed, first_name=form.first_name.data, last_name=form.last_name.data, type='User', status='pending')
            db.session.add(new_user)
            # auto activate user as it is a demo
            new_user.status = 'active'

            db.session.commit()

            login_user(new_user)

        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)


@auth.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route("/activate")
@login_required
def activate():
    user_to_activate = User.query.get(request.args.get('user_id'))
    user_to_activate.status = 'active'
    db.session.commit()
    return redirect(url_for('main.home'))




# ROUTES ECOM
@auth.route("/login", methods=['GET', 'POST'])
def login_ecom():
    if current_user.is_authenticated:
        return redirect(url_for('ecom.index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('ecom.index'))
            else:
                flash("Sorry, those credentials (pwd) info do not allow an access")
        else:
            flash("Sorry, those credentials (email) info do not allow an access ")
    return render_template('ecom/login_ecom.html', form=form)


@auth.route("/register", methods=['GET', 'POST'])
def register_ecom():
    if current_user.is_authenticated:
        return redirect(url_for('ecom.index'))
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("It seems an error occurred. Try with other credentials or try to login if you already have an account!")
            return redirect(url_for('auth.register_ecom'))

        else:
            pwd_hashed = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
            new_user = User(email=form.email.data, password=pwd_hashed, first_name=form.first_name.data, last_name=form.last_name.data, type='Client', status='active')
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

        return redirect(url_for('ecom.index'))
    return render_template('ecom/register_ecom.html', form=form)


@auth.route("/logout_ecom")
@login_required
def logout_ecom():
    logout_user()
    return redirect(url_for('auth.login_ecom'))