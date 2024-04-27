#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    # New methods for storage_get_count branch

    def get(self, cls, id):
        """
        Retrieves an object based on the class and its ID.

        Args:
            cls (class): The class of the object to retrieve.
            id (string): The ID of the object to retrieve.

        Returns:
            The object based on the class and its ID, or None if not found.
        """

        if cls is None or type(id) != str:
            return None

        key = cls.__name__ + '.' + id
        return self.__objects.get(key)

    def count(self, cls=None):
        """
        Counts the number of objects in storage matching the given class.

        Args:
            cls (class, optional): The class of objects to count. Defaults to None,
                                    which counts all objects in storage.

        Returns:
            int: The number of objects in storage matching the given class.
        """

        if cls is None:
            return len(self.__objects)
        count = 0
        for key, obj in self.__objects.items():
            if isinstance(obj, cls):
                count += 1
        return count
