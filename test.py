import model 
import crud
import os
from unittest import TestCase
from server import app
from flask import session
from model import User, Collection, Picture, connect_to_db, db

def example_data():
    """Create sample data"""

    user1 = crud.create_user('user@user.com', 'test')
    user2 = crud.create_user('user2@user.com', 'test')

    db.session.add_all([user1, user2])
    db.session.commit()


class FlaskIntegrationTests(TestCase):
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
        self.assertIn(b'<h1 style="text-align: center;">Welcome!</h1>', result.data)

    def test_return_url(self):
        """Check images load with user input."""

        client = app.test_client()
        result = client.post('/save-city', data={'city': 'california'})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"https://www.flickr.com/", result.data)

    # def test_user_creation(self):
    #     client = app.test_client()
    #     result = client.post('/newusers', data={'email': 'test@user.com',
    #                                             'password': 'test1',                    
    #                                             })
    #     self.assertIn(b"!", result.data)

    def test_create_user(self):
        """Check user creation."""

        result = self.client.post('/newusers',
                                  data={'email': 'user1@user.com',
                                        'password': 'test1'},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Please', result.data) 
        

class LoggedIn(TestCase):
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


    # def test_login(self):
    #     """Check account page loads."""
    #     result = self.client.post('/account-page', 
    #                               data={'email': 'user2@user.com',
    #                                     'password': 'test2'},
    #                               follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'Logout', result.data)

    def test_login(self):
        """Test login to account"""

        result = self.client.post('/login',
                                   data={'email': 'user1@user.com',
                                        'password': 'test'},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<div id="image-results">', result.data)
    

if __name__ == "__main__":
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')

    unittest.main(verbosity=2)
