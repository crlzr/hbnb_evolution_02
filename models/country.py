#!/usr/bin/python
""" Country model """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from data import storage, USE_DB_STORAGE, Base
from models.city import City

class Country(Base):
    """Representation of country """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    # Class attrib defaults
    id = None
    created_at = None
    updated_at = None
    __name = ""
    __code = ""

    if USE_DB_STORAGE:
        __tablename__ = 'countries'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __name = Column("name", String(128), nullable=False)
        __code = Column("code", String(2), nullable=False)
        #cities = relationship("City", back_populates="country", cascade="delete, delete-orphan")

    # Constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that db records have a default of datetime.now()
        if not USE_DB_STORAGE:
            self.created_at = datetime.now().timestamp()
            self.updated_at = self.created_at

        # Only allow name, code.
        # Note that setattr will call the setters for these attribs
        if kwargs:
            for key, value in kwargs.items():
                if key in ["name", "code"]:
                    setattr(self, key, value)

    # --- Getters and Setters ---
    @property
    def name(self):
        """Getter for private prop name"""
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for private prop name"""

        # ensure that the value is not spaces-only and is alphabets + spaces only
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z ]+$", value)
        if is_valid_name:
            self.__name = value
        else:
            raise ValueError("Invalid country name specified: {}".format(value))

    @property
    def code(self):
        """Getter for private prop code"""
        return self.__code

    @code.setter
    def code(self, value):
        """Setter for private prop code"""

        # ensure that the value is not spaces-only and is two uppercase alphabets only
        is_valid_code = len(value.strip()) > 0 and re.search("^[A-Z][A-Z]$", value)
        if is_valid_code:
            self.__code = value
        else:
            raise ValueError("Invalid country code specified: {}".format(value))

    # --- Static methods ---
    @staticmethod
    def all():
        """ Class method that returns all countries data"""
        data = []

        try:
            country_data = storage.get('Country')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load countries!"

        if USE_DB_STORAGE:
            for row in country_data:
                data.append({
                    "id": row.id,
                    "name": row.name,
                    "code": row.code,
                    "created_at": row.created_at.strftime(Country.datetime_format),
                    "updated_at": row.updated_at.strftime(Country.datetime_format)
                })
        else:
            for k, v in country_data.items():
                data.append({
                    "id": v['id'],
                    "name": v['name'],
                    "code": v['code'],
                    "created_at": datetime.fromtimestamp(v['created_at']),
                    "updated_at": datetime.fromtimestamp(v['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def specific(country_id):
        """ Class method that returns a specific country's data"""
        data = []

        try:
            country_data = storage.get('Country', country_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Country not found!"

        if USE_DB_STORAGE:
            # DBStorage
            data.append({
                "id": country_data.id,
                "name": country_data.name,
                "code": country_data.code,
                "created_at": country_data.created_at.strftime(Country.datetime_format),
                "updated_at": country_data.updated_at.strftime(Country.datetime_format)
                })
        else:
            # FileStorage
            data.append({
                "id": country_data['id'],
                "name": country_data['name'],
                "code": country_data['code'],
                "created_at": datetime.fromtimestamp(country_data['created_at']),
                "updated_at": datetime.fromtimestamp(country_data['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def create():
        """ Class method that creates a new country"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        try:
            country_data = storage.get('Country')
        except IndexError as exc:
            print("Error: ", exc)
            return "Country not found!"
        
        data = request.get_json()
        if 'name' not in data:
            abort(400, "Missing name")
        if 'code' not in data:
            abort(400, "Missing country code")
        for country in country_data:
            if USE_DB_STORAGE:
                if data['code'] == country.code:
                    abort(400, "Code must be unique")
                if data['name'] == country.name:
                    abort(400, "Name must be unique")
            else:
                if data['code'] == country_data[country]['code']:
                    abort(400, "Code must be unique")
                if data['name'] == country_data[country]['name']:
                    abort(400, "Name must be unique")


        try:
            new_country = Country(
                name=data["name"],
                code=data["code"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        output = {
            "id": new_country.id,
            "name": new_country.name,
            "code": new_country.code,
            "created_at": new_country.created_at,
            "updated_at": new_country.updated_at
        }

        # TODO: add a check for the country code to ensure that we don't have 2
        # countries with the same code

        try:
            if USE_DB_STORAGE:
                # DBStorage - note that the add method uses the Country object instance
                storage.add('Country', new_country)
                output['created_at'] = new_country.created_at.strftime(Country.datetime_format)
                output['updated_at'] = new_country.updated_at.strftime(Country.datetime_format)
            else:
                # FileStorage - note that the add method uses the dictionary 'output'
                storage.add('Country', output)
                output['created_at'] = datetime.fromtimestamp(Country.created_at)
                output['updated_at'] = datetime.fromtimestamp(Country.updated_at)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Country!"

        return jsonify(output)

    @staticmethod
    def update(country_id):
        """ Class method that updates an existing country"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Country record. Only name and code can be changed
            result = storage.update('Country', country_id, data, ["name", "code"])
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified country!"

        if USE_DB_STORAGE:
            output = {
                "id": result.id,
                "name": result.name,
                "created_at": result.created_at.strftime(Country.datetime_format),
                "updated_at": result.updated_at.strftime(Country.datetime_format)
            }
        else:
            output = {
                "id": result['id'],
                "name": result['name'],
                "created_at": datetime.fromtimestamp(result['created_at']),
                "updated_at": datetime.fromtimestamp(result['updated_at'])
            }

        return jsonify(output)

    @staticmethod
    def cities_data(country_id):
        """ Class method that returns a specific country's cities"""
        data = []

        if USE_DB_STORAGE:
            country_data = storage.get('Country', country_id)
            city_data = country_data.cities

            for v in city_data:
                data.append({
                    "id": v.id,
                    "name": v.name,
                    "country_id": v.country_id,
                    "created_at":v.created_at.strftime(Country.datetime_format),
                    "updated_at":v.updated_at.strftime(Country.datetime_format)
                })
        else:
            city_data = storage.get("City")

            for k, v in city_data.items():
                if v['country_id'] == country_id:
                    data.append({
                        "id": v['id'],
                        "name": v['name'],
                        "country_id": v['country_id'],
                        "created_at":datetime.fromtimestamp(v['created_at']),
                        "updated_at":datetime.fromtimestamp(v['updated_at'])
                    })

        return data

    @staticmethod
    def delete(country_id):
        """ Class method that deletes an existing Country"""
        try:
            # delete the Country record
            storage.delete('Country', country_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified country!"

        return Country.all()
