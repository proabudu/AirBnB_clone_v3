#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import unittest
from models import storage
from models.base_model import BaseModel
from io import StringIO  # to simulate user input/output

class TestHBNBCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Resets the storage for each test"""
        storage.all().clear()

    def test_create_valid(self):
        """Tests creating a valid instance"""
        # Simulate user input
        user_input = "create User name=\"John\" email=\"john@example.com\""
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect output for testing

        # Execute the command
        cmd = HBNBCommand()
        cmd.onecmd(user_input)
        sys.stdout = sys.__stdout__  # Restore normal output

        # Check output and storage content
        output = captured_output.getvalue().strip()
        self.assertEqual(len(output), 36)  # Length of a UUID
        self.assertIn(output, storage.all())
        instance = storage.all()[output]
        self.assertIsInstance(instance, User)
        self.assertEqual(instance.name, "John")
        self.assertEqual(instance.email, "john@example.com")

    def test_create_invalid_class(self):
        """Tests creating an instance of a non-existent class"""
        user_input = "create UnknownClass"
        captured_output = StringIO()
        sys.stdout = captured_output

        cmd = HBNBCommand()
        cmd.onecmd(user_input)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")
        self.assertEqual(len(storage.all()), 0)

    def test_show_valid(self):
        """Tests showing an existing instance"""
        # Create an instance first
        user = User(name="Jane", email="jane@example.com")
        user.save()
        user_id = user.id

        user_input = f"show User {user_id}"
        captured_output = StringIO()
        sys.stdout = captured_output

        cmd = HBNBCommand()
        cmd.onecmd(user_input)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertIn(str(user), output)

    def test_show_invalid_class(self):
        """Tests showing an instance of a non-existent class"""
        user_input = "show UnknownClass 12345"
        captured_output = StringIO()
        sys.stdout = captured_output

        cmd = HBNBCommand()
        cmd.onecmd(user_input)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_show_not_found(self):
        """Tests showing a non-existent instance"""
        user_input = "show User 12345"
        captured_output = StringIO()
        sys.stdout = captured_output

        cmd = HBNBCommand()
        cmd.onecmd(user_input)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertEqual(output, "** no instance found **")

    def test_update_valid(self):
        """Tests updating an existing instance"""
        # Create an instance first
        user = User(name="John", email="john@example.com")
        user.save()
        user_id = user.id

        user_input = f"update User {user_id} name=\"Jane\" email=\"jane@updated.com\""
        captured_output = StringIO()
        sys.stdout = captured_output

        cmd = HBNBCommand()
        cmd.onecmd(user_input)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertEqual(output, "")  # No output on successful update

        updated_user = storage.all()[user_id]
        self.assertEqual(updated_user.name, "Jane")
        self.assertEqual(updated_user.email, "Jane")
