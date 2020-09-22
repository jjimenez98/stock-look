from flask import render_template, request, redirect, url_for, jsonify, make_response, session, flash, Markup
import jwt
from startrekk import app
import pickle
from functools import wraps
from startrekk.models import Account, Watchlist
from datetime import datetime, timedelta
from startrekk  import db
from startrekk.stocks import stock
from matplotlib.figure import Figure
import io, base64, os
import csv

def list_tickers():
    t = list()
    with open('/Users/javierjimenez/flaskweb/startrekk/companylist.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    for i in range(1,len(data)):
        t.append((data[i][0],data[i][1]))
    return t

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/token

        print("token!!!!!!!!",token)
        
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : "Token is invalid"}), 401

        return f(*args, **kwargs)
    return decorated

def myMethod(token):
    return jsonify({'token' : token.decode('UTF-8')})


@app.route('/', methods = ['POST', 'GET'])
def index():
    users = Account.query.order_by(Account.date_created).all()
    if request.method == 'POST':
        task_username = request.form['username']
        print('in / login')
        task_password = request.form['password']
        try:
            u = Account.query.filter_by(username=task_username).first()
        except:
            return redirect('/')
        if type(u) == type(Account()):
            if u.username == task_username:
                if u.password == task_password:
                    token = jwt.encode({'user': task_username, 'exp': datetime.utcnow() + timedelta(minutes=30)},app.config['SECRET_KEY'])
                    myMethod(token)
                    return render_template('/home.html', token=token.decode(),user=users)
                else:
                    return make_response('could not auth',401)
            else:
                print("Not found")
        else:
            return redirect('/')   
        return redirect('/') 
    else:
        return render_template('home.html',users = users)
    return render_template('home.html')

@app.route('/home', methods = ['POST','GET'])
# @token_required
def home():
    return render_template('home.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        task_username = request.form['username']
        print('in / login')
        task_password = request.form['password']
        try:
            u = Account.query.filter_by(username=task_username).first()
        except:
            return redirect('/login')
        if type(u) == type(Account()):
            if u.username == task_username:
                if u.password == task_password:
                    token = jwt.encode({'user': task_username, 'exp': datetime.utcnow() + timedelta(minutes=30)},app.config['SECRET_KEY'])
                    myMethod(token)
                    return render_template('/home.html', token=token.decode())
                else:
                    return make_response('could not auth',401)
            else:
                print("Not found")
        else:
            return redirect('/login')
        return redirect('/login')
    else:
        users = Account.query.order_by(Account.date_created).all()
        return render_template('index.html',users = users)
    return render_template('index.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if request.form['username']:
            task_username = request.form['username']
            print(task_username)
            task_password = request.form['password']
            print(task_password)
            user = Account()
            user.password = task_password
            user.username = task_username
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'Account {task_username} was created!','success')
            except:
                flash(f'Account not created','success')
            return redirect('/login')
        else:
            return render_template('signup.html')
    return render_template('signup.html')

@app.route('/delete', methods = ['POST','GET'])
def delete():
    if request.method == 'POST':
        if request.form['username']:
            task_username = request.form['username']
            try:
                u = Account.query.filter_by(username=task_username).first()
                db.session.delete(u)
                db.session.commit()
                return redirect('/')
            except:
                return redirect('/')

@app.route('/stocks', methods = ['POST','GET'])
def stocks():
    if request.method == 'POST':
        # if request.form['Submit']:
        #     return 'hi'
        if request.form['ticker']:
            t = request.form['range']
            task_ticker = request.form['ticker']
            s = stock(task_ticker,1,t)
            s.getinfo()
            t = len(s.prices)
            arr = list()
            for i in range(t):
                arr.append(i)
            Open = s.data['open']
            High = s.data['high']
            Low = s.data['low']
            Close = s.data['close']
            adj_Close = s.data['adj_close']
            fig = Figure(figsize=(5.1,5))
            ax = fig.subplots()
            ax.set_ylabel('Price')
            ax.set_xlabel('Days')
            ax.plot(arr, s.prices)
            fig.suptitle(s.ticker)
            #encoding the figure -> png
            img = io.BytesIO()
            fig.savefig(img,format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            plot_url = Markup('<img style="padding-top:1rem; object-fit:cover; width:100%;"src="data:image/png;base64,{}">'.format(plot_url))
            listt = list_tickers()
            return render_template('stock.html',plot_url=plot_url, listt = listt, open = Open, high = High, low = Low, close = Close, adjclose = adj_Close, ticker= task_ticker)
    listt = list_tickers()
    return render_template('stock.html')

@app.route('/background_process')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)


