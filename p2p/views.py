from flask import Blueprint, render_template
from flask_login import  login_required, current_user
from werkzeug.wrappers import request
from flask import flash, request, jsonify
from .models import Transaction, User
from . import db
from flask import render_template, request
from flask import current_app as views
 
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/fund_account', methods=['GET', 'POST'])
@login_required

def fund_account():
    balance = 50000
    transactions =  Transaction.query.filter_by(user_id=current_user.id).all()

    for x in transactions:
        balance = balance + x.amount
    if request.method == 'POST':
        formAmount = int(request.form.get('amount'))
        balance = balance + formAmount
        trans = Transaction(amount = formAmount, user_id=current_user.id)
        db.session.add(trans)
        db.session.commit()
        flash("Succesfuly funded account with " + str(formAmount))
        return jsonify({'Succesfuly funded account with ': str(formAmount)})
    return render_template('fund_account.html', balance = balance, user=current_user) 

@views.route('/transfer', methods=['GET', 'POST'])

def transfer():
    users = User.query.all()
    balance = 50000
    transactions =  Transaction.query.filter_by(user_id=current_user.id).all()
    
    for x in transactions:
        balance = balance + x.amount
    if request.method == 'POST':
        formAmount = int(request.form.get('amount'))
        if balance >= formAmount and len(users) > 1:
            balance = balance - formAmount
            user_choice = request.form.get('user_choice')   
            trans = Transaction(amount = (formAmount*-1), user_id=current_user.id)
            db.session.add(trans)
            db.session.commit()
            flash("Succesfuly transfered " + str(formAmount) + " to " + users[int(user_choice) - 1].email, category='success')
            return jsonify({'success':
            "Succesfuly transfered " + str(formAmount) + " to " + users[int(user_choice) - 1].email + " " + str(balance)})
        if formAmount is None or int(formAmount) > int(balance) or int(balance) < 0:
            balance = 0
            flash("Insufficient Balance.", category='error')
            return jsonify({'error': 'Insufficient Balance.'})
        if len(users) <= 1:
            flash("No user chosen.", category='error')
            return jsonify({'error': 'No user chosen.'})
    return render_template('transfer.html', balance = balance , user=current_user, user_list = users)
   
