from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
from encrypt import encrypt
from encrypt import decrypt
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import random

database='final.db'
conn=sqlite3.connect(database)
cursor=conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS patient_details(Id INTEGER PRIMARY KEY AUTOINCREMENT, patient_name TEXT, patient_ID INT, age INT, address TEXT, d_email TEXT, password INT)")
cursor.execute("create table if not exists seller_details(Id INTEGER PRIMARY KEY AUTOINCREMENT ,seller_name text,sellertype text,busiess_ID int ,mobile_no int ,email text,pan text,gst text,password int)")
cursor.execute("create table if not exists doctor_details(Id INTEGER PRIMARY KEY AUTOINCREMENT ,doctor_name text,registatoin_ID int ,employe_code int ,email text,password int)")
cursor.execute("create table if not exists status (Id INTEGER PRIMARY KEY  ,medicine1 text,d_email text,busiess_ID text,patient_ID text,status int,order_no int)")
conn.commit()



app=Flask(__name__)
@app.route("/")
@app.route("/index")
def index():
        return render_template("index.html")

@app.route("/patient_details",methods=['POST','GET'])
def patient_details():
    if request.method=="POST":
        patient_name=request.form['patient_name']
        patient_ID=request.form['patient_ID']
        age=request.form['age']
        address=request.form['address']
        d_email=request.form['d_email']
        password=request.form['password']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("insert into patient_details (patient_name,patient_ID,age,address,d_email,password) values(?,?,?,?,?,?)",(patient_name,patient_ID,age,address,d_email,password))
        conn.commit()
        return render_template("patient_details.html")
    return render_template("patient_details.html")
plog=[]
@app.route("/patient_login", methods=['POST', 'GET'])
def patient_login():
    if request.method == "POST":
        patient_ID = request.form['patient_ID']
        plog.append(patient_ID)
        password = request.form['password']
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient_details WHERE patient_ID = ? AND password = ?", (patient_ID, password))
        user = cursor.fetchone()
        if user:
            return render_template("medicine.html" )
        else:
            return "wrong password"
    return render_template("patient_details.html")




        
@app.route("/seller_details",methods=['POST','GET'])
def seller_details():
    if request.method=="POST":
        sellername=request.form['sellername']
        sellertype=request.form['sellertype']
        busiess_ID=request.form['busiess_ID']
        mobile_no=request.form['mobile_no']
        email=request.form['email']
        pan=request.form['pan']
        gst=request.form['gst']
        password=request.form['password']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("insert into seller_details (seller_name,sellertype,busiess_ID,mobile_no,email,pan,gst,password) values(?,?,?,?,?,?,?,?)",(sellername,sellertype,busiess_ID,mobile_no,email,pan,gst,password))
        conn.commit()
        return render_template("seller_details.html")
    return render_template("seller_details.html")

slog=[]
@app.route("/seller_login", methods=['POST', 'GET'])
def seller_login():
    if request.method == "POST":
        busiess_ID = request.form['busiess_ID']
        slog.append(busiess_ID)
        password = request.form['password']
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM seller_details WHERE busiess_ID = ? AND password = ?", (busiess_ID, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()  
            cursor.execute("SELECT * FROM status WHERE busiess_ID = ? and status=0",(busiess_ID,))
            results = cursor.fetchall()
            return render_template("receive_table.html",results=results)
        else:
            return render_template("seller_details.html", message="Invalid credentials")
    return render_template("seller_details.html")


@app.route("/back2", methods=['POST', 'GET'])
def back2():
            conn = sqlite3.connect(database)
            cursor = conn.cursor()  
            cursor.execute("SELECT * FROM status  WHERE busiess_ID = ? and  status = ?",(slog[-1],0))
            results = cursor.fetchall()
            return render_template("receive_table.html",results=results)


@app.route("/back3", methods=['POST', 'GET'])
def back3():
            conn = sqlite3.connect(database)
            cursor = conn.cursor()  
            cursor.execute("SELECT * FROM status  WHERE busiess_ID = ? and  status = ?",(slog[-1],1))
            results = cursor.fetchall()
            return render_template("pen1.html",results=results)

