from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask import Flask, session
import jwt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY']= 'fdsfdasfdsafrqgopmtbombbgrer'
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique= True)
    password = db.Column(db.String(80), nullable=False,unique = True)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):
        return '<USER %r>' % self.id

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
    if request.method == 'POST':
        task_username = request.form['username']
        print(task_username)
        task_password = request.form['password']
        print(task_password)
        try:
            u = Account.query.filter_by(username=task_username).first()
        except:
            return redirect('/')
        if type(u) == type(Account()):

            if u.username == task_username:
                if u.password == task_password:
                    token = jwt.encode({'user': task_username, 'exp': datetime.utcnow() + timedelta(minutes=30)},app.config['SECRET_KEY'])
                    myMethod(token)
                    return redirect(f'/home?token={token.decode()}')
                else:
                    return make_response('could not auth',401)
            else:
                print("Not found")
        else:
            return redirect('/')
        
        
        return redirect('/')
   
    else:
        users = Account.query.order_by(Account.date_created).all()
        return render_template('index.html',users = users)

    return render_template('index.html')

@app.route('/home', methods = ['POST','GET'])
@token_required
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)