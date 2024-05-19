#!/usr/bin/python3

"""Unitest for console.py"""

import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestHBNBCommand(unittest.TestCase):
    """Tests for the HBNBCommand console."""

    def setUp(self):
        """Reset the storage before each test."""
        storage._FileStorage__objects = {}

    def test_help(self):
        """Test the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertIn("Documented commands", f.getvalue())

    def test_quit(self):
        """Test the quit command."""
        with patch('sys.stdout', new=StringIO()) as f:
            result = HBNBCommand().onecmd("quit")
            self.assertTrue(result)

    def test_create(self):
        """Test the create command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            self.assertIn("uuid", f.getvalue())

    def test_show(self):
        """Test the show command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(f"show BaseModel {obj_id}")
            self.assertIn("BaseModel", f.getvalue())

    def test_destroy(self):
        """Test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(f"destroy BaseModel {obj_id}")
            HBNBCommand().onecmd(f"show BaseModel {obj_id}")
            self.assertIn("no instance found", f.getvalue())

    def test_all(self):
        """Test the all command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("all")
            self.assertIn("BaseModel", f.getvalue())
            self.assertIn("User", f.getvalue())

    def test_update(self):
        """Test the update command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(f'update BaseModel {obj_id} name "MyName"')
            HBNBCommand().onecmd(f"show BaseModel {obj_id}")
            self.assertIn("MyName", f.getvalue())

    def test_update_with_dict(self):
        """Test the update command with dictionary representation."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(
                f'update BaseModel {obj_id} {{"name": "MyName", "age": 30}}'
            )
            HBNBCommand().onecmd(f"show BaseModel {obj_id}")
            self.assertIn("MyName", f.getvalue())
            self.assertIn("30", f.getvalue())

    def test_class_all(self):
        """Test <class name>.all() command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("BaseModel.all()")
            self.assertIn("BaseModel", f.getvalue())

    def test_class_count(self):
        """Test <class name>.count() command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("BaseModel.count()")
            self.assertIn("1", f.getvalue())

    def test_class_show(self):
        """Test <class name>.show(<id>) command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(f"BaseModel.show({obj_id})")
            self.assertIn(obj_id, f.getvalue())

    def test_class_destroy(self):
        """Test <class name>.destroy(<id>) command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(f"BaseModel.destroy({obj_id})")
            HBNBCommand().onecmd(f"BaseModel.show({obj_id})")
            self.assertIn("no instance found", f.getvalue())

    def test_class_update(self):
        """
        Test <class name>.update(<id>, <attribute name>,
        <attribute value>) command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(
                f'BaseModel.update({obj_id}, "name", "MyName")'
            )
            HBNBCommand().onecmd(f"BaseModel.show({obj_id})")
            self.assertIn("MyName", f.getvalue())

    def test_class_update_with_dict(self):
        """
        Test <class name>.update(<id>, <dictionary representation>)
        command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            HBNBCommand().onecmd(
                f'BaseModel.update({obj_id}, {{"name": "MyName", "age": 30}})'
            )
            HBNBCommand().onecmd(f"BaseModel.show({obj_id})")
            self.assertIn("MyName", f.getvalue())
            self.assertIn("30", f.getvalue())


if __name__ == '__main__':
    unittest.main()
