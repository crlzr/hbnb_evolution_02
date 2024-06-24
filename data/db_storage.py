#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb evolution"""

import importlib
from os import getenv
from copy import deepcopy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class DBStorage():
    """ Class for reading data from databases """
    __engine = None
    __session = None
    __module_names = {
        "User": "user",
        "Country": "country",
        "City": "city",
        "Amenity": "place_amenity",
        "Place": "place_amenity",
        "Review": "review"
    }

    def __init__(self, Base):
        """Instantiate a DBStorage object"""

        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        is_testing = getenv('TESTING')

        # If you were lazy and didn't specify anything on the command line, then the defaults below will be used
        # PLEASE DON'T DO THIS IN A REAL WORKING ENVIRONMENT
        if user is None:
            user = "hbnb_evo"
        if pwd is None:
            pwd = "hbnb_evo_pwd"
        if host is None:
            if getenv('IS_DOCKER_CONTAINER'):
                # make sure this is the same as the db container name in the docker compose file
                host = "hbnb_evo_2_db"
            else:
                host = "localhost"
        if db is None:
            if is_testing == "1":
                db = "hbnb_test_db"
            else:
                db = "hbnb_evo_db"

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db))

        if is_testing == "1":
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get(self, class_name = "", record_id = ""):
        """ Return data for specified class name with or without record id"""

        if class_name == "":
            raise IndexError("Unable to load Model data. No class name specified")

        if not self.__module_names[class_name]:
            raise IndexError("Unable to load Model data. Specified class name not found")

        namespace = self.__module_names[class_name]
        module = importlib.import_module("models." + namespace)
        class_ = getattr(module, class_name)

        if record_id == "":
            rows = self.__session.query(class_).all()
        else:
            try:
                rows = self.__session.query(class_).where(class_.id == record_id).limit(1).one()
            except:
                raise IndexError("Unable to load Model data. Specified id not found")

        return rows

    def add(self, class_name, new_record):
        """ Adds another record to specified class """

        if class_name.strip() == "" or not self.__module_names[class_name]:
            raise IndexError("Specified class name is not valid")

        # Assume that the database table already exists so we're not doing CREATE TABLE here

        self.__session.add(new_record)
        self.__session.commit()
        self.__session.refresh(new_record)

    def update(self, class_name, record_id, update_data, allowed = None):
        """ Updates existing record of specified class """

        # 1. find the record using the record_id
        # 2. update the record according to what is specified in the 'allowed' list
        # 3. 'save' the record back into the db and return it

        if class_name.strip() == "" or not self.__module_names[class_name]:
            raise IndexError("Specified class name is not valid")

        # Assume that the database table already exists so we're not doing CREATE TABLE here

        namespace = self.__module_names[class_name]
        module = importlib.import_module("models." + namespace)
        class_ = getattr(module, class_name)

        try:
            record = self.__session.query(class_).where(class_.id == record_id).limit(1).one()
        except:
            raise IndexError("Unable to find the record to update")

        # update the record values

        try:
            for k, v in update_data.items():
                if allowed is not None and len(allowed) > 0:
                    if k in allowed:
                        setattr(record, k, v)
                else:
                    setattr(record, k, v)

            # Don't forget to update the updated_at value! You just updated the record you know...
            record.updated_at = datetime.now()

            self.__session.commit()
        except:
            raise IndexError("Unable to update record")

        # For safety, don't return the original record. Return a copy instead
        return deepcopy(record)

    def delete(self, class_name, record_id):
        """ Method to delete items"""
        #record = self.get(class_name, record_id)
        raise IndexError("Unable to find the record to delete in db_storage.py")