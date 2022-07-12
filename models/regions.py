from db import db


class RegionsModel(db.Model):
    __tablename__ = 'regions'

    region_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region_name = db.Column(db.String(80))
    region = db.relationship("CountryModel", lazy="dynamic")

    def __init__(self, region_id, region_name):
        self.region_id = region_id 
        self.region_name = region_name

    def json(self):
        return {
            'region_id': self.region_id,
            'region_name': self.region_name,
        }

    @classmethod
    def find_by_name(cls, region_name):
        return cls.query.filter_by(region_name=region_name).first()

    @classmethod
    def find_by_id(cls, region_id):
        return cls.query.filter_by(region_id=region_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def update_from_db(self, region_id, region_name):
        self.region_id = region_id
        self.region_name = region_name
