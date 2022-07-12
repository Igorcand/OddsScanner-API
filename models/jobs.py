from db import db


class JobsModel(db.Model):
    __tablename__ = 'jobs'

    job_id = db.Column(db.String(10), primary_key=True)
    job_title = db.Column(db.String(35))
    min_salary = db.Column(db.Integer)
    max_salary = db.Column(db.Integer)

    job = db.relationship("JobHistoryModel", lazy="dynamic")

    #db.relationship("CountryModel", lazy="dynamic")

    def __init__(self, job_id, job_title, min_salary, max_salary):
        self.job_id = job_id 
        self.job_title = job_title
        self.min_salary = min_salary
        self.max_salary = max_salary


    def json(self):
        return {
            'job_id': self.job_id,
            'job_title': self.job_title,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,

        }


    @classmethod
    def find_by_id(cls, job_id):
        return cls.query.filter_by(job_id=job_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def update_from_db(self, job_id, job_title, min_salary, max_salary):
        self.job_id = job_id 
        self.job_title = job_title
        self.min_salary = min_salary
        self.max_salary = max_salary
