from db import db


class LocationsModel(db.Model):
    __tablename__ = 'locations'

    locations_id = db.Column(db.Integer, primary_key=True)
    street_adress = db.Column(db.String(50))
    postal_code = db.Column(db.String(12))
    city = db.Column(db.String(30))
    state_province = db.Column(db.String(25))

    country_id = db.Column(db.String(2), db.ForeignKey('country.country_id'))
    location = db.relationship("DepartmentsModel", lazy="dynamic")
    #region = db.relationship("RegionsModel", back_populates="region_id")

    def __init__(self, locations_id, street_adress, postal_code, city, state_province, country_id):
        self.locations_id = locations_id 
        self.street_adress = street_adress
        self.postal_code = postal_code
        self.city = city
        self.state_province = state_province
        self.country_id = country_id



    def json(self):
        return {
            'locations_id': self.locations_id,
            'street_adress': self.street_adress,
            'postal_code' : self.postal_code,
            'city': self.city,
            'state_province': self.state_province,
            'country_id' : self.country_id,
        }

    @classmethod
    def find_by_name(cls, locations_id):
        return cls.query.filter_by(locations_id=locations_id).first()
        

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db(self, locations_id, street_adress, postal_code, city, state_province, country_id):
        self.locations_id = locations_id
        self.street_adress = street_adress
        self.postal_code = postal_code
        self.city = city
        self.state_province = state_province
        self.country_id = country_id
