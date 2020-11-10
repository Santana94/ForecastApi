from flask_restplus import Api
from flask import Blueprint

from .main.controller.forecast_controller import api as forecast_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FORECAST API',
          version='1.0',
          description='a forecast api'
          )

api.add_namespace(forecast_ns, path='/cidade')
