import datetime
from flask_restful import Resource, reqparse

from models.job_history import JobHistoryModel


class JobHistory(Resource):
    parser = reqparse.RequestParser() 
    #parser.add_argument("country_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("start_date", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("end_date", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("job_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("department_id", type=int, required=True, help="This field cannot be left blank")


    def get(self, employee_id):
        try:
            country = JobHistoryModel.find_by_id(employee_id)
            if country:
                return country.json(), 200
            return {'message': 'employee name not found'}, 404 
        except Exception:
            return {'Message': f'An error occurred while getting the employee_id'}, 500
        
    def post(self, employee_id):
        if JobHistoryModel.find_by_id(employee_id):
            return (
                {"Message": f"An employee with ID '{employee_id}' already exists"}
            )
        data = JobHistory.parser.parse_args()
        employee = JobHistoryModel(employee_id, **data)
        try:
            employee.save_to_db()
        except:
            return {'Message': f'An error occurred while inserting the employee'}, 500
        return employee.json(), 201

    def delete(self, employee_id):
        try:
            employee = JobHistoryModel.find_by_id(employee_id)
            if employee:
                employee.delete_from_db()
                return {'message': 'employee deleted'}, 200 
            return{'message': 'employee not found'}, 404
        except Exception:
            return {'Message': f'An error occurred while deleting employee'}, 500

    def put(self, employee_id):
        try:
            data = JobHistory.parser.parse_args()
            employee = JobHistoryModel.find_by_id(employee_id)
            if employee:
                employee.update_from_db(employee_id, **data)
                employee.save_to_db()
                return employee.json(), 200
            else:
                employee = JobHistoryModel(employee_id, **data)
            employee.save_to_db()
            return employee.json(), 200
        except Exception:
            return {'Message': f'An error occurred while editing the employee'}, 500

class JobHistoryList(Resource):
    def get(self):
        try:
            return {"jobs":[x.json() for x in JobHistoryModel.find_all()]}
        except Exception:
            return {'Message': f'An error occurred while getting all jobs'}, 500

