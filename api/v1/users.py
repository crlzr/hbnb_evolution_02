#!/usr/bin/python3
""" objects that handles all default RestFul API actions for User"""
from api.v1 import api_routes
from models.user import User
from data.file_export import export_to_file
from flask import jsonify

@api_routes.route('/users', methods=["GET"])
def users_get():
    """returns Users"""
    # use the User class' static .all method
    return jsonify(User.all())

@api_routes.route('/users/<user_id>', methods=["GET"])
def users_specific_get(user_id):
    """returns specified user"""
    # use the User class' static .specific method
    return User.specific(user_id)

@api_routes.route('/users', methods=["POST"])
def users_post():
    """ posts data for new user then returns the user data"""
    # -- Usage example --
    # curl -X POST localhost:5000/api/v1/users /
    #   -H "Content-Type: application/json" /
    #   -d '{"first_name":"Peter","last_name":"Parker","email":"p.parker@daily-bugle.net","password":"123456"}'

    # use the User class' static .create method
    return User.create()

@api_routes.route('/users/<user_id>', methods=["PUT"])
def users_put(user_id):
    """ updates existing user data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # use the User class' static .update method
    # can only update first_name and last_name
    return User.update(user_id)

@api_routes.route('/users/<user_id>/reviews', methods=["GET"])
def users_all_reviews(user_id):
    """returns specified user"""
    return User.reviews_data(user_id)

@api_routes.route('users/export', methods=["GET"])
def users_all_export():
    """ exports to file """
    data_to_print = User.all()
    return export_to_file(data_to_print)


@api_routes.route('/users/<user_id>', methods=["DELETE"])
def user_delete(user_id):
    """ deletes existing user data using specified id """
    return jsonify(User.delete(user_id))
