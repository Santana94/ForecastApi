from .. import db


class Forecast(db.Model):
    """ Forecast Model for storing requested forecast information """
    __tablename__ = "forecast"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    rain_probability = db.Column(db.Float, nullable=False)
    rain_precipitation = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Forecast '{self.city}' - '{self.id}' >"
