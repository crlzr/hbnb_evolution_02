#!/usr/bin/python
""" Place models """

from datetime import datetime
import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from data import storage, USE_DB_STORAGE, Base

# This is unfortunately the best possible way to have the many-to-many relationship work both ways.
# If the two classes are split into separate files, you'll have to import the other class
# to make things work, and this would cause a circular import error (chicken and egg problem).


if USE_DB_STORAGE:
    # define the many-to-many table
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
        Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True)
    )


class Place(Base):
    """Representation of place """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    # Class attrib defaults
    id = None
    created_at = None
    updated_at = None
    __city_id = ""
    __host_id = ""
    __name = ""
    __description = ""
    __address = ""
    __number_of_rooms = 0
    __number_of_bathrooms = 0
    __max_guests = 0
    __price_per_night = 0
    __latitude = 0
    __longitude = 0

    if USE_DB_STORAGE:
        __tablename__ = 'places'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __city_id = Column("city_id", String(60), ForeignKey('cities.id'), nullable=False)
        __host_id = Column("host_id", String(60), ForeignKey('users.id'), nullable=False)
        __name = Column("name", String(128), nullable=False)
        __description = Column("description", String(1024), nullable=True)
        __address = Column("address", String(1024), nullable=True)
        __number_of_rooms = Column("number_of_rooms", Integer, nullable=False, default=0)
        __number_of_bathrooms = Column("number_of_bathrooms", Integer, nullable=False, default=0)
        __max_guests = Column("max_guests", Integer, nullable=False, default=0)
        __price_per_night = Column("price_per_night", Integer, nullable=False, default=0)
        __latitude = Column("latitude", Float, nullable=True)
        __longitude = Column("longitude", Float, nullable=True)
        amenities = relationship("Amenity", secondary=place_amenity, back_populates = 'places')
        reviews = relationship("Review", back_populates="place", cascade="delete, delete-orphan")
        owner = relationship("User", back_populates="properties")

    # Constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that db records have a default of datetime.now()
        if not USE_DB_STORAGE:
            self.created_at = datetime.now().timestamp()
            self.updated_at = self.created_at

        # Only allow whatever is in can_init_list.
        # Note that setattr will call the setters for these attribs
        if kwargs:
            for key, value in kwargs.items():
                if key in ["city_id", "host_id", "name", "description", "number_rooms", "number_bathrooms", "max_guest", "price_by_night", "latitude", "longitude"]:
                    setattr(self, key, value)

    @property
    def city_id(self):
        """ Returns value of private property city_id """
        return self.__city_id

    @city_id.setter
    def city_id(self, value):
        """Setter for private prop city_id"""
        self.__city_id = value

    @property
    def host_id(self):
        """ Returns value of private property host_id """
        return self.__host_id

    @host_id.setter
    def host_id(self, value):
        """Setter for private prop host_id"""
        self.__host_id = value

    @property
    def name(self):
        """ Returns value of private property name """
        return self.__name

    @name.setter
    def name(self, value):
        """Setter for private prop name"""
        # Can't think of any special checks to perform here tbh
        self.__name = value

    @property
    def description(self):
        """ Returns value of private property description """
        return self.__description

    @description.setter
    def description(self, value):
        """Setter for private prop description"""
        # Can't think of any special checks to perform here tbh
        self.__description = value

    @property
    def address(self):
        """ Returns value of private property address """
        return self.__address

    @address.setter
    def address(self, value):
        """Setter for private prop address"""
        # Can't think of any special checks to perform here tbh
        self.__address = value

    @property
    def number_of_rooms(self):
        """ Returns value of private property number_of_rooms """
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        """Setter for private prop number_of_rooms"""
        if isinstance(value, int):
            self.__number_of_rooms = value
        else:
            raise ValueError("Invalid value specified for Number of Rooms: {}".format(value))

    @property
    def number_of_bathrooms(self):
        """ Returns value of private property number_of_bathrooms """
        return self.__number_of_bathrooms

    @number_of_bathrooms.setter
    def number_of_bathrooms(self, value):
        """Setter for private prop number_of_bathrooms"""
        if isinstance(value, int):
            self.__number_of_bathrooms = value
        else:
            raise ValueError("Invalid value specified for Number of Bathrooms: {}".format(value))

    @property
    def max_guests(self):
        """ Returns value of private property max_guests """
        return self.__max_guests

    @max_guests.setter
    def max_guests(self, value):
        """Setter for private prop max_guests"""
        if isinstance(value, int):
            self.__max_guests = value
        else:
            raise ValueError("Invalid value specified for Max Guests: {}".format(value))

    @property
    def price_per_night(self):
        """ Returns value of private property price_per_night """
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        """Setter for private prop price_per_night"""
        if isinstance(value, int):
            self.__price_per_night = value
        else:
            raise ValueError("Invalid value specified for Price per Night: {}".format(value))

    @property
    def latitude(self):
        """ Returns value of private property latitude """
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Setter for private prop latitude"""
        if isinstance(value, float):
            self.__latitude = value
        else:
            raise ValueError("Invalid value specified for Latitude: {}".format(value))

    @property
    def longitude(self):
        """ Returns value of private property longitude """
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for private prop longitude"""
        if isinstance(value, float):
            self.__longitude = value
        else:
            raise ValueError("Invalid value specified for Longitude: {}".format(value))

    # --- Static methods ---

    @staticmethod
    def all():
        """ Class method that returns all place data"""
        data = []

        try:
            place_data = storage.get('Place')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load places!"

        if USE_DB_STORAGE:
            # DBStorage
            for row in place_data:
                # use print(row.__dict__) to see the contents of the sqlalchemy model objects
                data.append({
                    "id": row.id,
                    "host_user_id": row.host_user_id,
                    "city_id": row.city_id,
                    "name": row.name,
                    "description": row.description,
                    "address": row.address,
                    "latitude": row.latitude,
                    "longitude": row.longitude,
                    "number_of_rooms": row.number_of_rooms,
                    "bathrooms": row.bathrooms,
                    "price_per_night": row.price_per_night,
                    "max_guests": row.max_guests,
                    "created_at": row.created_at.strftime(Place.datetime_format),
                    "updated_at": row.updated_at.strftime(Place.datetime_format)
                })
        else:
            # FileStorage
            for k, v in place_data.items():
                data.append({
                    "id": v['id'],
                    "host_user_id": v['host_user_id'],
                    "city_id": v['city_id'],
                    "name": v['name'],
                    "description": v['description'],
                    "address": v['address'],
                    "latitude": v['latitude'],
                    "longitude": v['longitude'],
                    "number_of_rooms": v['number_of_rooms'],
                    "bathrooms": v['bathrooms'],
                    "price_per_night": v['price_per_night'],
                    "max_guests": v['max_guests'],
                    "created_at": datetime.fromtimestamp(v['created_at']),
                    "updated_at": datetime.fromtimestamp(v['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def specific(place_id):
        """ Class method that returns a specific place's data"""
        data = []

        try:
            place_data = storage.get('Place', place_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Place not found!"

        if USE_DB_STORAGE:
            # DBStorage
            data.append({
                "id": place_data.id,
                "host_user_id": place_data.host_user_id,
                "city_id": place_data.city_id,
                "name": place_data.name,
                "description": place_data.description,
                "address": place_data.address,
                "latitude": place_data.latitude,
                "longitude": place_data.longitude,
                "number_of_rooms": place_data.number_of_rooms,
                "bathrooms": place_data.bathrooms,
                "price_per_night": place_data.price_per_night,
                "max_guests": place_data.max_guests,
                "created_at": place_data.created_at.strftime(Place.datetime_format),
                "updated_at": place_data.updated_at.strftime(Place.datetime_format)
            })
        else:
            # FileStorage
            data.append({
                "id": place_data['id'],
                "host_user_id": place_data['host_user_id'],
                "city_id": place_data['city_id'],
                "name": place_data['name'],
                "description": place_data['description'],
                "address": place_data['address'],
                "latitude": place_data['latitude'],
                "longitude": place_data['longitude'],
                "number_of_rooms": place_data['number_of_rooms'],
                "bathrooms": place_data['bathrooms'],
                "price_per_night": place_data['price_per_night'],
                "max_guests": place_data['max_guests'],
                "created_at": datetime.fromtimestamp(place_data['created_at']),
                "updated_at": datetime.fromtimestamp(place_data['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def create():
        """ Class method that creates a new Place"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        for key in ["host_user_id", "city_id", "name", "description", "address",
                "latitude", "longitude", "number_of_rooms", "bathrooms",
                "price_per_night", "max_guests"]:
            if key not in data:
                abort(400, "Missing {}".format(key))

        try:
            new_place = Place(
                host_user_id=data["host_user_id"],
                city_id=data["city_id"],
                name=data["name"],
                description=data["description"],
                address=data["address"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                number_of_rooms=data["number_of_rooms"],
                bathrooms=data["bathrooms"],
                price_per_night=data["price_per_night"],
                max_guests=data["max_guests"],
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        output = {
            "id": new_place.id,
            "host_user_id": new_place.host_user_id,
            "city_id": new_place.city_id,
            "name": new_place.name,
            "description": new_place.description,
            "address": new_place.address,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "number_of_rooms": new_place.number_of_rooms,
            "bathrooms": new_place.bathrooms,
            "price_per_night": new_place.price_per_night,
            "max_guests": new_place.max_guests,
            "created_at": new_place.created_at,
            "updated_at": new_place.updated_at
        }

        try:
            if USE_DB_STORAGE:
                # DBStorage - note that the add method uses the Place object instance 'new_place'
                storage.add('Place', new_place)
                # datetime -> readable text
                output['created_at'] = new_place.created_at.strftime(Place.datetime_format)
                output['updated_at'] = new_place.updated_at.strftime(Place.datetime_format)
            else:
                # FileStorage - note that the add method uses the dictionary 'output'
                storage.add('Place', output)
                # timestamp -> readable text
                output['created_at'] = datetime.fromtimestamp(new_place.created_at)
                output['updated_at'] = datetime.fromtimestamp(new_place.updated_at)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Place!"

        return jsonify(output)

    @staticmethod
    def update(place_id):
        """ Class method that updates an existing Place"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Place record. All attributes except id, created & updated are allowed to be modified
            result = storage.update('Place', place_id, data,
                                    ["name", "host_user_id", "city_id","description", "address",
                                     "latitude", "longitude", "number_of_rooms", "bathrooms",
                                     "price_per_night", "max_guests"])
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified place!"

        if USE_DB_STORAGE:
            output = {
                "id": result.id,
                "host_user_id": result.host_user_id,
                "city_id": result.city_id,
                "name": result.name,
                "description": result.description,
                "address": result.address,
                "latitude": result.latitude,
                "longitude": result.longitude,
                "number_of_rooms": result.number_of_rooms,
                "bathrooms": result.bathrooms,
                "price_per_night": result.price_per_night,
                "max_guests": result.max_guests,
                "created_at": result.created_at.strftime(Place.datetime_format),
                "updated_at": result.updated_at.strftime(Place.datetime_format)
            }
        else:
            output = {
                "id": result["id"],
                "host_user_id": result["host_user_id"],
                "city_id": result["city_id"],
                "name": result["name"],
                "description": result["description"],
                "address": result["address"],
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "number_of_rooms": result["number_of_rooms"],
                "bathrooms": result["bathrooms"],
                "price_per_night": result["price_per_night"],
                "max_guests": result["max_guests"],
                "created_at": datetime.fromtimestamp(result["created_at"]),
                "updated_at": datetime.fromtimestamp(result["updated_at"])
            }

        # print out the updated user details
        return jsonify(output)

    @staticmethod
    def delete(place_id):
        """ Class method that deletes an existing Place"""
        try:
            # delete the Place record
            storage.delete('Place', place_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified Place!"

        return Place.all()



class Amenity(Base):
    """Representation of amenity """

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    # Class attrib defaults
    id = None
    created_at = None
    updated_at = None
    __name = ""

    # Class attrib defaults
    if USE_DB_STORAGE:
        __tablename__ = 'amenities'
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.now())
        updated_at = Column(DateTime, nullable=False, default=datetime.now())
        __name = Column("name", String(128), nullable=False)
        places = relationship("Place", secondary=place_amenity, back_populates='amenities')

    # constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that setattr will call the setters for attribs in the list
        if kwargs:
            for key, value in kwargs.items():
                if key in ["name"]:
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
            raise ValueError("Invalid amenity name specified: {}".format(value))

    # --- Static methods ---
    @staticmethod
    def all():
        """ Class method that returns all amenity data"""
        data = []

        try:
            amenity_data = storage.get('Amenity')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load amenities!"

        if USE_DB_STORAGE:
            for row in amenity_data:
                data.append({
                    "id": row.id,
                    "name": row.name,
                    "created_at": row.created_at.strftime(Amenity.datetime_format),
                    "updated_at": row.updated_at.strftime(Amenity.datetime_format)
                })
        else:
            for k, v in amenity_data.items():
                data.append({
                    "id": v['id'],
                    "name": v['name'],
                    "created_at": datetime.fromtimestamp(v['created_at']),
                    "updated_at": datetime.fromtimestamp(v['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def specific(amenity_id):
        """ Class method that returns a specific amenities' data"""
        data = []

        try:
            amenity_data = storage.get('Amenity', amenity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Amenity data!"

        if USE_DB_STORAGE:
            data.append({
                "id": amenity_data.id,
                "name": amenity_data.name,
                "created_at": amenity_data.created_at.strftime(Amenity.datetime_format),
                "updated_at": amenity_data.updated_at.strftime(Amenity.datetime_format)
                })
        else:
            data.append({
                "id": amenity_data['id'],
                "name": amenity_data['name'],
                "created_at": datetime.fromtimestamp(amenity_data['created_at']),
                "updated_at": datetime.fromtimestamp(amenity_data['updated_at'])
                })

        return jsonify(data)

    @staticmethod
    def create():
        """ Class method that creates a new amenity"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        if 'name' not in data:
            abort(400, "Missing name")

        ###### TO DO ##### ONLY UNIQUE NAME FOR AMENITY

        try:
            new_amenity = Amenity(
                name=data["name"],
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            if USE_DB_STORAGE:
                # DBStorage - note that the add method uses the Amenity object instance
                storage.add('Amenity', new_amenity)
            else:
                # FileStorage - note that the add method uses the dictionary 'output'
                output = {
                    "id": new_amenity.id,
                    "name": new_amenity.name,
                    "created_at": new_amenity.created_at,
                    "updated_at": new_amenity.updated_at
                    }
                storage.add('Amenity', output)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Amenity!"

        try:
            return Amenity.specific(new_amenity.id)
        except IndexError:
            return "New Amenity not stored correctly"

    @staticmethod
    def update(amenity_id):
        """ Class method that updates an existing Amenity"""
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Amenity record. Only name can be changed
            result = storage.update('Amenity', amenity_id, data, ["name"])
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified Amenity!"

        if USE_DB_STORAGE:
            output = {
                "id": result.id,
                "name": result.name,
                "created_at": result.created_at.strftime(Amenity.datetime_format),
                "updated_at": result.updated_at.strftime(Amenity.datetime_format)
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
    def delete(amenity_id):
        """ Class method that deletes an existing Amenity"""
        try:
            # delete an Amenity
            storage.delete('Amenity', amenity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified Amenity!"

        return Amenity.all()