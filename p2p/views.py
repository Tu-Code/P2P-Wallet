from flask import Blueprint, render_template, redirect
from flask.helpers import url_for
from flask_login import  login_required, current_user
from werkzeug.wrappers import request
from flask import flash, request, jsonify
import mysql.connector
# from p2p.models import Transaction
# from .models import Activity, UserActivity
from .models import Transaction, User
from . import db
from flask import Flask, render_template, request
import requests, json
from flask import current_app as views
 
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/fund_account', methods=['GET', 'POST'])
@login_required
def fund_account_check():
    if request.method == 'POST':
        ref = request.get_json()
        access_token='sk_test_8f311084a17072f23b3d2a85544428bff469c060'
        link = 'https://api.paystack.co/transaction/verify/:' + ref
        Link = requests.get(link)
        # data = json.loads(Link.content)
        # print( data )
        details = requests.get(Link,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'})
        resultOfCheck = details.json().get('data')
        data_string = json.dumps(resultOfCheck['data'])
        fund = Transaction(amount = data_string['amount'], user_id=current_user.id)
        db.session.add(fund)
        db.session.commit()
        
        return render_template('fund_account.html', user=current_user)

    return render_template('fund_account.html', user=current_user) 
    
   
@views.route('/transfer', methods=['GET', 'POST'])
def transfer():
    # transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    # balance = sum([x.amount for x in transactions])
    
    users = User.query.all()
    if request.method == 'POST':
        amount = int(request.form.get('amount'))
        user_choice = request.form.get('user_choice')   
        if int(amount) <= int(balance) and users:
            # balance = balance - amount
            trans_1 = Transaction(amount = amount, user_id=user_choice)
            trans_2 = Transaction(amount = (amount*-1), user_id=current_user.id)
            db.session.add(trans_1)
            db.session.add(trans_2)
            db.session.commit()
            flash("Succesfuly transfered " + str(amount) + " to " + users[int(user_choice) - 1].email, category='success')

            # return render_template('transfer.html', user=current_user, balance = balance, user_list = users)
        # if amount is None or int(amount) > int(balance) or int(balance) < 0:
        #     balance = 0
        #     flash("Insufficient Balance.", category='error') 

    return render_template('transfer.html', user=current_user, balance = balance, user_list = users)
   
