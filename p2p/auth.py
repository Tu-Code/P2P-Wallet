from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email =request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in succesfully!', category='success')
                return jsonify({'Logged in succesfully!':'success'})
            else:
                flash('Incorrect Password', category='error')
                return jsonify({'error': 'Incorrect Password.'})
        else:
            flash('Email doesn\'t exist', category='error')
            return jsonify({'error':'Email doesn\'t exist. '})

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            return jsonify({'error': 'Email already exists.'})
        if len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
            return jsonify({'error': 'Email must be greater than 3 characters'})
        elif len(name) < 2:
            flash('Name must be greater than 1 character', category='error')
            return jsonify({'error': 'Name must be greater than 1 character'})
        elif len(password) < 7:
            flash('Password is too short', category='error')
            return jsonify({'error': 'Password is too short'})
        else:
            # account created                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmnbh4
            new_user = User(email=email, password=generate_password_hash
            (password, method = 'sha256'), name=name, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            print(user)
            login_user(new_user)
            return jsonify({ 'response' : 'User ' + email + ' created' })

    return render_template('signup.html', user=current_user)