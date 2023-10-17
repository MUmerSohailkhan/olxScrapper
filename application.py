from flask import Flask,request,render_template,redirect,url_for
import mysql.connector
import time
from flask_login import LoginManager,login_required,login_user ,UserMixin




app=Flask(__name__)
app.config["SECRET_KEY"]='869238acc2ea82bf22e537688aa795455d66d223'
loginManager=LoginManager()
loginManager.login_view="logInUser"
loginManager.init_app(app)



class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@loginManager.user_loader
def load_user(user_id):
    # cursor = mysql.get_db().cursor()
    mycursor.execute("SELECT userId FROM user WHERE userId = %s", (user_id,))
    user = mycursor.fetchone()
    if user:
        return User(user[0])
    else:
        return None

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="scrapperDB"
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
                login_user(User(myresult[0][1]))
                return redirect (url_for("scrapperTool"))
            else:
                print("wrong password")
        else:
            print("no user name associated with this email")
    return render_template("index.html")



@login_required
@app.route("/scrapperTool", methods=["Post", "Get"])
def scrapperTool():

    if request.form:
        print(request.form['option1'])
        print(request.form['option2'])
        time.sleep(10)
    return render_template("scrapperTool.html")

@app.route("/contactInfo", methods=["Post", "Get"])
def contactInfo():
    page = int(request.args.get('page', 1))
    per_page=20
    offset = (page - 1) * per_page  # Calculate the offset
    query = f"SELECT * FROM contactInfo LIMIT {per_page} OFFSET {offset}"
    mycursor.execute(query)
    contactData = mycursor.fetchall()
    print(contactData)
    total_items =57  # Get the total number of items from your database
    total_pages = (total_items + per_page - 1)

    return render_template("contactInfo.html",contactData=contactData, page=page, per_page=per_page, total_pages=total_pages)

# @app.route("/filteredContactInfo", methods=["Post", "Get"])
# def filteredContactInfo():
#     if request


if __name__=="__main__":
    app.run(debug=True)
