from .. import db


class Forecast(db.Model):
    """ Forecast Model for storing requested forecast information """
    __tablename__ = "forecast"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    rain_probability = db.Column(db.Float, nullable=True)
    rain_precipitation = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Forecast '{self.city}' - '{self.id}' >"
