#!/usr/bin/python
""" Review model """

from datetime import datetime
import uuid
import re
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from data import storage, USE_DB_STORAGE, Base
from flask import jsonify, request, abort

class Review(Base):
    """Representation of Review """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    # Class attrib defaults
    id = None
    __commentor_user_id = ""
    __place_id = ""
    __feedback = ""
    __rating = 0
    created_at = None
    updated_at = None



    if USE_DB_STORAGE:
        __tablename__ = 'review'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __feedback = Column("feedback", String(128), nullable=False)
        __rating = Column("rating", Integer, nullable=False, default=0)
        __commentor_user_id = Column("commentor_user_id", String(128), ForeignKey("users.id"), nullable=False)
        __place_id = Column("place_id", String(128), ForeignKey('places.id'), nullable=False)
        #country = relationship("Country", back_populates="cities")

    # constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that db records have a default of datetime.now()
        if not USE_DB_STORAGE:
            self.created_at = datetime.now().timestamp()
            self.updated_at = self.created_at

        # Only allow feedback, rating, commentor_user_id, place_id
        # Note that setattr will call the setters for these attribs
        if kwargs:
            for key, value in kwargs.items():
                if key in ["feedback", "rating", "commentor_user_id", "place_id"]:
                    setattr(self, key, value)

    @property
    def feedback(self):
        """Getter for private prop feedback"""
        return self.__feedback

    @feedback.setter
    def feedback(self, value):
        """Setter for private prop feedback"""

        # ensure that the value is not spaces-only and is alphabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value)
        if is_valid_name:
            self.__feedback = value
        else:
            raise ValueError("Invalid feedback specified: {}".format(value))

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
    def commentor_user_id(self):
        """Getter for private prop commentor_user_id"""
        return self.__commentor_user_id

    @commentor_user_id.setter
    def commentor_user_id(self, value):
        """Setter for private prop commentor_user_id"""
        # ensure that the specified commentor user id actually exists before setting
        if storage.get('User', value) is not None:
            self.__commentor_user_id = value
        else:
            raise ValueError("Invalid commentor_user_id specified: {}".format(value))

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
                    "commentor_user_id": row.commentor_user_id,
                    "place_id": row.place_id,
                    "feedback": row.feedback,
                    "rating": row.rating,
                    "created_at": row.created_at.strftime(Review.datetime_format),
                    "updated_at": row.updated_at.strftime(Review.datetime_format)
                })
        else:
            # FileStorage
            for k, v in review_data.items():
                data.append({
                    "id": v['id'],
                    "commentor_user_id": v['commentor_user_id'],
                    "place_id": v['place_id'],
                    "feedback": v['feedback'],
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
                "commentor_user_id": review_data.commentor_user_id,
                "place_id": review_data.place_id,
                "feedback": review_data.feedback,
                "rating": review_data.rating,
                "created_at": review_data.created_at.strftime(Review.datetime_format),
                "updated_at": review_data.updated_at.strftime(Review.datetime_format)
                })
        else:
            # FileStorage
            data.append({
                    "id": review_data['id'],
                    "commentor_user_id": review_data['commentor_user_id'],
                    "place_id": review_data['place_id'],
                    "feedback": review_data['feedback'],
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

        for key in ["commentor_user_id", "place_id", "feedback", "rating"]:
            if key not in data:
                abort(400, "Missing {}".format(key))

        try:
            new_review = Review(
                commentor_user_id=data['commentor_user_id'],
                place_id=data['place_id'],
                feedback=data['feedback'],
                rating=data['rating']
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        output = {
            "id": new_review.id,
            "commentor_user_id": new_review.commentor_user_id,
            "place_id": new_review.place_id,
            "feedback": new_review.feedback,
            "rating": new_review.rating,
            "created_at": new_review.created_at,
            "updated_at": new_review.updated_at
        }

        try:
            if USE_DB_STORAGE:
                # DBStorage - note that the add method uses the Review object instance 'new_review'
                storage.add('Review', new_review)
                # datetime -> readable text
                output['created_at'] = new_review.created_at.strftime(Review.datetime_format)
                output['updated_at'] = new_review.updated_at.strftime(Review.datetime_format)
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
            result = storage.update('City', review_id, data, ["commentor_user_id", "place_id", "feedback", "rating"])
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified Review!"

        if USE_DB_STORAGE:
            output = {
                "id": result.id,
                "commentor_user_id": result.commentor_user_id,
                "place_id": result.place_id,
                "feedback": result.feedback,
                "rating": result.rating,
                "created_at": result.created_at.strftime(Review.datetime_format),
                "updated_at": result.updated_at.strftime(Review.datetime_format)
            }
        else:
            output = {
                "id": result['id'],
                "commentor_user_id": result['commentor_user_id'],
                "place_id": result['place_id'],
                "feedback": result['feedback'],
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
