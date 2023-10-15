from flask import Flask,request,render_template,redirect,url_for
import mysql.connector
import time
# from flask_login import LoginManager,login_required,login_user


app=Flask(__name__)
app.config["SECRET_KEY"]='869238acc2ea82bf22e537688aa795455d66d223'
# loginManager=LoginManager()
# loginManager.login_view="logInUser"
# loginManager.init_app(app)



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="olxdatabase"
)
mycursor = mydb.cursor()




@app.route("/")
@app.route("/signin")
@app.route("/login",methods=["Post","GET"])
def logInUser():
    if request.form:
        email = request.form['email']
        print(email)
        password = request.form['password']
        print(password)
        query=f"select * from user where Email='{email}'"
        print(query)
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        print(myresult)
        if myresult:
            if myresult[0][3]==password:
                # login_user(myresult[0])
                return redirect (url_for("scrapperTool"))
            else:
                print("wrong password")
        else:
            print("no user name associated with this email")
    return render_template("index.html")



# @login_required
@app.route("/scrapperTool", methods=["Post", "Get"])
def scrapperTool():

    if request.form:
        print(request.form['option1'])
        print(request.form['option2'])
        time.sleep(10)
    return render_template("scrapperTool.html")

@app.route("/contactInfo", methods=["Post", "Get"])
def contactInfo():
    query="select * from contactInfo"
    mycursor.execute(query)
    contactData = mycursor.fetchall()
    print(contactData)

    return render_template("contactInfo.html",contactData=contactData)


if __name__=="__main__":
    app.run(debug=True)