@app.route("/doctor_details",methods=['POST','GET'])
def doctor_details():
    if request.method=="POST":
        doctor_name=request.form['doctor_name']
        registatoin_ID=request.form['registatoin_ID']
        employe_code=request.form['employe_code']
        email=request.form['email']
        password=request.form['password']
        conn=sqlite3.connect(database)
        cursor=conn.cursor()
        cursor.execute("insert into doctor_details (doctor_name,registatoin_ID,employe_code,email,password) values(?,?,?,?,?)",(doctor_name,registatoin_ID,employe_code,email,password))
        conn.commit()
        return render_template("doctor_details.html")
    return render_template("doctor_details.html")

d=[]
@app.route("/doctor_login", methods=['POST', 'GET'])
def doctor_login():
    if request.method == "POST":
        email = request.form['email']
        d.append(email)
        password = request.form['password']
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctor_details WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        if user:
                cursor.execute("SELECT * FROM status WHERE d_email =? and status= ?",(email,1))
                results = cursor.fetchall()
                return render_template("pen1.html",results=results)
        else:
            return render_template("doctor_details.html", message="Invalid credentials")
    return render_template("doctor_details.html")




encryp=[]
de=[]
key1=[]
@app.route("/medicine", methods=['POST', 'GET'])
def medicine():
    if request.method == "POST":
        a = request.form['medicine1']
        b = request.form['medicine2']
        c = request.form['medicine3']
        d = request.form['medicine4']
        d_email = request.form['d_email']
        de.append(d_email)
        data=a+","+b+","+c+","+d
        password = request.form['key']
        key1.append(password)
        encrypted1 = encrypt(data, password)
        encryp.append(encrypted1)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM seller_details" )
        results = cursor.fetchall()
        return render_template("table_seller.html",results=results)
    return render_template("medicine.html")    


        
@app.route("/table_seller", methods=['POST', 'GET'])
def table_seller():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()  
    cursor.execute("SELECT * FROM seller_details")
    results = cursor.fetchall()
    return render_template("table_seller.html",results=results)

@app.route("/receive_table", methods=['POST', 'GET'])
def receive_table():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()  
    cursor.execute("SELECT * FROM medicine")
    results = cursor.fetchall()
    return render_template("receive_table.html",results=results)

def email_send(email,key,name,order_no):
            smtp_server = 'smtp.example.com'
            smtp_port = 587
            sender_email = 'triossoftwaremail@gmail.com'
            sender_password = 'knaxddlwfpkplsik'
            receiver_email = email
            host = "smtp.gmail.com"
            mmail = 'triossoftwaremail@gmail.com'      
            hmail = email
            receiver_name = name
            sender_name= "E-commerce"
            msg = MIMEMultipart()
            subject = "please dont share your key"
            text = f"your key-{key},Order no-{order_no}"
            msg = MIMEText(text, 'plain')
            msg['To'] = formataddr((receiver_name, hmail))
            msg['From'] = formataddr((sender_name, mmail))
            msg['Subject'] = 'patient -id  ' + receiver_name
            server = smtplib.SMTP(host, 587)
            server.ehlo()
            server.starttls()
            password = "knaxddlwfpkplsik"
            server.login(mmail, password)
            server.sendmail(mmail, [hmail], msg.as_string())
            server.quit()
            send="send"


def generate_order(length=6):
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp


@app.route('/send', methods=["GET","POST"])
def send():
    if request.method == "POST":
            userid = request.form['number']
            medicine1=encryp[-1]
            d_email=de[-1]
            busiess_ID=userid
            patient_ID=plog[-1]
            key=key1[-1]
            conn = sqlite3.connect(database)
            cursor=conn.cursor()
            status=0
            order_no = generate_order()

            cursor.execute("insert into status (medicine1,d_email,busiess_ID,patient_ID,status,order_no) values(?,?,?,?,?,?)",(medicine1,d_email,busiess_ID,patient_ID,status,order_no))
            conn.commit()
            cursor.execute("SELECT email FROM seller_details WHERE busiess_ID IN (?)", (userid,))
            data=cursor.fetchone()
            email1=email_send(d_email,key,patient_ID,order_no)
            email2=email_send(data[0],key,patient_ID,order_no)
            
            
            return render_template("medicine.html")

