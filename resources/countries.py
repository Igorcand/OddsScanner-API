from flask_restful import Resource, reqparse

from models.countries import CountryModel
from models.regions import RegionsModel

class Country(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument("country_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("country_name", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("region_id", type=int, required=True, help="This field cannot be left blank")


    def get(self, country_id):
        try:
            country = CountryModel.find_by_name(country_id)
            if country:
                return country.json(), 200
            return {'message': 'country name not found'}, 404 
        except Exception:
            return {'Message': f'An error occurred while getting the country'}, 500
        
    def post(self, country_id):
        if CountryModel.find_by_name(country_id):
            return (
                {"Message": f"An country with ID '{country_id}' already exists"}
            )
        data = Country.parser.parse_args()
        country = CountryModel(country_id, **data)
        try:
            country.save_to_db()
        except:
            return {'Message': f'An error occurred while inserting the country'}, 500
        return country.json(), 201

    def delete(self, country_id):
        try:
            country = CountryModel.find_by_name(country_id)
            if country:
                country.delete_from_db()
                return {'message': 'country deleted'}, 200 
            return{'message': 'country not found'}, 404
        except Exception:
            return {'Message': f'An error occurred while deleting country'}, 500

    def put(self, country_id):
        try:
            data = Country.parser.parse_args()
            country = CountryModel.find_by_name(country_id)
            if country:
                country.update_from_db(country_id, **data)
                country.save_to_db()
                return country.json(), 200
            else:
                country = CountryModel(country_id, **data)
            country.save_to_db()
            return country.json(), 200
        except Exception:
            return {'Message': f'An error occurred while editing the country'}, 500

class CountriesList(Resource):
    def get(self):
        try:
            return {"country":[x.json() for x in CountryModel.find_all()]}
        except Exception:
            return {'Message': f'An error occurred while getting all countries'}, 500

class Country_by_region(Resource):
    def get(self, region_id):
        try:
            countries = CountryModel.query.filter_by(region_id=region_id)
            region = RegionsModel.find_by_id(region_id)
            region = region.json()
            region_name = region['region_name']

            #region = RegionsModel.query.filter_by(region_id=region_id).first()

            return {region_name:[x.json() for x in countries]}
        except Exception:
            return {'Message': f'An error occurred while to try filter all countries by region {region_id}'}, 500