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
        user = form.username.data
        passw = form.password.data
        return user + passw
    return "home page"


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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")