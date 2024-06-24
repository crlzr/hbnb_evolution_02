""" objects that handles all default RestFul API actions for City """
from api.v1 import api_routes
from models.city import City

@api_routes.route('/cities', methods=["GET"])
def cities_get():
    """ get data for all cities """
    return City.all()

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
    city_data = storage.get('City', 'id', city_id)
    c = city_data[0].country
    data.append({
        "id": c.id,
        "name": c.name,
        "code": c.code,
        "created_at":c.created_at.strftime(City.datetime_format),
        "updated_at":c.updated_at.strftime(City.datetime_format)
    })
    return data

@api_routes.route('/cities/<city_id>', methods=["DELETE"])
def cities_delete(city_id):
    """ deletes existing city data using specified id """
    return City.delete(city_id)
