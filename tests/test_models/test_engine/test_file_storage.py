#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine import storage  # Assuming storage
from models.user import User


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.obj1 = User(name="John", email="john@doe.com", password="secret")
        self.obj2 = Amenity(name="wifi")
        storage.new(self.obj1)
        storage.new(self.obj2)
        storage.save()

    def tearDown(self):
        storage.delete(self.obj1)
        storage.delete(self.obj2)
        storage.save()

    def test_all(self):
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertEqual(len(all_objs), 2)

    def test_all_filtered(self):
        user_objs = storage.all(User)
        self.assertIsInstance(user_objs, dict)
        self.assertEqual(len(user_objs), 1)
        self.assertEqual(user_objs["User.{}".format(self.obj1.id)], self.obj1)

    def test_new(self):
        new_obj = User(name="Jane", email="jane@doe.com", password="secret2")
        storage.new(new_obj)
        storage.save()
        retrieved_obj = storage.get(User, new_obj.id)
        self.assertEqual(retrieved_obj, new_obj)
        storage.delete(new_obj)
        storage.save()

    def test_get(self):
        retrieved_obj = storage.get(User, self.obj1.id)
        self.assertEqual(retrieved_obj, self.obj1)
        self.assertIsNone(storage.get(User, "non-existent-id"))

    def test_count(self):
        self.assertEqual(storage.count(), 2)
        self.assertEqual(storage.count(User), 1)

    def test_save(self):
        # Saving already calls self.reload(), so no separate test needed


if __name__ == "__main__":
    unittest.main()
