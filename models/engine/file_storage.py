#!/usr/bin/python3
"""
Defines a `FileStorage` class.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        with open(self.__file_path, 'w') as f:
            obj_dict = {
                key: obj.to_dict()
                for key, obj in self.__objects.items()
            }
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    cls_name = value["__class__"]
                    cls = globals()[cls_name]
                    self.__objects[key] = cls(**value)
        except FileNotFoundError:
            pass


globals()["BaseModel"] = BaseModel
globals()["User"] = User
globals()["State"] = State
globals()["City"] = City
globals()["Amenity"] = Amenity
globals()["Place"] = Place
globals()["Review"] = Review
