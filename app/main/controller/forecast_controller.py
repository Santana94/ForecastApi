from flask_api import FlaskAPI

from app.main.service.forecast_service import ForecastService, ApiAdvisorAdapter, ApiAdvisorAdaptee

app = FlaskAPI(__name__)


@app.route("/cidade", methods=['GET'])
def city_forecast_insertion():
    adaptee = ApiAdvisorAdaptee()
    adapter = ApiAdvisorAdapter(adaptee)
    service = ForecastService(adapter)
    return service.save()
