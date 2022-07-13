from flask import Flask
from flask_restful import Api

from db import db
from resources.regions import Region, RegionsList
from resources.countries import Country, CountriesList, Country_by_region
from resources.locations import Location, LocationsList, Location_by_country, Location_by_region
from resources.departments import Department, DepartmentsList, Department_by_location, Department_by_country, Department_by_region
from resources.jobs import Jobs, JobsList
from resources.job_history import JobHistory, JobHistoryList
from resources.employees import Employee, EmployeesList

from default.default import Default

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Region, "/region/<string:region_name>")
api.add_resource(RegionsList, "/regions")

api.add_resource(Country, "/country/<string:country_id>")
api.add_resource(CountriesList, "/countries/")
api.add_resource(Country_by_region, "/country_by_region/<int:region_id>")

api.add_resource(Location, "/location/<int:location_id>")
api.add_resource(LocationsList, "/locations")
api.add_resource(Location_by_country, "/locations_by_country/<string:country_id>")
api.add_resource(Location_by_region, "/locations_by_region/<int:region_id>")

api.add_resource(Department, "/department/<int:department_id>")
api.add_resource(DepartmentsList, "/departments")
api.add_resource(Department_by_location, '/departments_by_location/<int:location_id>')
api.add_resource(Department_by_country, '/departments_by_country/<string:country_id>')
api.add_resource(Department_by_region, '/departments_by_region/<int:region_id>')

api.add_resource(Jobs, "/job/<string:job_id>")
api.add_resource(JobsList, "/jobs")

api.add_resource(JobHistory, "/job_history/<int:employee_id>")
api.add_resource(JobHistoryList, "/job_histories")

api.add_resource(Employee, "/employee/<int:employee_id>")
api.add_resource(EmployeesList, "/employees")

api.add_resource(Default, '/default')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)