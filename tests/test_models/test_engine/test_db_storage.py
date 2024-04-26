#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import unittest
from models import amenity, base_model, city, place, review, state, user
from models.engine import DBStorage


class TestDBStorage(unittest.TestCase):
    """
    Unit tests for DBStorage class methods.
    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up the test environment before running any tests.
        """
        cls.storage = DBStorage()
        cls.user = user.User(email="test@example.com", password="test123")
        cls.place = place.Place(name="Test Place", city_id="1234")
        cls.storage.new(cls.user)
        cls.storage.new(cls.place)
        cls.storage.save()

    @classmethod
    def tearDownClass(cls):
        """
        Tears down the test environment after all tests have run.
        """
        cls.storage.delete(cls.user)
        cls.storage.delete(cls.place)
        cls.storage.save()
        cls.storage.close()

    def test_all(self):
        """
        Tests the `all` method to retrieve all objects from storage.
        """
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertIn(f"{self.user.__class__.__name__}.{self.user.id}", all_objs)
        self.assertIn(f"{self.place.__class__.__name__}.{self.place.id}", all_objs)

    def test_all_with_class(self):
        """
        Tests the `all` method with a specific class argument.
        """
        user_objs = self.storage.all(user.User)
        self.assertIsInstance(user_objs, dict)
        self.assertEqual(len(user_objs), 1)
        self.assertIn(f"{user.User.__name__}.{self.user.id}", user_objs)

    def test_new(self):
        """
        Tests the `new` method to add an object to storage.
        """
        new_amenity = amenity.Amenity(name="Test Amenity")
        self.storage.new(new_amenity)
        self.storage.save()

        amenity_obj = self.storage.get(amenity.Amenity, new_amenity.id)
        self.assertIs not None(amenity_obj)
        self.assertEqual(amenity_obj.name, "Test Amenity")

        self.storage.delete(new_amenity)
        self.storage.save()

    def test_get(self):
        """
        Tests the `get` method to retrieve an object by class and ID.
        """
        retrieved_user = self.storage.get(user.User, self.user.id)
        self.assertIsInstance(retrieved_user, user.User)
        self.assertEqual(retrieved_user.email, "test@example.com")

        # Test getting a non-existent object
        self.assertIsNone(self.storage.get(state.State, "non-existent-id"))

    def test_count(self):
        """
        Tests the `count` method to get the number of objects in storage.
        """
        total_count = self.storage.count()
        self.assertGreater(total_count, 1)  # At least 2 objects (user & place)

        user_count = self.storage.count(user.User)
        self.assertEqual(user_count, 1)


if __name__ == "__main__":
    unittest.main()
