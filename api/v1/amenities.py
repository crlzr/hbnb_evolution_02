""" objects that handles all default RestFul API actions for Amenity """
from api.v1 import api_routes
from models.place_amenity import Amenity
from data.file_export import export_to_file 
from flask import jsonify

@api_routes.route('/amenities', methods=["POST"])
def amenity_post():
    """ Creates a new Amenity and returns it """
    return Amenity.create()

@api_routes.route('/amenities', methods=["GET"])
def amenity_get():
    """ Gets all Amenities """
    return jsonify(Amenity.all())

@api_routes.route('/amenities/<amenity_id>', methods=["GET"])
def amenity_specific_get(amenity_id):
    """ Gets a specific Amenity """
    return Amenity.specific(amenity_id)

@api_routes.route('/amenities/<amenity_id>', methods=["PUT"])
def amenity_put(amenity_id):
    """ Updates a specific Amenity and returns it """
    return Amenity.update(amenity_id)

@api_routes.route('amenities/export', methods=["GET"])
def amenities_all_export():
    """ exports to file """
    data_to_print = Amenity.all()
    return export_to_file(data_to_print)


@api_routes.route('/amenities/<amenity_id>', methods=["DELETE"])
def amenity_delete(amenity_id):
    """ deletes existing amenity data using specified id """
    return jsonify(Amenity.delete(amenity_id))
