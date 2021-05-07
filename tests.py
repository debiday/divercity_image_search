import model 
import flask
import crud
import server
from unittest import TestCase





class FlaskIntegrationTestCase(TestCase):
    """Testing flask server"""

    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b"<h1>Welcome!</h1>", result.data)
    

if __name__ == "__main__":
    #if called like a script, run our tests
    import unittest

    unittest.main(verbosity=2)
