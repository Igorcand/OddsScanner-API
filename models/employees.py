from db import db


class EmployeesModel(db.Model):
    __tablename__ = 'employees'

    employees_id = db.Column(db.Integer, db.ForeignKey('job_history.employee_id')) 
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    phone_number = db.Column(db.String(30))
    hire_date = db.Column(db.String(30))
    job_id = db.Column(db.Integer,db.ForeignKey('job_history.job_id')) 
    salary = db.Column(db.Integer)
    comission_pct = db.Column(db.Integer)
    manager_id = db.Column(db.Integer, primary_key=True)
    department_id =db.Column(db.Integer, db.ForeignKey('job_history.employee_id')) 

    
    #department = db.relationship("DepartmentsModel", lazy="dynamic")

    def __init__(self, employees_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, comission_pct, manager_id, department_id):
        self.employees_id = employees_id 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number 
        self.hire_date = hire_date
        self.job_id = job_id
        self.salary = salary
        self.comission_pct = comission_pct 
        self.manager_id = manager_id
        self.department_id = department_id



    def json(self):
        return {
            'employees_id': self.employees_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'hire_date': self.hire_date, 
            'job_id': self.job_id,
            'salary': self.salary,
            'comission_pct': self.comission_pct,
            'manager_id': self.manager_id,
            'department_id': self.department_id 
            }

    @classmethod
    def find_by_id(cls, employees_id):
        return cls.query.filter_by(employees_id=employees_id).first()
        
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, employees_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, comission_pct, manager_id, department_id):
        self.employees_id = employees_id 
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number 
        self.hire_date = hire_date
        self.job_id = job_id
        self.salary = salary
        self.comission_pct = comission_pct 
        self.manager_id = manager_id
        self.department_id = department_id