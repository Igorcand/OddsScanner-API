from db import db


class DepartmentsModel(db.Model):
    __tablename__ = 'departments'

    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(30))
    manager_id = db.Column(db.Integer, ) #db.ForeignKey('job_history.job_id')
    locations_id = db.Column(db.Integer, db.ForeignKey('locations.locations_id'))
    
    department = db.relationship("JobHistoryModel", lazy="dynamic")

    def __init__(self, department_id, department_name, manager_id, locations_id):
        self.department_id = department_id 
        self.department_name = department_name
        self.manager_id = manager_id
        self.locations_id = locations_id



    def json(self):
        return {
            'department_id': self.department_id,
            'department_name': self.department_name,
            'manager_id' : self.manager_id,
            'locations_id': self.locations_id,
        }

    @classmethod
    def find_by_name(cls, department_id):
        return cls.query.filter_by(department_id=department_id).first()
        
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, department_id, department_name, manager_id, locations_id):
        self.department_id = department_id
        self.department_name = department_name
        self.manager_id = manager_id
        self.locations_id = locations_id