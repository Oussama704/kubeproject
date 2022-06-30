from re import A
from flask import Flask,request, redirect, url_for,render_template
import boto3
import pymysql
session={}
db = pymysql.connect("database-eyseon.csofxf8tnbgk.us-east-1.rds.amazonaws.com", "admin", "adminadmin", "users")
cursor = db.cursor()
def color(data):
    del data["ID"]
    dictdata={}
    for i in range(len(data)):
        if int(data["cap"+str(i+1)])<35:
            dictdata["cap"+str(i+1)]="red"
        if int(data["cap"+str(i+1)])>=77:
            dictdata["cap"+str(i+1)]="grenn"
        else :
            dictdata["cap"+str(i+1)]="yellow"
    return dictdata
app =Flask(__name__)
@app.route('/')
def index():
    return render_template("home.html")
@app.route('/login',methods=['GET', 'POST'])
def login():
    if len(session)==0:
        print("1111111111111111111111111111111111111111")
        if request.method == 'POST':
            print("2222222222222222222222222222222222222222222222222")
            username =request.form['username']
            password=request.form['password']
            print("3333333333333333333333333333333333333333333333333")
            cursor.execute('SELECT * FROM users WHERE username = %s AND pwd = %s', (username, password))
            print("4444444444444444444444444444444444444444444444444")
            account = cursor.fetchone()
            print("hhhhhhhhhhhhhhhhhhhhhhh : ",account)
            if account!=None:
                session['loggedin'] = True
                session['username']=username
                session['password']=password
                session['id']=account[2]
            # Redirect to home page
                return redirect(url_for('demo'))
            else :
                return render_template("login.html")

        else:
            return render_template("login.html")
    else : 
        return redirect(url_for('demo'))
@app.route('/demo')
def demo():
    if len(session)>0:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('capteus')
        resource=table.get_item(
                    Key ={
                    'ID': 1
                  }
            )
        data=resource["Item"]
        data=color(data)
        data["username"]=session["username"]
        data["id"]=session["id"]
        print(data)
        return render_template("demo.html",data=data)
    else : 
        return redirect(url_for('login'))
def fun():
    print("Hello world !")
if __name__=='main':
    app.run(debug=True)
