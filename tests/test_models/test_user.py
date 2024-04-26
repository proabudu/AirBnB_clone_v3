#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

import unittest
from models.user import User

class TestUser(unittest.TestCase):

    def test_tablename(self):
        """Tests the table name based on storage type"""
        # Set storage type to 'db'
        models.storage_t = 'db'
        user = User()
        self.assertEqual(user.__tablename__, 'users')

        # Set storage type to something else
        models.storage_t = 'other'
        user = User()
        self.assertIsNone(user.__tablename__)  # or another expected value

    def test_column_definitions(self):
        """Tests presence and data types of columns"""
        user = User()
        self.assertIsInstance(user.email, sqlalchemy.Column)
        self.assertEqual(user.email.type.__class__, sqlalchemy.String)
        self.assertEqual(user.email.nullable, False)

        # Similar assertions for password, first_name, last_name

    def test_relationship_definitions(self):
        """Tests presence and types of relationships"""
        user = User()
        self.assertIsInstance(user.places, sqlalchemy.orm.relationship)
        self.assertEqual(user.places.argument, "Place")
        self.assertEqual(user.places.backref, "user")

        # Similar assertion for reviews relationship

if __name__ == '__main__':
    unittest.main()
