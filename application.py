from flask import Flask,request,render_template,redirect,url_for,jsonify
import mysql.connector
import time
from flask_login import LoginManager,login_required,login_user ,UserMixin
from utils import createPattern



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

@app.route("/api/olxdata", methods=["Post", "Get"])
def filteredContactInfo():
    param=list(request.args.keys())
    # print(type(param))
    # return "ok"
    print(len(param))
    findValue=list(request.args.values())
    print(findValue)
    if (len(param)==1 and (param[0]=='addid'or param[0]=='contactid'or param[0]=='phonenumber' )):
        query=f"select * from olxdata where addid='{findValue[0]}' or contactid='{findValue[0]}' or phonenumber='{findValue[0]}'"
        print(query)
        mycursor.execute(query)
        data=mycursor.fetchall()
        return data,200
    elif len(param)<1:
        return jsonify({"Message":"please insert proper parameters according to documentation"}),400
    else:
        paraList=list(request.args.keys())
        parameters = dict(request.args.items())
        offset = parameters['start']
        if 'city' in paraList and 'address' not in paraList:
            print(parameters)
            city=parameters['city'].split(',')
            cityPattern=list(map(createPattern,city))
            print(cityPattern)
            query = "SELECT * FROM olxdata WHERE " + " OR ".join(["Address LIKE %s" for _ in cityPattern])+ f" LIMIT {parameters['range']} OFFSET {parameters['start']}"
            print(query)
            mycursor.execute(query,cityPattern)
            data=mycursor.fetchall()
        elif ('address' in paraList and 'city' not in paraList) or ('address' in paraList and 'city'  in paraList):
            address=parameters['address'].split('|')
            query = f"select * from olxdata where  Address IN {tuple(address)} LIMIT {parameters['range']} OFFSET {offset}"
            print(query)
            mycursor.execute(query)
            data = mycursor.fetchall()
        elif 'addid' in paraList:
            addid=parameters['addid'].split(',')
            print(addid)
            query = f"select * from olxdata where  Addid IN {tuple(addid)} LIMIT {parameters['range']} OFFSET {offset}"
            mycursor.execute(query)
            data = mycursor.fetchall()
        elif 'addid' in paraList and 'city' in paraList and 'phonenumber' in paraList:
            addid=parameters['addid'].split(',')
            city = parameters['city']
            phonenumber=parameters['city'].split(',')
            query = f"select * from olxdata where  Addid IN {tuple(addid)} and Address like '%{city}%' LIMIT {parameters['range']} OFFSET {offset}"
            mycursor.execute(query)
            data = mycursor.fetchall()

        return data,200

@app.route("/api/createSearchWord", methods=["Post", "Get"])
def createSearchWord():
    searchWord=request.args.get('searchWord')
    print(searchWord)
    with open('searchWord.txt','w') as file:
        file.write(searchWord)
        file.close()
        return {'Message':'Search word is set'},200

if __name__=="__main__":
    app.run(debug=True)
