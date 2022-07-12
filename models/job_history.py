from db import db


class JobHistoryModel(db.Model):
    __tablename__ = 'job_history'

    employee_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))
    job_id = db.Column(db.String(10), db.ForeignKey('jobs.job_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))

    #region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'))

    #location = db.relationship("LocationsModel", lazy="dynamic")

    def __init__(self, employee_id, start_date, end_date, job_id, department_id):
        self.employee_id = employee_id 
        self.start_date = start_date
        self.end_date = end_date
        self.job_id = job_id
        self.department_id = department_id


    def json(self):
        return {
            'employee_id' : self.employee_id,
            'start_date' : self.start_date,
            'end_date' : self.end_date,
            'job_id' : self.job_id,
            'department_id' : self.department_id 
        }

    @classmethod
    def find_by_id(cls, employee_id):
        return cls.query.filter_by(employee_id=employee_id).first()
        

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, employee_id, start_date, end_date, job_id, department_id):
        self.employee_id = employee_id 
        self.start_date = start_date
        self.end_date = end_date
        self.job_id = job_id
        self.department_id = department_id
        