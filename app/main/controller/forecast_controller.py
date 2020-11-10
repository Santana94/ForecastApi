from flask_api import status
from flask_restplus import Resource, reqparse, inputs, ValidationError

from app.main.service.forecast_service import ForecastService
from app.main.util.adapters import ApiAdvisorAdaptee, ApiAdvisorAdapter
from app.main.util.dto import ForecastDto

api = ForecastDto.api
_forecast = ForecastDto.forecast

parser = reqparse.RequestParser()
parser.add_argument('id', type=inputs.positive,
                    help="The city id is required.",
                    required=True)


@api.route('')
class Forecast(Resource):
    @api.doc('get a forecast')
    @api.expect(parser)
    def get(self):
        try:
            args = parser.parse_args()
            adaptee = ApiAdvisorAdaptee()
            adapter = ApiAdvisorAdapter(adaptee).request(args['id'])
            service = ForecastService(adapter)
            return service.save()
        except ValidationError as error:
            return {'error': str(error)}, status.HTTP_400_BAD_REQUEST
