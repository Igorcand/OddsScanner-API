from flask_restful import Resource, reqparse


from models.employees import EmployeesModel
from db import db

from resources.countries import Country_by_region
from resources.locations import Location_by_region



class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("first_name", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("last_name", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("email", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("phone_number", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("hire_date", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("job_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("salary", type=int, required=True, help="This field cannot be left blank")
    parser.add_argument("comission_pct", type=int, required=True, help="This field cannot be left blank")
    parser.add_argument("manager_id", type=int, required=True, help="This field cannot be left blank")
    parser.add_argument("department_id", type=str, required=True, help="This field cannot be left blank")


    def get(self, employee_id):
        try:
            employee= EmployeesModel.find_by_id(employee_id)
            if employee:
                return employee.json(), 200
            return {'message': 'employee name not found'}, 404 
        except Exception:
            return {'Message': f'An error occurred while getting the employee'}, 500
        
    def post(self, employee_id):
        print(employee_id)
        if EmployeesModel.find_by_id(employee_id):
            return (
                {"Message": f"An country with ID '{employee_id}' already exists"}
            )
        data = Employee.parser.parse_args()
        print(data)
        employee = EmployeesModel(employee_id, **data)
        try:
            employee.save_to_db()
        except:
            return {'Message': f'An error occurred while inserting the employee'}, 500
        return employee.json(), 201

    def delete(self, employee_id):
        try:
            employee = EmployeesModel.find_by_id(employee_id)
            if employee:
                employee.delete_from_db()
                return {'message': 'employee deleted'}, 200 
            return{'message': 'employee not found'}, 404
        except Exception:
            return {'Message': f'An error occurred while deleting employee'}, 500

    def put(self, employee_id):
        try:
            data = Employee.parser.parse_args()
            employee = EmployeesModel.find_by_name(employee_id)
            if employee:
                employee.update_from_db(employee_id, **data)
                employee.save_to_db()
                return employee.json(), 200
            else:
                employee = EmployeesModel(employee_id, **data)
            employee.save_to_db()
            return employee.json(), 200
        except Exception:
            return {'Message': f'An error occurred while editing employee'}, 500

class EmployeesList(Resource):
    def get(self):
        try:
            return {"employees":[x.json() for x in EmployeesModel.find_all()]}
        except Exception:
            return {'Message': f'An error occurred while getting all employees'}, 500


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