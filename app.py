from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
                    return redirect('/home')
                else:
                    print('incorrect password')
                    pass
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
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)