#!/usr/bin/python3
"""Defines unittests for file storage"""

import unittest
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
import os


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        """Set up a FileStorage instance and a temporary file path."""
        self.storage = FileStorage()
        self.temp_file_path = "temp_file.json"
        self.storage._FileStorage__file_path = self.temp_file_path

    def tearDown(self):
        """Clean up the temporary file."""
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)

    def test_all(self):
        """Test the all() method."""
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)

    def test_new(self):
        """Test the new() method."""
        obj = BaseModel()
        self.storage.new(obj)
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test the save() method."""
        obj = User()
        self.storage.new(obj)
        self.storage.save()

        self.assertTrue(os.path.exists(self.temp_file_path))

        with open(self.temp_file_path, 'r') as f:
            content = json.load(f)

        self.assertIn(f"User.{obj.id}", content)

    def test_reload(self):
        """Test the reload() method."""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertIn(f"BaseModel.{obj.id}", self.storage.all())


if __name__ == '__main__':
    unittest.main()
