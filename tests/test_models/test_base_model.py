#!/usr/bin/python3

"""Basemodel unittest"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
from unittest.mock import patch
import uuid


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        """Set up a fresh BaseModel instance for each test."""
        self.model = BaseModel()

    def test_initialization_no_args(self):
        """Test initialization without arguments."""
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertEqual(self.model.created_at, self.model.updated_at)

    def test_initialization_with_kwargs(self):
        """Test initialization with keyword arguments."""
        data = {
            "id": "1234",
            "created_at": "2023-01-01T12:00:00",
            "updated_at": "2023-01-02T12:00:00",
            "name": "Test Model"
        }
        model = BaseModel(**data)

        self.assertEqual(model.id, "1234")
        self.assertEqual(model.created_at, datetime(2023, 1, 1, 12))
        self.assertEqual(model.updated_at, datetime(2023, 1, 2, 12))
        self.assertEqual(model.name, "Test Model")

    def test_str_representation(self):
        """Test string representation of the instance."""
        expected_str = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), expected_str)

    @patch("models.storage.save")
    def test_save_method(self, mock_storage_save):
        """Test the save method and updated_at attribute."""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)
        mock_storage_save.assert_called_once()

    def test_to_dict(self):
        """Test the to_dict method."""
        obj_dict = self.model.to_dict()
        self.assertEqual(obj_dict['__class__'], 'BaseModel')
        self.assertEqual(
            obj_dict['created_at'], self.model.created_at.isoformat()
            )
        self.assertEqual(
            obj_dict['updated_at'], self.model.updated_at.isoformat()
        )
        self.assertEqual(obj_dict['id'], self.model.id)


if __name__ == '__main__':
    unittest.main()
