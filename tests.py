import model 
import flask
import crud
import server
import os
from unittest import TestCase
from model import User, Collection, Picture, connect_to_db, db

# class ChildTestCase(TestCase):
    
#     def test_index(self):
#         self.assertEqual(crud.get_child_by_id(1), "<Child name=Katele Caldera missing_age=17 >")



class FlaskIntegrationTestCase(TestCase):
    """Testing flask server"""
    def setUp(self):
        """Stuff to do before every test."""

    # Get the Flask test client
    client = server.app.test_client()

    # Show Flask errors that happen during tests
    server.app.config['TESTING'] = True

    # Connect to test database
    connect_to_db(server.app, "postgresql:///testdb")

    # Create tables
    db.create_all()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_homepage(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b'<h1 style="text-align: center;">Welcome!</h1>', result.data)

    def test_return_url(self):
        client = server.app.test_client()
        result = client.post('/save-city', data={'city': 'california'})
        self.assertIn(b"https://www.flickr.com/", result.data)

    # def test_create_user(self):
        
    

if __name__ == "__main__":
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')

    unittest.main(verbosity=2)
