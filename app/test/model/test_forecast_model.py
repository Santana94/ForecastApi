from app.main import db
from app.main.model.forecast import Forecast


def test_forecast_model_repr_method(db_session, app):
    # GIVEN
    data = {
        'id': 1,
        'city': 'Test City',
        'state': 'Test State',
        'country': 'Test Country',
        'rain_probability': 1.23,
        'rain_precipitation': 234.2
    }

    # WHEN
    forecast = Forecast(**data)
    db.session.add(forecast)
    db.session.commit()

    # THEN
    assert forecast.__repr__() == f"<Forecast '{forecast.city}' - '{forecast.id}' >"
