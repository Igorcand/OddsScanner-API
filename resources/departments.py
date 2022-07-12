from flask_restful import Resource, reqparse

from models.departments import DepartmentsModel
from models.locations import LocationsModel
from models.countries import CountryModel
from models.regions import RegionsModel
from db import db

from resources.countries import Country_by_region
from resources.locations import Location_by_region

class Department(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument("country_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("department_name", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("manager_id", type=int, required=True, help="This field cannot be left blank")
    parser.add_argument("locations_id", type=int, required=True, help="This field cannot be left blank")


    def get(self, department_id):
        try:
            department= DepartmentsModel.find_by_name(department_id)
            if department:
                return department.json(), 200
            return {'message': 'department name not found'}, 404 
        except Exception:
            return {'Message': f'An error occurred while getting the department'}, 500
        
    def post(self, department_id):
        print(department_id)
        if DepartmentsModel.find_by_name(department_id):
            return (
                {"Message": f"An country with ID '{department_id}' already exists"}
            )
        data = Department.parser.parse_args()
        print(data)
        department = DepartmentsModel(department_id, **data)
        try:
            department.save_to_db()
        except:
            return {'Message': f'An error occurred while inserting the department'}, 500
        return department.json(), 201

    def delete(self, department_id):
        try:
            department = DepartmentsModel.find_by_name(department_id)
            if department:
                department.delete_from_db()
                return {'message': 'department deleted'}, 200 
            return{'message': 'department not found'}, 404
        except Exception:
            return {'Message': f'An error occurred while deleting department'}, 500

    def put(self, department_id):
        try:
            data = Department.parser.parse_args()
            department = DepartmentsModel.find_by_name(department_id)
            if department:
                department.update_from_db(department_id, **data)
                department.save_to_db()
                return department.json(), 200
            else:
                department = DepartmentsModel(department_id, **data)
            department.save_to_db()
            return department.json(), 200
        except Exception:
            return {'Message': f'An error occurred while editing department'}, 500

class DepartmentsList(Resource):
    def get(self):
        try:
            return {"departments":[x.json() for x in DepartmentsModel.find_all()]}
        except Exception:
            return {'Message': f'An error occurred while getting all department'}, 500


class Department_by_location(Resource):
    def get(self, location_id):
        try:
            departments = DepartmentsModel.query.filter_by(locations_id=location_id)
            location = LocationsModel.find_by_name(location_id)
            location = location.json()
            location_id = location['locations_id']
            return {location_id:[x.json() for x in departments]}
        except Exception:
             return {'Message': f'An error occurred while to try filter all departments by location_id {location_id}'}, 500


class Department_by_country(Resource):
    def get(self, country_id):
        try:
   
            results = db.session.query(LocationsModel, CountryModel).join(CountryModel).filter_by(country_id=country_id)
            departments_dict = []
            for locations_model, country_model in results:
                location_id = locations_model.locations_id
                department = Department_by_location.get(location_id, location_id)
                if len(department[location_id]) > 0:
                    departments_dict.append(department)
            return {country_id:[x for x in departments_dict]}
            
        except Exception:
             return {'Message': f'An error occurred while to try filter all departments by country_id {country_id}'}, 500


class Department_by_region(Resource):
    def get(self, region_id):
        try:
            locations = Location_by_region.get(region_id, region_id)
            location_list = []
            for key, value in locations.items():
                for country in value:
                    value_country = country.values()
                    for location in value_country:
                        for id in location:
                            location_list.append(id['locations_id'])
            departments_list = []
            for location_id in location_list:
                department = Department_by_location.get(location_id, location_id)
                if len(department[location_id]) > 0:
                    departments_list.append(department)

            return {region_id:[x for x in departments_list]}
            
        except Exception:
            return {'Message': f'An error occurred while to try filter all departments by region_id {region_id}'}, 500