from app import app
from flask import render_template,request,redirect,url_for,flash,session
from werkzeug.utils import secure_filename
import os
from app import mysql
from app.forms import LoginForm,SignUpForm,PurchaseForm

@app.route("/")
def home():
    form = LoginForm()
    return render_template("login.html",form= form)

@app.route("/item_purchase",methods=["POST","GET"])
def purchase():
    form = PurchaseForm()
    if request.method == "POST":
        if form.validate_on_submit():
           # cur = mysql.connection.cursor()

            username = form.username.data
            password = form.password.data
            credit = form.credit_card.data
            amt = form.amt.data

            cur = mysql.connection.cursor()
            to_use = [0,0]
            for i in range(1,4):
                pass
                query = f"SELECT item_amt FROM branch_{i}.items WHERE itemId = {1}"
                cur.execute(query)
                val = cur.fetchone()[5]

                if val > to_use[1]:
                    to_use[1] = val
                    to_use[0] = i
            branch = to_use[0]
            query = f"update branch_{branch}.items set item_amt = item_amt - {1} where itemId = {1} "
            
            return 'purchased'
        flash_errors(form)
        return redirect(url_for("purchase"))
    return render_template("item.html",form=form)

@app.route("/sign_up")
def SignUp():
    form = SignUpForm()
    return render_template("signUp.html",form = form)

@app.route("/home_page",methods =["GET","POST"])
def store():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():

        cur = mysql.connection.cursor()

        user = form.username.data
        passw = form.password.data + "\\"+"r"

        userfind = False
        queryToUse = ''
        data = ''
        for i in range(1,4):
       
            query = f"SELECT * FROM branch_{i}.account where username = '{user}' and `password` ='{passw}' "
            print(query)
            
            result =cur.execute(query)
            print(result)
            if result > 0:
                queryToUse = query
                userfind = True
                data = cur.fetchone()
                break
        # lst.append(result)
        # lst.append( cur.execute(f"SELECT * FROM branch_2.account where username = '{user}' and `password` ='{passw}'")) 
        # lst.append( cur.execute(f"SELECT * FROM branch_3.account where username = '{user}' and `password` ='{passw}'")) 

        # rows = cur.fetchall()
        # branch = 1
        
        if user == False:
            flash('Username or Password is incorrect.', 'danger') 
            return redirect(url_for("home"))
        
        session['userid'] = data[0]
        session['login'] = True
        print(data)
        print(f"session is {session}")
        return user + passw
    flash_errors(form)
    return redirect(url_for("home"))

@app.route("/signing-up",methods =["GET","POST"])
def signing_up():
    form = SignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        # cur = mysql.connection.cursor()
        
        fname = form.fname.data
        lname = form.lname.data
        credit_card = form.credit_card_no.data
        password = form.password.data
        branch = form.branch.data
        email = form.email.data
        add_sign_up_data_to_branch(branch,fname,lname,credit_card,password,email)
        return 'diandra screen'
    flash_errors(form)
    return redirect(url_for("SignUp"))

def add_sign_up_data_to_branch(branch,fname,lname,credit_card,password,email):
    password = password + "\\"+"r"
    credit_card = credit_card + "\\"+"r"
    cur = mysql.connection.cursor()
    query = ""
    if branch == "Branch 1":
        checkuser = cur.execute(f"select * from branch_1.account where username= '{email}' ")
        if checkuser > 0:
            flash("email already exist","danger")
            return redirect(url_for("SignUp"))
        
        checkuser = cur.execute(f"select * from branch_1.customer where credit_card_no = '{credit_card}' ")
        if checkuser > 0:
            flash("credit card already exist","danger")
            return redirect(url_for("SignUp"))

        query = f"insert into branch_1.account(username,password) values('{email}' ,'{password}') "
        cur.execute(query)
        
        query2 = f"insert into branch_1.customer(lname,fname,credit_card_no) values('{lname}' ,'{fname}','{credit_card}')"
        cur.execute(query2)
        
        query3 = f"select account_id from branch_1.account where username = '{email}' and password = '{password}' "

        account_id = cur.execute(query3)
        account_id = cur.fetchone()[0]
        print(f"customerId is {account_id }")

        query4 = f"select customerId from branch_1.customer where lname = '{lname}' and fname= '{fname}' and  credit_card_no = '{credit_card}'  "

        customerId = cur.execute(query4)
        customerId = cur.fetchone()[0]
        print(f"customerId is {customerId}")
        query5 = f"insert into branch_1.owns values({customerId},{account_id})"
        cur.execute(query5)
        mysql.connection.commit()
    elif branch == "Branch 2":
        checkuser = cur.execute(f"select * from branch_2.account where username= '{email}' ")
        if checkuser > 0:
            flash("email already exist","danger")
            return redirect(url_for("SignUp"))
        
        checkuser = cur.execute(f"select * from branch_2.customer where credit_card_no = '{credit_card}' ")
        if checkuser > 0:
            flash("credit card already exist","danger")
            return redirect(url_for("SignUp"))

        query = f"insert into branch_2.account(username,password) values('{email}' ,'{password}') "
        cur.execute(query)
        
        query2 = f"insert into branch_2.customer(lname,fname,credit_card_no) values('{lname}' ,'{fname}','{credit_card}')"
        cur.execute(query2)
        
        query3 = f"select account_id from branch_2.account where username = '{email}' and password = '{password}' "

        account_id = cur.execute(query3)
        account_id = cur.fetchone()[0]
        print(f"customerId is {account_id }")

        query4 = f"select customerId from branch_2.customer where lname = '{lname}' and fname= '{fname}' and  credit_card_no = '{credit_card}'  "

        customerId = cur.execute(query4)
        customerId = cur.fetchone()[0]
        print(f"customerId is {customerId}")
        query5 = f"insert into branch_2.owns values({customerId},{account_id})"
        cur.execute(query5)
        mysql.connection.commit()
    else:
        checkuser = cur.execute(f"select * from branch_2.account where username= '{email}' ")
        if checkuser > 0:
            flash("email already exist","danger")
            return redirect(url_for("SignUp"))
        
        checkuser = cur.execute(f"select * from branch_2.customer where credit_card_no = '{credit_card}' ")
        if checkuser > 0:
            flash("credit card already exist","danger")
            return redirect(url_for("SignUp"))

        query = f"insert into branch_2.account(username,password) values('{email}' ,'{password}') "
        cur.execute(query)
        
        query2 = f"insert into branch_2.customer(lname,fname,credit_card_no) values('{lname}' ,'{fname}','{credit_card}')"
        cur.execute(query2)
        
        query3 = f"select account_id from branch_2.account where username = '{email}' and password = '{password}' "

        account_id = cur.execute(query3)
        account_id = cur.fetchone()[0]
        print(f"customerId is {account_id }")

        query4 = f"select customerId from branch_1.customer where lname = '{lname}' and fname= '{fname}' and  credit_card_no = '{credit_card}'  "

        customerId = cur.execute(query4)
        customerId = cur.fetchone()[0]
        print(f"customerId is {customerId}")
        query5 = f"insert into branch_1.owns values({customerId},{account_id})"
        cur.execute(query5)
        mysql.connection.commit()

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")