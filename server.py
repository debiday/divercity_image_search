"""Server for image app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
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


@app.route('/user-page')
def user_page():
  """Show user's search-page."""
  # Removes ability to access this page if not logged in
  if 'email' in session:
    user = crud.get_user_by_email(session['email'])
    # session["email"] = email

    return render_template('user-page.html', user=user)
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

    return redirect('/user-page')


@app.route('/logout')
def logout():
    """Log user out of session."""

    del session['email']
    flash("Successfully logged out")
        
    return redirect('/')


# <!--------------------------------------------------------------->
# <--Routes for Account Page -->
# <!--------------------------------------------------------------->
@app.route('/save-city', methods=['POST'])
def save_tracking():
    """Save user input from html form"""

    city = request.form.get('city')

    url_front = "https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=4f2a9c7f2ea592f840664a1486e37348&text=%22";
    url_back = "+people%22&per_page=100&format=json&nojsoncallback=1";
    final_url = f'{url_front}{city}{url_back}'

    return final_url


@app.route('/account-page')
def collections_page():
  """Show user's account-page."""
  # Removes ability to access this page if not logged in
  if 'email' in session:
    user = crud.get_user_by_email(session['email'])
    # session["email"] = email

    return render_template('account-page.html', user=user)
  return redirect('/')

# TODO: Fix these two crucial routes
@app.route('/save-images', methods=["POST"])
def save_collection():
  """Creates and returns a collection to database."""

  user_id = request.form.get('user_id')
  date_saved = request.form.get('date_saved')
  notes = request.form.get('notes')

  new_collection = crud.create_collection(user_id=user_id, date_saved=date_saved, notes=notes)

  # collection_id = new_collection[collection_id]
  # print("****finding collection id****")
  # print(collection_id)
  collection_str = str(new_collection)
  collection_id = int(collection_str[26:29])
  print("******collection id*******")
  print(collection_id)
  print("******list of selected images*******")
  urls = request.form.get("selected")
  print(request.form) 
  print(str(urls))


  if new_collection:
    flash("Your images have been saved in your saved searches.")

  return "Your images have been saved in your saved searches."
# <___Working_____>

  # if request.method == 'POST':
  #     image_list = request.form.getlist('selected')
  #     print(request.form.getlist('1'))

  # # for url in image_list:
  # #   save_picture = crud.create_picture(collection_id, url)
  # return str(image_list)

  # new_pictures = crud.create_picture(collection_id=collection_id, url=url)


# @app.route('/save-images', methods=["POST"])
# def save_images():
#   """Create and return new pictures."""

#   if request.method == 'POST':
#       print(request.form.getlist('selected'))
#       return 'Done!'
    
#     # for url in image_list:
#     #   save_picture = crud.create_picture(collection_id, url)
#   return redirect

# <_______________working____________________>


  # TODO: In AJAX event listener?
  # for __ in ____, 
  #   new_picture = crud.create_picture(collection_id, url)
  


  # if new_collection:
  #   flash("Your images have been saved in your collection.")

  # return "Your images have been saved in your collection."


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
