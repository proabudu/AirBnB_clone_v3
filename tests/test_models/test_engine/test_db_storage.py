import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine import DBStorage
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary engine for testing
        cls.engine = create_engine('sqlite:///:memory:')
        # Bind the engine to the global metadata object
        Base.metadata.create_all(cls.engine)

        # Set up a temporary session for testing
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after tests are finished
        Base.metadata.drop_all(cls.engine)
        # Close the session
        cls.session.close()

    def setUp(self):
        self.db = DBStorage()
        self.db.reload()  # Create all tables

        self.user1 = User(email="john.doe@example.com", password="secret")
        self.user2 = User(email="jane.doe@example.com", password="secret2")
        self.db.new(self.user1)
        self.db.new(self.user2)
        self.db.save()

    def tearDown(self):
        self.db.delete(self.user1)
        self.db.delete(self.user2)
        self.db.save()

    def test_all(self):
        all_objs = self.db.all()
        self.assertEqual(len(all_objs), 2)
        self.assertIsInstance(all_objs[next(iter(all_objs))], User)

    def test_all_by_class(self):
        user_objs = self.db.all(User)
        self.assertEqual(len(user_objs), 2)
        for obj in user_objs.values():
            self.assertIsInstance(obj, User)

    def test_get_none(self):
        self.assertIsNone(self.db.get(None, "123"))
        self.assertIsNone(self.db.get(User, "non-existent-id"))

    def test_get_by_class_and_id(self):
        user1_retrieved = self.db.get(User, self.user1.id)
        self.assertEqual(user1_retrieved, self.user1)

    def test_count(self):
        self.assertEqual(self.db.count(), 2)
        self.assertEqual(self.db.count(User), 2)
        self.assertEqual(self.db.count(Amenity), 0)  # No Amenity objects created

if __name__ == "__main__":
    unittest.main()
