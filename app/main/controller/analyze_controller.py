from flask_api import status
from flask_restplus import Resource, reqparse, inputs

from app.main.util.dto import AnalyzeDto

api = AnalyzeDto.api

parser = reqparse.RequestParser()
parser.add_argument('data_inicial', type=inputs.date,
                    help="The initial date is required.",
                    required=True)
parser.add_argument('data_final', type=inputs.date,
                    help="The final date is required.",
                    required=True)


@api.route('')
class Analyze(Resource):
    @api.doc('get a forecast analysis')
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        queryset = self.get_queryset()
        return {}, status.HTTP_200_OK

    def get_queryset(self):
        return