@app.route('/recieve', methods=["GET","POST"])
def recieve():
        if request.method == "POST":
            userid = request.form['number']
            password = request.form['pass']
            conn = sqlite3.connect(database)
            cursor = conn.cursor()  
            cursor.execute("SELECT  medicine1,d_email FROM status where id=?",(userid,))
            results = cursor.fetchone()
            decrypted=results[0]
            d_email=results[1]
            decrypted1 = decrypt(decrypted, password)
            if decrypted1== 1:
                    a="*****"
                    b="Incorrect Password"
                    return render_template("accept.html",medicine1=b, medicine2=a, medicine3=a ,medicine4=a,email=a)
            else:
                    a, b, c ,d= decrypted1.split(',')
                    return render_template("accept.html",medicine1=a, medicine2=b, medicine3=c ,medicine4=d,email=d_email)
        return render_template("receive_table.html")



@app.route('/show', methods=["GET","POST"])
def show():
        if request.method == "POST":
            userid = request.form['number']
            password = request.form['pass']
            conn = sqlite3.connect(database)
            cursor = conn.cursor()  
            cursor.execute("SELECT  medicine1,d_email FROM status where id=?",(userid,))
            results = cursor.fetchone()
            decrypted=results[0]
            d_email=results[1]
            decrypted1 = decrypt(decrypted, password)
            a, b, c ,d= decrypted1.split(',')
            return render_template("accept.html",medicine1=a, medicine2=b, medicine3=c ,medicine4=d,email=d_email)
        return render_template("receive_table.html")

@app.route('/pending', methods=["GET","POST"])
def pending():    
                userid = request.form['number1']
                conn = sqlite3.connect(database)
                cursor = conn.cursor()
                cursor.execute("UPDATE status SET status = 1 WHERE id = ?", (userid,))
                conn.commit()
                cursor.execute("SELECT  * FROM status where busiess_ID=? and status=?",(slog[-1],1))
                results = cursor.fetchall()
                heading="PENDING LIST"
                return render_template("final.html",results=results,heading=heading)


@app.route('/pend', methods=["GET","POST"])
def pend():
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("SELECT  * FROM status where busiess_ID=? and status=?",(slog[-1],1))
        results = cursor.fetchall()
        heading="PENDING LIST"
        return render_template("final.html",results=results,heading=heading)


@app.route('/accept', methods=["GET","POST"])
def accept():
           userid = request.form['number1']
           conn = sqlite3.connect(database)
           cursor = conn.cursor()
           cursor.execute("UPDATE status SET status = 2 WHERE id = ?", (userid,))
           conn.commit()
           cursor.execute("SELECT * FROM status WHERE d_email= ? and status=?", (d[-1],1))
           results = cursor.fetchall()
           return render_template("pen1.html",results=results)
                

                

@app.route('/totall_accept', methods=["GET","POST"])
def totall_accept():
           conn = sqlite3.connect(database)
           cursor = conn.cursor()
           cursor.execute("SELECT * FROM status where status = ? and busiess_ID=?",(2,slog[-1]))
           results = cursor.fetchall()
           return render_template("d_accept.html",results=results)

@app.route('/final', methods=["GET","POST"])
def final():
           userid = request.form['number']
           conn = sqlite3.connect(database)
           cursor = conn.cursor()
           cursor.execute("UPDATE status SET status = 3 WHERE id = ?", (userid,))
           cursor.execute("SELECT * FROM status WHERE busiess_ID=? and status=?", (slog[-1],3))
           conn.commit()
           results = cursor.fetchall()
           heading="SENDED LIST"
           return render_template("final.html",results=results,heading=heading)
                
@app.route('/final2', methods=["GET","POST"])
def final2():
           userid = request.form['number2']
           conn = sqlite3.connect(database)
           cursor = conn.cursor()
           cursor.execute("UPDATE status SET status = 3 WHERE id = ?", (userid,))
           conn.commit()
           cursor.execute("SELECT * FROM status WHERE busiess_ID=? and status=?", (slog[-1],3))
           results = cursor.fetchall()
           heading="SENDED LIST"
           return render_template("final.html",results=results,heading=heading)
        
@app.route('/final1', methods=["GET","POST"])
def final1():
           conn = sqlite3.connect(database)
           cursor = conn.cursor()
           cursor.execute("SELECT * FROM status WHERE busiess_ID=? and status= ?", (slog[-1],3))
           results = cursor.fetchall()
           heading="SENDED LIST"
           return render_template("final.html",results=results,heading=heading)



@app.route('/final3', methods=["GET", "POST"])                                          
def final3():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM status WHERE patient_ID=?", (plog[-1],))
    results = cursor.fetchall()
    heading="UPDATES"
    return render_template("final.html" ,results=results,back=1,heading=heading)

if __name__=='__main__':
    app.run(port=300,debug=False)
