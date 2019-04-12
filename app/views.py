from app import app
from flask import render_template,request,redirect,url_for,flash,session,jsonify
from werkzeug.utils import secure_filename
import os
from app import mysql
from app.forms import LoginForm,SignUpForm,PurchaseForm
from datetime import datetime

@app.route("/")
def home():
    form = LoginForm()
    return render_template("login.html",form= form)

@app.route("/",methods=["POST","GET"])
def comment_sub():
    if request.method == "POST":

        cur = mysql.connection.cursor()

        item_name = request.form["item_name"]
        cusid = request.form["cusid"]
        id = request.form["id"]
        comment = request.form["comment"]
        branch = session['branch']
        cur = mysql.connection.cursor()
        query = f"select fname,lname from branch_{branch}.customer where customerId = {cusid} "
        cur.execute(query)
        res = cur.fetchone()
        fname = res[0]
        lname = res[1]
        fullname = fname + " "+ lname
        print("here")
        query = f"insert into branch_{branch}.review(customerId,comments ) values({cusid},'{comment}')"
        print(query)
        cur.execute(query)
        return render_template("comments.html",fullname=fullname,comment=comment)
    return 'comment not added'

@app.route("/search")
def search():
    return render_template("search.html")

    

@app.route("/get_items", methods=['GET'])
def get_items():
    items = []
    cur = mysql.connection.cursor()
    for i in range(1,4):

        query = f"SELECT brand,item_name,item_type,item_amt,itemId,price  FROM branch_{i}.items limit 5 "
        cur.execute(query)
        res = cur.fetchall()
        for rows in res:
            items.append( {"brand":rows[0],"item_name":rows[1],"item_type":rows[2],"item_amt":rows[3],"itemId":rows[4],"price":rows[5] } )


    return jsonify( items )
    # return jsonify(data={"user": user}, message="Success")

@app.route("/item_purchase/<id>",methods=["POST","GET"])
@app.route("/item_purchase",methods=["POST","GET"])
def purchase(id = None):
    print(id)
    form = PurchaseForm()
    if request.method == "POST":
        if form.validate_on_submit():
           # cur = mysql.connection.cursor()

            # username = form.username.data
            # password = form.password.data
            credit = form.credit_card.data
            amt = form.amt.data
            id = request.form["id"]
            print(f"id is {id}")
            cur = mysql.connection.cursor()
            to_use = [0,0]
            for i in range(1,4):
                print("arrives")
                query = f"SELECT item_amt FROM branch_{i}.items WHERE itemId = {id}"
                cur.execute(query)
                val = int( cur.fetchone()[0] )

                if val > to_use[1]:
                    to_use[1] = val
                    to_use[0] = i
            branch = to_use[0]
            val = to_use[1] 
            query = f"update branch_{branch}.items set item_amt = item_amt - {amt} where itemId = {id}"
            cur.execute(query)
            print("first")
            #query = f"inse"
            # print(session['userid'])
            cusid = session["userid"] # dummy customer id
            # pucrhase table (itemId 	customerId 	purchase_amt )
            # query = f'insert into purchase values({id},{cusid},{amt})'
            query = f"select item_name,price from branch_{branch}.items where itemId = {id} "
            cur.execute(query)
            res = cur.fetchone()
            print("second")
            query = f"insert into branch_{branch}.receipt( itemId,customerId ) values( {id},{cusid} )"
            cur.execute(query)
            # query to get the receit id 
            query = f"select receipt_num from branch_{branch}.receipt where itemId = {id} and customerId={cusid}"
            cur.execute(query)
            receipt_num = cur.fetchone()[0]

            flash("purchase complete","success")
            return render_template("receipt.html",item_name=res[0],price =res[1],amt = amt,id=id,receipt_num=receipt_num,cusid=cusid,branchnum=branch)

    

        flash_errors(form)
        return redirect(url_for("purchase"))

    if not id == None:
        cur = mysql.connection.cursor()
        for i in range(1,4):
            query = f"SELECT * FROM branch_{i}.items WHERE itemId = {id}"
            res = cur.execute(query)
            if res > 0:
                row = cur.fetchone() 
                branch = row[1]
                name = row[2]
                types = row[3]
                amt = int(row[4])
                price = int(row[5])
                return render_template("item.html",form =form,branch = branch,name= name, types = types,amt = amt,price = price,id=id)
    flash_errors(form)
    return render_template("item.html",form=form)

@app.route("/get_specific_item/<item>")
def get_item(item):
    cur = mysql.connection.cursor()
    query = f"SELECT brand,item_name,item_type,item_amt,itemId FROM branch_1.items WHERE item_name like '%{ item }%'"
    res = cur.execute(query)
    rows = cur.fetchone()
    item = {"brand":rows[0],"item_name":rows[1],"item_type":rows[2],"item_amt":rows[3],"itemId":rows[4] } 
    print("here")
    return jsonify( [item] )


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
        result = 0
        for i in range(1,4):
       
            query = f"SELECT * FROM branch_{i}.account where username = '{user}' and `password` ='{passw}' "
            print(query)
            
            result =cur.execute(query)
            print(result)
            if result > 0:
                queryToUse = query
                userfind = True
                data = cur.fetchone()
                session['branch'] = i
                break
        if result == 0:
            flash('Username or Password is incorrect.', 'danger') 
            return redirect(url_for("home"))

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
        return render_template("home_page.html")
    flash_errors(form)
    return redirect(url_for("home"))

@app.route("/testing_home")
def test():
    return render_template("home_page.html")


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
        flash("account created","success")
        return redirect(url_for("home"))
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


# @app.errorhandler(404)
# def page_not_found(error):
#     """Custom 404 page."""
#     return render_template('404.html'), 404

@app.context_processor
def utility_processor():
    def getDate():
        return datetime.today().strftime('%Y-%m-%d')
    return dict(getDate=getDate)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")