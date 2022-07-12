from db import db


class CountryModel(db.Model):
    __tablename__ = 'country'

    country_id = db.Column(db.String(2), primary_key=True)
    country_name = db.Column(db.String(80))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'))
    country = db.relationship("LocationsModel", lazy="dynamic")
    #region = db.relationship("RegionsModel", back_populates="region_id")

    def __init__(self, country_id, country_name, region_id):
        self.country_id = country_id 
        self.country_name = country_name
        self.region_id = region_id

    def json(self):
        return {
            'country_id': self.country_id,
            'country_name': self.country_name,
            'region_id' : self.region_id
        }

    @classmethod
    def find_by_name(cls, country_id):
        return cls.query.filter_by(country_id=country_id).first()
        

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, country_id, country_name,  region_id):
        self.country_id = country_id
        self.country_name = country_name
        self.region_id = region_id
        