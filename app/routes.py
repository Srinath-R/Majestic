from app import app
from flask import render_template,url_for,request,session,redirect
from app import db
from app.models import User, Booking
from datetime import datetime

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/explore.html')
def explore():
    return render_template("explore.html")

@app.route('/rooms.html')
def room():
    return render_template("rooms.html")

@app.route('/bb.html')
def booking():
    return render_template("bb.html")    

@app.route('/contact.html')
def contact():
    return render_template("contact.html")            

@app.route('/login.html')
def login():
    if 'user' in session:
        return render_template("home.html",session=session)
    else:    
        return render_template("login.html")     

@app.route('/register.html')
def register():
    if 'user' in session:
        return render_template("home.html",session=session)
    else:  
        return render_template("register.html")    

@app.route('/register',methods = ['POST','GET'])
def add_user():
    if request.method == "POST":
        result = request.form
        if result['password'] == result['confirm_password']:
            u = User(name=result['name'], email=result['email'],password=result['password'])
            db.session.add(u)
            db.session.commit()
        return render_template("login.html")

@app.route('/dashboard',methods = ['POST','GET'])
def login_user():
    if 'user' in session:
        return render_template("home.html",session=session)
    elif request.method == "POST":
        result = request.form
        email = result['email']
        password = result['password']
        query = db.engine.execute("SELECT * FROM user WHERE email='{}'".format(email))
        row = query.fetchone()
        if row is None:
            return "Wrong Email ID!"  
        elif password == row[2]:
            session['id'] = row[0]  
            session.permanent = True
            session['email'] = row[1]
            session['password'] = row[2]
            session['user'] = row[3]
            return render_template("home.html",session = session)
        else:
            return "Wrong password!"   
    else:
        return "Bad Request."             
          
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))  

@app.route('/home.html')
def home():
    return render_template("home.html")    

@app.route('/book')
def book():
    return render_template("book.html")

@app.route('/rooms')
def rooms():
    query = db.engine.execute("SELECT * FROM booking WHERE guest_id={}".format(session['id']))
    return render_template("room.html",results=query)

@app.route('/cancel')
def cancel():    
    return render_template("cancel.html")

@app.route('/booking',methods = ['POST','GET'])
def bookingroom():
    if 'user' not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            result = request.form
            for num in range(1,101):
                if db.session.query(Booking.room_no).filter_by(room_no=num).scalar() is None:
                    rno = num
                    break
            b = Booking(room_no=rno, guest_id=int(session['id']),start=datetime.strptime(result['from'], '%Y-%m-%dT%H:%M'),end=datetime.strptime(result['to'], '%Y-%m-%dT%H:%M'))
            db.session.add(b)
            db.session.commit()
            return redirect(url_for("rooms"))

@app.route('/cancelbooking',methods = ['POST','GET'])
def cancelbooking():
    if 'user' not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            result = request.form
            db.engine.execute("DELETE FROM booking WHERE guest_id={} AND room_no={}".format(session['id'],result['rno']))
            return redirect(url_for("rooms"))



