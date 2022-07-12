from flask_restful import Resource, reqparse

from models.jobs import JobsModel

class Jobs(Resource):
    parser = reqparse.RequestParser() 
    #parser.add_argument("job_id", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("job_title", type=str, required=True, help="This field cannot be left blank")
    parser.add_argument("min_salary", type=int, required=True, help="This field cannot be left blank")
    parser.add_argument("max_salary", type=int, required=True, help="This field cannot be left blank")

    def get(self, job_id):
        try:
            job = JobsModel.find_by_id(job_id)
            if job:
                return job.json(), 200
            return {'message': 'Job_id not found'}, 404 
        except Exception:
            return {'Message': f'An error occurred while getting the job'}, 500
        
    def post(self, job_id):
        print(job_id)
        job = JobsModel.find_by_id(job_id)
        if job:
            return (
                {"Message": f"An job with name '{job_id}' already exists"}
            )
        data = Jobs.parser.parse_args()
        print(data)
        job = JobsModel(job_id, **data)
        try:
            job.save_to_db()
        except:
            return {'Message': f'An error occurred while inserting the job'}, 500
        return job.json(), 201

    def delete(self, job_id):
        try:
            job = JobsModel.find_by_id(job_id)
            if job:
                job.delete_from_db()
                return {'message': 'job deleted'}, 200 
            return{'message': 'job not found'}, 404
        except Exception:
            return {'Message': f'An error occurred while deleting the job'}, 500

    def put(self, job_id):
        try:
            data = Jobs.parser.parse_args()
            job = JobsModel.find_by_id(job_id)

            if job:
                job.update_from_db(job_id, **data)
                job.save_to_db()
                return job.json(), 200
            else:
                job = JobsModel(job_id, **data)
            job.save_to_db()
            return job.json(), 200
        except Exception:
            return {'Message': f'An error occurred while editing the job'}, 500

class JobsList(Resource):
    def get(self):
        try:
            return {"jobs":[x.json() for x in JobsModel.find_all()]}
        except Exception:
            return {'Message': f'An error occurred while getting all jobs'}, 500

