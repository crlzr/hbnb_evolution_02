#!/usr/bin/python
""" Review model """

from datetime import datetime
import uuid
import re
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from data import storage, USE_DB_STORAGE, Base
from flask import jsonify, request, abort
from models import datetime_format

class Review(Base):
    """Representation of Review """

    # Class attrib defaults
    id = None
    __user_id = ""
    __place_id = ""
    __comment = ""
    __rating = 0
    created_at = None
    updated_at = None



    if USE_DB_STORAGE:
        __tablename__ = 'reviews'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __comment = Column("comment", String(128), nullable=False)
        __rating = Column("rating", Integer, nullable=False, default=0)
        __user_id = Column("user_id", String(128), ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
        __place_id = Column("place_id", String(128), ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
        place = relationship("Place", back_populates="reviews", foreign_keys=[__place_id])
        writer = relationship("User", back_populates="reviews", foreign_keys=[__user_id])

    # constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that db records have a default of datetime.now()
        if not USE_DB_STORAGE:
            self.created_at = datetime.now().timestamp()
            self.updated_at = self.created_at

        # Only allow comment, rating, user_id, place_id
        # Note that setattr will call the setters for these attribs
        if kwargs:
            for key, value in kwargs.items():
                if key in ["comment", "rating", "user_id", "place_id"]:
                    setattr(self, key, value)

    @property
    def comment(self):
        """Getter for private prop comment"""
        return self.__comment

    @comment.setter
    def comment(self, value):
        """Setter for private prop comment"""

        # ensure that the value is not spaces-only and is alphabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z0-9.,- ]+$", value)
        if is_valid_name:
            self.__comment = value
        else:
            raise ValueError("Invalid comment specified: {}".format(value))

    @property
    def rating(self):
        """Getter for private prop rating"""
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Setter for private prop rating"""
        if not isinstance(value, int):
            raise TypeError("Rating must be an int between 1.0 and 5.0: {}".format(value))
        if value < 1 or value > 5:
            raise ValueError("Rating must be an int between 1.0 and 5.0: {}".format(value))

        self.__rating = value

    @property
    def user_id(self):
        """Getter for private prop user_id"""
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        """Setter for private prop user_id"""
        # ensure that the specified user id actually exists before setting
        if storage.get('User', value) is not None:
            self.__user_id = value
        else:
            raise ValueError("Invalid user id specified: {}".format(value))

    @property
    def place_id(self):
        """Getter for private prop place_id"""
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        """Setter for private prop place_id"""
        # ensure that the specified place id actually exists before setting
        if storage.get('Place', value) is not None:
            self.__place_id= value
        else:
            raise ValueError("Invalid place_id specified: {}".format(value))

    # --- Static methods ---

    @staticmethod
    def all():
        """ Class method that returns all Review data"""
        data = []

        try:
            review_data = storage.get('Review')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load reviews!"

        if USE_DB_STORAGE:
            # DBStorage
            for row in review_data:
                # use print(row.__dict__) to see the contents of the sqlalchemy model objects
                data.append({
                    "id": row.id,
                    "user_id": row.user_id,
                    "place_id": row.place_id,
                    "comment": row.comment,
                    "rating": row.rating,
                    "created_at": row.created_at.strftime(datetime_format),
                    "updated_at": row.updated_at.strftime(datetime_format)
                })
        else:
            # FileStorage
            for k, v in review_data.items():
                data.append({
                    "id": v['id'],
                    "user_id": v['user_id'],
                    "place_id": v['place_id'],
                    "comment": v['comment'],
                    "rating": v['rating'],
                    "created_at": datetime.fromtimestamp(v['created_at']),
                    "updated_at": datetime.fromtimestamp(v['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def specific(review_id):
        """ Class method that returns all Review data"""
        data = []

        try:
            review_data = storage.get('Review', review_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load reviews!"

        if USE_DB_STORAGE:
            # DBStorage
            data.append({
                "id": review_data.id,
                "user_id": review_data.user_id,
                "place_id": review_data.place_id,
                "comment": review_data.comment,
                "rating": review_data.rating,
                "created_at": review_data.created_at.strftime(datetime_format),
                "updated_at": review_data.updated_at.strftime(datetime_format)
                })
        else:
            # FileStorage
            data.append({
                    "id": review_data['id'],
                    "user_id": review_data['user_id'],
                    "place_id": review_data['place_id'],
                    "comment": review_data['comment'],
                    "rating": review_data['rating'],
                    "created_at": datetime.fromtimestamp(review_data['created_at']),
                    "updated_at": datetime.fromtimestamp(review_data['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def create():
        """ Class method that creates a new review"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        for key in ["user_id", "place_id", "comment", "rating"]:
            if key not in data:
                abort(400, "Missing {}".format(key))

        try:
            new_review = Review(
                user_id=data['user_id'],
                place_id=data['place_id'],
                comment=data['comment'],
                rating=data['rating']
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        output = {
            "id": new_review.id,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id,
            "comment": new_review.comment,
            "rating": new_review.rating,
            "created_at": new_review.created_at,
            "updated_at": new_review.updated_at
        }

        try:
            if USE_DB_STORAGE:
                # DBStorage - note that the add method uses the Review object instance 'new_review'
                storage.add('Review', new_review)
                # datetime -> readable text
                output['created_at'] = new_review.created_at.strftime(datetime_format)
                output['updated_at'] = new_review.updated_at.strftime(datetime_format)
            else:
                # FileStorage - note that the add method uses the dictionary 'output'
                storage.add('Review', output)
                # timestamp -> readable text
                output['created_at'] = datetime.fromtimestamp(new_review.created_at)
                output['updated_at'] = datetime.fromtimestamp(new_review.updated_at)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Review!"

        return jsonify(output)

    @staticmethod
    def update(review_id):
        """ Class method that updates an existing Review"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Review record. Only name and country_id are allowed to be modified
            result = storage.update('Review', review_id, data, ["user_id", "place_id", "comment", "rating"])
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified Review!"

        if USE_DB_STORAGE:
            output = {
                "id": result.id,
                "user_id": result.user_id,
                "place_id": result.place_id,
                "comment": result.comment,
                "rating": result.rating,
                "created_at": result.created_at.strftime(datetime_format),
                "updated_at": result.updated_at.strftime(datetime_format)
            }
        else:
            output = {
                "id": result['id'],
                "user_id": result['user_id'],
                "place_id": result['place_id'],
                "comment": result['comment'],
                "rating": result['rating'],
                "created_at": datetime.fromtimestamp(result['created_at']),
                "updated_at": datetime.fromtimestamp(result['updated_at'])
            }

        # print out the updated user details
        return jsonify(output)

    @staticmethod
    def delete(review_id):
        """ Class method that deletes an existing Review"""
        try:
            # delete the Review record
            storage.delete('Review', review_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified review!"

        return Review.all()
