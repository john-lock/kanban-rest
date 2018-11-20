from flask import Blueprint
from flask_restful import Api
from resources.kanban import Kanban
from resources.card import CardResource
from resources.board import BoardResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Kanban, '/Kanban')
api.add_resource(BoardResource, '/Board')
api.add_resource(CardResource, '/Card')


# add routes for Board/BOARD_ID etc
