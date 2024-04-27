import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine import DBStorage
from models.user import User
from models.__init__ import metadata
from file_storage import FileStorage


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FileStorage()
        self.user1 = User(email="john.doe@example.com", password="secret")
        self.user2 = User(email="jane.doe@example.com", password="secret2")
        self.storage.new(self.user1)
        self.storage.new(self.user2)
        self.storage.save()

    def tearDown(self):
        self.storage.delete(self.user1)
        self.storage.delete(self.user2)
        self.storage.save()
        DBStorage.close()
        metadata.drop_all(DBStorage().engine)

    def test_get_all(self):
        all_objs = self.storage.all()
        self.assertEqual(len(all_objs), 2)
        self.assertIsInstance(all_objs[next(iter(all_objs))], User)

    def test_get_all_by_class(self):
        user_objs = self.storage.all(User)
        self.assertEqual(len(user_objs), 2)
        for obj in user_objs.values():
            self.assertIsInstance(obj, User)

    def test_get_none(self):
        self.assertIsNone(self.storage.get(None, "123"))
        self.assertIsNone(self.storage.get(User, "non-existent-id"))

    def test_get_by_class_and_id(self):
        user1_retrieved = self.storage.get(User, self.user1.id)
        self.assertEqual(user1_retrieved, self.user1)

    def test_count(self):
        self.assertEqual(self.storage.count(), 2)
        self.assertEqual(self.storage.count(User), 2)
        self.assertEqual(self.storage.count(Amenity), 0)  # No Amenity objects created

if __name__ == "__main__":
    unittest.main()
