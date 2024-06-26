#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Review"""
from api.v1 import api_routes
from models.review import Review


@api_routes.route('/reviews', methods=["GET"])
def reviews_get():
    """returns Reviews"""
    # use the Review class' static .all method
    return Review.all()

@api_routes.route('/reviews/<review_id>', methods=["GET"])
def reviews_specific_get(review_id):
    """returns specified review"""
    # use the Review class' static .specific method
    return Review.specific(review_id)

@api_routes.route('/reviews', methods=["POST"])
def reviews_post():
    """ posts data for new reviews then returns the review data"""
    # -- Usage example --
    # curl -X POST localhost:5000/api/v1/reviews /
    #   -H "Content-Type: application/json" /
    #   -d '{"place_id":<place_id>,"commentor_user_id":"<commentor_user_id>","feedback":"If I could give 0 stars, I would","rating":1}'

    # use the Review class' static .create method
    return Review.create()

@api_routes.route('/reviews/<review_id>', methods=["PUT"])
def reviews_put(review_id):
    """ updates existing review data using specified id """
    # -- Usage example --
    # curl -X PUT [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    # use the Review class' static .update method
    # can only update place_id, commentor_user_id, feedback, rating
    return Review.update(review_id)

@api_routes.route('/reviews/<review_id>', methods=["DELETE"])
def review_delete(review_id):
    """ deletes existing review data using specified id """
    return Review.delete(review_id)
