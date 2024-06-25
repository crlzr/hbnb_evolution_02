#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb evolution"""

import json
from pathlib import Path

class FileStorage():
    """ Class for reading data from JSON files """
    __data = {}
    __classes = ["Amenity", "City", "Country", "Place", "Review", "User"]

    # No constructor in this class - doesn't seem like we really need one anyway

    def load_data(self, is_testing = False):
        """ Load JSON data from file and stores it all in __data """

        models_filepath = "data/models_testing.json" if is_testing else "data/models.json"
        relations_filepath = "data/relations_testing.json" if is_testing else "data/relations.json"

        self.__data['models'] = self.__load_models_data(models_filepath)
        self.__data['relations'] = self.__load_many_to_many_relations_data(relations_filepath)

    def get(self, class_name = "", record_id = ""):
        """ Return all data or data for specified class name and / or id"""

        if class_name == "":
            raise IndexError("Unable to load Model data. No class name specified")

        if class_name not in self.__classes:
            raise IndexError("Unable to load Model data. Specified class name not found")

        if record_id == "":
            return self.__data['models'][class_name]
        else:
            if record_id not in self.__data['models'][class_name]:
                raise IndexError("Unable to load Model data. Specified id not found")

            return self.__data['models'][class_name][record_id]

    def add(self, class_name, new_record):
        """ Adds another entry to specified class """

        if class_name.strip() == "" or class_name not in self.__classes:
            raise IndexError("Specified class name is not valid")

        # create if it doesn't exist
        if class_name not in self.__data['models']:
            self.__data['models'][class_name] = {}

        if new_record['id'] in self.__data['models'][class_name]:
            raise IndexError("An item with the same id already exists")

        # add to existing data and return
        self.__data['models'][class_name][new_record['id']] = new_record

    def update(self, class_name, record_id, update_data, allowed = None):
        """ Updates existing entry of specified class """

        # 1. find the record using the record_id
        # 2. update the record according to what is specified in the 'allowed' list
        # 3. 'save' the record back into memory and return it

        if class_name in self.__classes:
            if class_name not in self.__data['models'] or record_id not in self.__data['models'][class_name]:
                raise IndexError("Unable to find the record to update")

        record = self.get(class_name, record_id)

        # update the record values
        for k, v in update_data.items():
            if allowed is not None and len(allowed) > 0:
                if k in allowed:
                    record[k] = v
            else:
                record[k] = v

        self.__data['models'][class_name][record_id] = record

        return record

    def delete(self, class_name, record_id):
        """ Method to delete items"""
        if class_name in self.__classes:
            if class_name not in self.__data['models'] or record_id not in self.__data['models'][class_name]:
                raise IndexError("Unable to find the record to delete in file_storage.py")

        try:
            data_to_del = self.get(class_name)
            data_to_del.pop(record_id, None)
        except:
            raise IndexError("Unable to delete the record.")

    def __load_models_data(self, filepath):
        """ Load JSON data from models file and returns as dictionary """
        temp = {}
        models_data = {}

        if not Path(filepath).is_file():
            raise FileNotFoundError("Data file '{}' missing".format(filepath))

        try:
            with open(filepath, 'r') as f:
                rows = json.load(f)
            for key in rows:
                temp[key] = rows[key]
        except ValueError as exc:
            raise ValueError("Unable to load data from file '{}'".format(filepath)) from exc

        # The data at this point is not directly usable. It needs to be reorganised
        for key, value in temp.items():
            models_data[key] = {}
            for row in value:
                models_data[key][row['id']] = row

        # print(json.dumps(model_data))
        return models_data

    def __load_many_to_many_relations_data(self, filepath):
        """ Load JSON data from relations file and returns as dictionary """

        temp = {}
        relations_data = {}

        if not Path(filepath).is_file():
            raise FileNotFoundError("Data file '{}' missing".format(filepath))

        try:
            with open(filepath, 'r') as f:
                rows = json.load(f)
            for key in rows:
                temp[key] = rows[key]
        except ValueError as exc:
            raise ValueError("Unable to load data from file '{}'".format(filepath)) from exc

        # reorganise relations data
        for key, value in temp.items():
            # the key will be in the format like <something>_to_<something>
            keys = key.split('_to_')
            if keys[0] not in relations_data:
                relations_data[keys[0]] = {}

            if keys[1] not in relations_data[keys[0]]:
                relations_data[keys[0]][keys[1]] = {}

            for row in value:
                if row['place_id'] not in relations_data[keys[0]][keys[1]]:
                    relations_data[keys[0]][keys[1]][row['place_id']] = []

                relations_data[keys[0]][keys[1]][row['place_id']].append(row['amenity_id'])

        # print(json.dumps(relations_data))
        return relations_data
