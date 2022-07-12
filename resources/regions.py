from flask_restful import Resource, reqparse

from models.regions import RegionsModel

class Region(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument("region_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("region_name", type=str, required=True, help="This field cannot be left blank")

    def get(self, region_name):
        try:
            region = RegionsModel.find_by_name(region_name)
            if region:
                return region.json(), 200
            return {'message': 'Region name not found'}, 404 
        except Exception:
            return {'Message': f'An error occurred while getting the region'}, 500
        
    def post(self, region_name):
        id = region_name
        region_id = RegionsModel.find_by_id(id)
        if region_id:
            return (
                {"Message": f"An region with id '{id}' already exists"}
            )
        data = Region.parser.parse_args()
        name = data['region_name']
        region = RegionsModel.find_by_name(name)

        if region:
            return (
                {"Message": f"An region with name '{name}' already exists"}
            )
        region = RegionsModel(region_name, **data)
        try:
            region.save_to_db()
        except:
            return {'Message': f'An error occurred while inserting the region'}, 500
        return region.json(), 201

    def delete(self, region_name):
        try:
            region = RegionsModel.find_by_name(region_name)
            if region:
                region.delete_from_db()
                return {'message': 'region deleted'}, 200 
            return{'message': 'region not found'}, 404
        except Exception:
            return {'Message': f'An error occurred while deleting the region'}, 500

    def put(self, region_name):
        try:
            data = Region.parser.parse_args()
            region = RegionsModel.find_by_id(region_name)

            if region:
                region.update_from_db(region_name, **data)
                region.save_to_db()
                return region.json(), 200
            else:
                region = RegionsModel(region_name, **data)
            region.save_to_db()
            return region.json(), 200
        except Exception:
            return {'Message': f'An error occurred while editing the region'}, 500

class RegionsList(Resource):
    def get(self):
        try:
            return {"regions":[x.json() for x in RegionsModel.find_all()]}
        except Exception:
            return {'Message': f'An error occurred while getting all region'}, 500

