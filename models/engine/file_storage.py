#!/usr/bin/python3
"""Defines FileStorage class."""
import json
import os


class FileStorage:
    """FileStorage class."""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return __objects dictionary, optionally filtered by class."""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if isinstance(cls, str):
                    if value.__class__.__name__ == cls:
                        new_dict[key] = value
                else:
                    if isinstance(value, cls):
                        new_dict[key] = value
            return new_dict
        return FileStorage.__objects

    def new(self, obj):
        """Set obj in __objects."""
        if obj:
            key = "{}.{}".format(
                obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to JSON file."""
        json_objects = {}
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()

        with open(FileStorage.__file_path,
                  "w", encoding="utf-8") as f:
            json.dump(json_objects, f)

    def delete(self, obj=None):
        """Delete obj from __objects if it's inside."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def reload(self):
        """Deserialize JSON file to __objects."""
        if not os.path.exists(FileStorage.__file_path):
            return

        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Place": Place,
            "Amenity": Amenity,
            "Review": Review
        }

        try:
            with open(FileStorage.__file_path,
                      "r", encoding="utf-8") as f:
                saved = json.load(f)
                for key, val in saved.items():
                    name = val["__class__"]
                    if name in classes:
                        obj = classes[name](**val)
                        FileStorage.__objects[key] = obj
        except Exception:
            pass

    def close(self):
        """Call reload() method for deserializing the JSON file to objects."""
        self.reload()
