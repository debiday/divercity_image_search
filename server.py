"""Server for image app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
import json
import os
import flickrapi

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ["FLASK_KEY"]
app.jinja_env.undefined = StrictUndefined

# <------------FLICKR API------------>

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]


# <---------------------------------->

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/save-city', methods=['POST'])
def save_tracking():
    """Save user input from html form"""

    city = request.form.get('city')

    return city
    




# <!--------------------------------------------------------------->
# <--Routes for User -->
# <!--------------------------------------------------------------->
@app.route('/registration')
def show_registration():
    """Show registration page."""

    return render_template("registration.html")


@app.route('/newusers', methods = ["POST"])
def register_user():
  """Saves user information to database"""
  
  email = request.form.get('email')
  password = request.form.get('password')

  user = crud.get_user_by_email(email)

  if user: 
    flash('Email is already in use. Please log in.')
  else:
    user = crud.create_user(email, password)
    session["email"] = email
    flash('Your account has been created! Please log in.')

  return redirect('/')
  

@app.route('/login', methods = ['POST'])
def submit_login_form():
  """Submits the login form."""

  user = crud.get_user_by_email(request.form['email'])
  password = request.form['password']

  if user == None:
    flash('''An account for this email doesn't exist yet.
              Please create a new account.''')
    return redirect('/')
  elif password != user.password:
    flash('Wrong password. Please try again.')
    return redirect('/')

  else: 
    flash('Logged in!')
    session['email'] = user.email

    return redirect('/tracking-page')


@app.route('/logout')
def logout():
    """Log user out of session."""

    del session['email']
    flash("Successfully logged out")
        
    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
