from flask_restplus import Namespace, fields


class ForecastDto:
    api = Namespace('forecast', description='forecast related operations')
    forecast = api.model('forecast', {
        'id': fields.Integer(required=True, description='city id'),
        'city': fields.String(required=True, description='city name'),
        'state': fields.String(required=True, description='state name'),
        'country': fields.String(description='country name'),
        'date': fields.DateTime(description='forecast date'),
        'rain_probability': fields.DateTime(description='rain probability'),
        'rain_precipitation': fields.DateTime(description='rain precipitation'),
        'max_temp': fields.DateTime(description='max. temperature'),
        'min_temp': fields.DateTime(description='min. temperature'),
    })


class AnalyzeDto:
    api = Namespace('analyze', description='forecast analysis')
