#!/usr/bin/python3
""" objects that handles all default RestFul API actions for User"""
from api.v1 import api_routes
from models.user import User


@api_routes.route('/users', methods=["GET"])
def users_get():
    """returns Users"""
    # use the User class' static .all method
    return User.all()

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

@api_routes.route('/users/<user_id>', methods=["DELETE"])
def user_delete(user_id):
    """ deletes existing user data using specified id """
    return User.delete(user_id)