import base64,io
from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from mongoengine.errors import NotUniqueError
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import *
from ..models import *

users = Blueprint("users", __name__)

""" ************ User Management views ************ """

def get_strengths(str_lst):
    lst = str_lst.split(",")
    strength_lst = [Strength(strength_name = s) for s in lst]
    return strength_lst
    
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        group = Group.objects(group_name=form.group.data).modify(upsert=True, new=True, set_on_insert__meetings=0)

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            strengths=form.select_field.data,
            group=group,
        )
        user.save()

        # add new user into group
        group.group_members.append(user)
        group.save()
        
        # add user into the strengths
        strength_lst = get_strengths(user.strengths)
        for s in strength_lst:
            s.users.append(user)
            s.save()
        
        flash("Registration successful! You have been added to the group.", "success")
        return redirect(url_for("users.login"))
    
    return render_template('register.html', form = form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('strengths.index'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username = form.username.data).first()
            
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.account'))
            else:
                flash("Login failed!", 'auth-fail')
    return render_template('login.html', form = form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

def get_users(str_username_lst):
    lst = []
    for name in str_username_lst:
        user = User.objects(username = name).first()


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    
    LogMeetingForm = LogMeeting()
    
    if request.method == 'POST':
        if LogMeetingForm.validate_on_submit():
            form_str_members = set(LogMeetingForm.members.data.split(" "))
            for name in form_str_members:
                user = User.objects(username = name).first()
                if user and user.group == current_user.group:
                    user.appearances += 1
                    user.save()
            current_user.group.meetings += 1
            current_user.group.save()
            return render_template('account.html', LogMeeting= LogMeetingForm)
            
    return render_template('account.html', LogMeeting= LogMeetingForm)

