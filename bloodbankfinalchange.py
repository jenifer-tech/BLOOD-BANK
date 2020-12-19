from flask import Flask,request,jsonify  
import json
import pymysql
import re



app=Flask(__name__)

def db_connection():    

    conn=None

    try:
        conn=pymysql.connect(   host='sql12.freemysqlhosting.net',
                                database='sql12375682',
                                user='sql12375682',
                                password='nL9hwqHpV7',
                                cursorclass=pymysql.cursors.DictCursor
                            )
    except pymysql.Error as e :
        print(e)    
    return conn   


def exe_query(conn,cursor):
    conn=db_connection()
    cursor=conn.cursor()  
    return conn,cursor   

def validation(new_name,new_location,new_email,new_gender,new_mobileno,new_bloodgroup):
    if not new_name or not new_location or not new_email or not new_gender or not new_mobileno or not new_bloodgroup:
        return "Please enter all values"
    elif not new_name.isalpha():
        return "Name allowed only strings"
    elif not new_location.isalpha():
        return "Location allowed only strings"
    elif not re.match  (r'[^@]+@[^@]+\.[^@]+',new_email):   
        return "Invalid Email address " 
    elif not  new_gender.isalpha():
        return "Invalid gender"
    elif not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),new_mobileno):    
        return"Mobile no must contain only 10 numbers"    
    elif not re.match (r'^(a|b|ab|o)[+-]$',new_bloodgroup):   
        return "Invalid blood group " 

    
@app.route("/adddonar",methods=["POST"])  
def adddonar():
    a,b=exe_query('con','cursor')
    
    new_name=request.form['name']   
    new_location=request.form['location']
    new_email=request.form['email']
    new_gender=request.form['gender']
    new_mobileno=request.form['mobileno']
    new_bloodgroup=request.form['bloodgroup']
    
    error_msg=validation(new_name,new_location,new_email,new_gender,new_mobileno,new_bloodgroup)
    if error_msg:
        return jsonify({"message":error_msg}),400
    b.execute('SELECT * FROM blood WHERE name=%s' ,(new_name,))      
    acc=b.fetchone()
    if acc:
        return jsonify({"message":"Blood Donar {} account already exist!".format(new_name)}),200             
    else:
        que="""INSERT INTO blood(name,location,email,gender,mobileno,bloodgroup)
                                VALUES (%s,%s,%s,%s,%s,%s)"""

        b.execute(que,(new_name,new_location,new_email,new_gender,new_mobileno,new_bloodgroup))
        a.commit()
        return jsonify({"message":"Blood Donar {} ({}) added successfully!".format(new_name,new_bloodgroup)}),201



@app.route("/searchdonar",methods=['POST'])
def searchdonnar():
    
    
    new_bloodgroup=request.form.get('bloodgroup')
    new_location=request.form.get('location') 
    new_gender=request.form.get('gender') 
    new_email=request.form.get('email')
    a,b=exe_query('con','cursor')  

    x="SELECT * FROM blood where"    
    if new_bloodgroup and new_gender and new_location:   
        y1="location=%s and  bloodgroup=%s and  gender=%s"  
        c1="% s % s" % (x, y1)       
        b.execute(c1,(new_location , new_bloodgroup , new_gender,))
        account=b.fetchall()              
        return jsonify(account),200       
    elif new_bloodgroup and new_gender: 
        y2=" bloodgroup=%s and  gender=%s"
        c2="%s%s" % (x,y2)
        b.execute(c2,(new_bloodgroup , new_gender,))
        account=b.fetchall()              
        return jsonify(account),200   
    elif new_bloodgroup and new_location:
        y3="bloodgroup=%s and location=%s"
        c3="% s % s" % (x,y3)
        b.execute(c3,(new_bloodgroup,new_location))
        account=b.fetchall()              
        return jsonify(account),200   
    elif new_location and new_gender:
        y4="location=%s and gender=%s"
        c4="% s % s" % (x,y4)
        b.execute(c4,(new_location,new_gender))
        account=b.fetchall()              
        return jsonify(account),200  
   
    elif new_bloodgroup:
        y5="bloodgroup=%s"    
        c5="%s %s" % (x,y5)
        b.execute(c5,(new_bloodgroup))
        account=b.fetchall()
        return jsonify(account),200

    elif new_gender:
        y6="gender=%s"    
        c6="%s %s" % (x,y6)
        b.execute(c6,(new_gender))
        account=b.fetchall()
        return jsonify(account),200

    elif new_location:
        y7="location=%s"    
        c7="%s %s" % (x,y7)
        b.execute(c7,(new_location))
        account=b.fetchall()
        return jsonify(account),200
    elif new_email:
        y8="email=%s"    
        c8="%s %s" % (x,y8)
        b.execute(c8,(new_email))
        account=b.fetchall()
        return jsonify(account),200    
    return jsonify({"message":"Please....You have select valid resonse!"})

@app.route("/updatedonar/<int:id>",methods=['PUT'])
def update(id):
    a,b=exe_query('con','cursor')
    sql="""UPDATE blood SET name=%s,location=%s,email=%s,gender=%s,mobileno=%s,bloodgroup=%s WHERE id=%s""" 
    new_name=request.form['name']   
    new_location=request.form['location']
    new_email=request.form['email']
    new_gender=request.form['gender']
    new_mobileno=request.form['mobileno']
    new_bloodgroup=request.form['bloodgroup']
    update_donar={"id":id,
                 "name":new_name,
                 "location":new_location,
                 "email":new_email,
                 "gender":new_gender,
                 "mobileno":new_mobileno,
                 "bloodgroup":new_bloodgroup
    }               
    b.execute(sql,(new_name,new_location,new_email,new_gender,new_mobileno,new_bloodgroup,id))
    a.commit()
    return jsonify(update_donar) 

@app.route("/deletedonar",methods=['DELETE'])
def delete():
    a,b=exe_query('con','cursor')  
    new_email=request.form['email']
    b.execute("""SELECT * FROM blood where email=%s""",(new_email,)) 
    account=b.fetchone()      
    if account:
        sql_del="""DELETE FROM blood WHERE email=%s""" 
        b.execute(sql_del,(new_email,))
        a.commit()
        return jsonify({"message":"Blood donar {} account  has been deleted  successfully!.".format(new_email)}),200
    else:    
        return jsonify({"message":"Please enter correct Email Id "}),401 


if __name__=='__main__':
    app.run(debug=True) 
