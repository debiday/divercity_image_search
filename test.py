import model 
import crud
import os
from unittest import TestCase
from server import app
from flask import session
from model import User, Collection, Picture, connect_to_db, db

def example_data():
    """Create sample data"""

    User.query.delete()
    Collection.query.delete()
    Picture.query.delete()

    user1 = crud.create_user('user@user.com', 'test')
    user2 = crud.create_user('user2@user.com', 'test')

    collection1 = crud.create_collection(1, "notes", "01/01/2021")
    collection2 = crud.create_collection(2, "notes", "01/01/2021")

    picture1 = crud.create_picture(1, "google.com")
    picture2 = crud.create_picture(2, "google.com")

    db.session.add_all([user1, user2])
    db.session.commit()


class FlaskTests(TestCase):
    """Testing flask server"""

    def setUp(self):
        """Stuff to do before every test."""

    # Get the Flask test client
    client = app.test_client()

    # Show Flask errors that happen during tests
    app.config['TESTING'] = True
    
    # Connect to test database
    connect_to_db(app, "postgresql:///testdb")

    # Create tables
    db.create_all()


    def tearDown(self):
        """Do at end of every test."""
        
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        

    def test_homepage(self):
        """Check homepage loads."""

        client = app.test_client()
        result = client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<p>Already have an account? <a href="/">Sign in</a>.</p>', result.data)


    def test_return_images(self):
        """Check images load with user input."""

        client = app.test_client()
        result = client.post('/save-city', data={'city': 'california'})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"https://www.flickr.com/", result.data)


    def test_create_user(self):
        """Check user creation."""

        result = self.client.post('/newusers',
                                  data={'register-email': 'user1@user.com',
                                        'register-password': 'test1'},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'account has been created', result.data) 


class FlaskTestsLoggedIn(TestCase):
    """Flask tests that use the database while user is logged in""" 

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'placeholderkey'
        self.client = app.test_client()

        connect_to_db(app, 'postgresql:///testdb', echo=False)

        db.create_all()
        example_data()


    def tearDown(self):
        """Stuff to do after each test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    def test_login(self):
        """Test login to account"""

        result = self.client.post('/login',
                                   data={'email': 'user1@user.com',
                                        'password': 'test'},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div id="image-results">', result.data)


    def test_query_collection(self):
        """Check collection query."""

        self.assertEqual(str(crud.get_collections()), "[<Collection collection_id=1 user=1>, <Collection collection_id=2 user=2>]")


    def test_query_collection_by_id(self):
        """Check collection_id query."""

        self.assertEqual(str(crud.get_collection_by_id(1)), "<Collection collection_id=1 user=1>")


    def test_get_collection_by_email(self):
        """Check query by email returns all collections"""

        self.assertEqual(str(crud.get_collection_by_email("user@user.com")), "[<Collection collection_id=1 user=1>]")


    def test_get_pictures_by_collection(self):
        """Check query by collections returns all pictures"""

        self.assertEqual(str(crud.get_pictures_by_collection(1)), "[<Picture picture_id=1 URL=google.com>]")



    def test_create_collection(self):
        """Check collection creation"""

        self.assertEqual(str(crud.create_collection(1, "notes", "01/01/2021")), "<Collection collection_id=3 user=1>")


    def test_create_picture(self):
        """Check picture creation"""

        crud.create_collection(1, "notes", "01/01/2021")
        self.assertEqual(str(crud.create_picture(1, "google.com")), "<Picture picture_id=3 URL=google.com>")


if __name__ == "__main__":
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')

    unittest.main(verbosity=2)
