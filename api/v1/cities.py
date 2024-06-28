""" objects that handles all default RestFul API actions for City """
from api.v1 import api_routes
from models.city import City
from data.file_export import export_to_file 
from flask import jsonify

@api_routes.route('/cities', methods=["GET"])
def cities_get():
    """ get data for all cities """
    return jsonify(City.all())

@api_routes.route('/cities', methods=["POST"])
def cities_post():
    """ posts data for new city then returns the city data"""
    # -- Usage example --
    # curl -X POST [URL] /
    #    -H "Content-Type: application/json" /
    #    -d '{"key1":"value1","key2":"value2"}'

    return City.create()

@api_routes.route('/cities/<city_id>', methods=["GET"])
def cities_specific_get(city_id):
    """ returns specific city data """
    return City.specific(city_id)

@api_routes.route('/cities/<city_id>', methods=["PUT"])
def cities_put(city_id):
    """ updates existing city data using specified id """
    return City.update(city_id)

@api_routes.route('/cities/<city_id>/country', methods=["GET"])
def cities_specific_country_get(city_id):
    """ Retrieves the data for the country the city belongs to """

    # Using model relationship to get data
    from data import storage
    data = []
    city_data = storage.get('City', city_id)

    c = city_data.country
    data.append({
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at":c.created_at.strftime(City.datetime_format),
        "updated_at":c.updated_at.strftime(City.datetime_format)
    })
    return data

@api_routes.route('/cities/<city_id>/places', methods=["GET"])
def cities_all_places(city_id):
    """ Retrieves the places for a specific city """
    return City.places_data(city_id)

@api_routes.route('cities/export', methods=["GET"])
def cities_all_export():
    """ exports to file """
    data_to_print = City.all()
    return export_to_file(data_to_print)

@api_routes.route('/cities/<city_id>', methods=["DELETE"])
def cities_delete(city_id):
    """ deletes existing city data using specified id """
    return jsonify(City.delete(city_id))
