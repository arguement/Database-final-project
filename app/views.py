from app import app
from flask import render_template,request,redirect,url_for,flash
from werkzeug.utils import secure_filename
import os
from app import mysql
from app.forms import LoginForm,SignUpForm

@app.route("/")
def home():
    form = LoginForm()
    return render_template("login.html",form= form)

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
        print(passw)
        query = f"SELECT * FROM branch_1.account where username = '{user}' and `password` ='{passw}' "
        print(query)
        result =cur.execute(query)
        # rows = cur.fetchall()
        if result == 0:
            flash('Username or Password is incorrect.', 'danger')
            return redirect(url_for("home"))
        print(result)
        return user + passw
    flash_errors(form)
    return redirect(url_for("home"))

@app.route("/signing-up",methods =["GET","POST"])
def signing_up():
    form = SignUpForm()
    if request.method == "POST" and form.validate_on_submit():
        cur = mysql.connection.cursor()
        fname = form.fname.data
        lname = form.lname.data
        email = form.credit_card_no.data
        password = form.pas
    
    flash_errors(form)
    return redirect(url_for("SignUp"))


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