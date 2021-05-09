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
app.secret_key = "placeholderkey"
#for production replace "placeholderkey" with os.environ["FLASK_KEY"]
app.jinja_env.undefined = StrictUndefined


# <!--------------------------------------------------------------->
# <--Search with Flickr API -->
# <!--------------------------------------------------------------->
api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/save-city', methods=['POST'])
def save_tracking():
    """Save user input from html form"""

    city = request.form.get('city')

    url_front = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=4f2a9c7f2ea592f840664a1486e37348&text=%22";
    url_back = "+people%22&per_page=100&format=json&nojsoncallback=1";
    final_url = f'{url_front}{city}{url_back}'

    return final_url


# <!--------------------------------------------------------------->
# <--Routes for User -->
# <!--------------------------------------------------------------->
@app.route('/newusers', methods = ["POST"])
def register_user():
  """Saves user information to database"""
  
  email = request.form.get('register-email')
  password = request.form.get('register-password')

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

    return redirect('/account-page')


@app.route('/logout')
def logout():
    """Log user out of session."""

    del session['email']
    flash("Successfully logged out")
        
    return redirect('/')


# <!--------------------------------------------------------------->
# <--Routes for Account Page -->
# <!--------------------------------------------------------------->
@app.route('/account-page')
def user_page():
  """Show user's account-page."""
  # Removes ability to access this page if not logged in
  if 'email' in session:
    user = crud.get_user_by_email(session['email'])
    # session["email"] = email

    return render_template('account-page.html', user=user)
  return redirect('/')

@app.route('/save_images', methods=['POST'])
def save_images():
  """Save images from form."""

  collection_id = request.form.get('collection_id')

  if request.method == 'POST':
    image_list = request.form.getlist('selected')
  
  # for url in image_list:
  #   save_picture = crud.create_picture(collection_id, url)
  return str(image_list)

  

  # save_images_count = 0
  # saved_images = request.form.get('selected')
  # print(saved_images)
  # if saved_images == True :
  #   save_images_count += 1
  # else :
  #   pass
  # print(save_images_count)
  return redirect


 


# @app.route('/create-saved-picture', methods=["POST"])
# def create_picture():
#   """Saves images to db."""

#   collection_id = request.form.get('collection_id')
#   url = request.form.get('url')

#   new_picture = crud.create_picture(collection_id, url)

#   return new_picture

# @app.route('/create-saved-picture', methods=["POST"])
# def create_picture():
#   """Saves images to db."""

#   collection_id = request.form.get('collection_id')
#   url = request.form.get('url')

#   new_picture = crud.create_picture(collection_id, url)

#   return new_picture

  # TODO: In AJAX event listener?
  # for __ in ____, 
  #   new_picture = crud.create_picture(collection_id, url)
  


  # if new_collection:
  #   flash("Your images have been saved in your collection.")

  # return "Your images have been saved in your collection."


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
