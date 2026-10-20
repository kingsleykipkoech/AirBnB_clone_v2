#!/usr/bin/python3
"""Defines BaseModel class."""
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class BaseModel:
    """BaseModel class."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    if isinstance(value, str):
                        value = datetime.fromisoformat(value)
                setattr(self, key, value)

    def __str__(self):
        """String representation."""
        dictionary = self.to_dict()
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, dictionary)

    def save(self):
        """Save instance and update timestamp."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Dictionary representation."""
        dictionary = dict(self.__dict__)
        dictionary["__class__"] = self.__class__.__name__
        if "created_at" in dictionary and isinstance(dictionary["created_at"], datetime):
            dictionary["created_at"] = dictionary["created_at"].isoformat()
        if "updated_at" in dictionary and isinstance(dictionary["updated_at"], datetime):
            dictionary["updated_at"] = dictionary["updated_at"].isoformat()
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """Delete the current instance from the storage."""
        models.storage.delete(self)
