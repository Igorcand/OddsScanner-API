from flask_restful import Resource, reqparse

from models.locations import LocationsModel
from models.countries import CountryModel
from models.regions import RegionsModel
from db import db

class Location(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument("country_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("street_adress", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("postal_code", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("city", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("state_province", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("country_id", type=str, required=True, help="This field cannot be left blank")



    def get(self, location_id):
        try:
            location= LocationsModel.find_by_name(location_id)
            if location:
                return location.json(), 200
            return {'message': 'location name not found'}, 404 
        except Exception:
            return {'Message': f'An error occurred while getting the location'}, 500
        
    def post(self, location_id):
        print(location_id)
        if LocationsModel.find_by_name(location_id):
            return (
                {"Message": f"An country with ID '{location_id}' already exists"}
            )
        data = Location.parser.parse_args()
        print(data)
        location = LocationsModel(location_id, **data)
        try:
            location.save_to_db()
        except:
            return {'Message': f'An error occurred while inserting the location'}, 500
        return location.json(), 201

    def delete(self, location_id):
        try:
            location = LocationsModel.find_by_name(location_id)
            if location:
                location.delete_from_db()
                return {'message': 'location deleted'}, 200 
            return{'message': 'location not found'}, 404
        except Exception:
            return {'Message': f'An error occurred while deleting location'}, 500

    def put(self, location_id):
        try:
            data = Location.parser.parse_args()
            location = LocationsModel.find_by_name(location_id)
            if location:
                location.update_from_db(location_id, **data)
                location.save_to_db()
                return location.json(), 200
            else:
                location = LocationsModel(location_id, **data)
            location.save_to_db()
            return location.json(), 200
        except Exception:
            return {'Message': f'An error occurred while editing the locations'}, 500

class LocationsList(Resource):
    def get(self):
        try:
            return {"locations":[x.json() for x in LocationsModel.find_all()]}
        except Exception:
            return {'Message': f'An error occurred while getting all locations'}, 500


class Location_by_country(Resource):
    def get(self, country_id):
        #try:
            locations = LocationsModel.query.filter_by(country_id=country_id)
            country = CountryModel.find_by_name(country_id)
            country = country.json()
            country_id = country['country_id']

            #region = RegionsModel.query.filter_by(region_id=region_id).first()

            return {country_id:[x.json() for x in locations]}
        # except Exception:
        #     return {'Message': f'An error occurred while to try filter all locations by country_id {country_id}'}, 500


class Location_by_region(Resource):
    def get(self, region_id):
        try:
   
            results = db.session.query(RegionsModel, CountryModel).join(CountryModel).filter_by(region_id=region_id)
            locations_dict = []
            for _, c in results:
                country_id = c.country_id
                location = Location_by_country.get(country_id, country_id)
                if len(location[country_id]) > 0:
                    locations_dict.append(location)
            return {region_id:[x for x in locations_dict]}
            


        except Exception:
             return {'Message': f'An error occurred while to try filter all countries by region {region_id}'}, 500