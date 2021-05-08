import model 
import flask
import crud
import server
import os
from unittest import TestCase
from model import User, Collection, Picture, connect_to_db, db

class FlaskIntegrationTests(TestCase):
    """Testing flask server"""

    def setUp(self):
        """Stuff to do before every test."""

    # Get the Flask test client
    client = server.app.test_client()

    # Show Flask errors that happen during tests
    server.app.config['TESTING'] = True

    server.app.config['LOGIN_DISABLED'] = True

    # Connect to test database
    connect_to_db(server.app, "postgresql:///testdb")

    # Create tables
    db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        
    def test_homepage(self):
        """Check homepage loads."""

        client = server.app.test_client()
        result = client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1 style="text-align: center;">Welcome!</h1>', result.data)

    def test_return_url(self):
        """Check images load with user input."""

        client = server.app.test_client()
        result = client.post('/save-city', data={'city': 'california'})
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"https://www.flickr.com/", result.data)

    # def test_user_creation(self):
    #     client = server.app.test_client()
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

    # def test_account(self):
    #     """Check account page loads."""

    #     result = self.client.get('/account-page', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'logout', result.data)

# class LoggedIn(TestCase):
#     """Testing routes that require user login"""

    #     # # # TODO: How to add sessions
    # def test_favorites(self):
    #     """Check account page loads."""

    #     result = self.client.get('/account-page')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'logout', result.data)

# class LoggedIn(TestCase):
#     """Flask tests that use the database while user is logged in""" 

#     def setUp(self):
#         """Stuff to do before every test."""

#         server.app.config['TESTING'] = True
#         server.app.config['SECRET_KEY'] = 'placeholderkey'
#         self.client = server.app.test_client()

#         connect_to_db(server.app, 'postgresql:///testdb', echo=False)

#         db.create_all()

#         self.client.post('/login', data={"email": "user1@user.com", "password": "test1"}, follow_redirects=True)



#     def tearDown(self):
#         """Stuff to do after each test."""

#         db.session.remove()
#         db.drop_all()
#         db.engine.dispose()


    # def test_login(self):
    #     """Check account page loads."""

    #     result = self.client.post('/account-page', follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'logout', result.data)


    

if __name__ == "__main__":
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')

    unittest.main(verbosity=2)
