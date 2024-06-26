""" objects that handles all default RestFul API actions for Place """
from api.v1 import api_routes
from models.place_amenity import Place


@api_routes.route('/places', methods=["POST"])
def places_post():
    """adds a new Place and returns it"""
    return Place.create()

@api_routes.route('/places', methods=["GET"])
def places_get():
    """returns all Places"""
    return Place.all()

@api_routes.route('/places/<place_id>', methods=["GET"])
def places_specific_get(place_id):
    """returns a specific Places"""
    return Place.specific(place_id)

@api_routes.route('/places/<place_id>', methods=["PUT"])
def places_put(place_id):
    """updates a specific Place and returns it"""
    return Place.update(place_id)

@api_routes.route('/places/<place_id>', methods=["DELETE"])
def place_delete(place_id):
    """ deletes existing place data using specified id """
    return Place.delete(place_id)
