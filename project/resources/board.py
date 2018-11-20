from flask import request
from flask_restful import Resource
from model import db, Board, BoardSchema


boards_schema = BoardSchema(many=True)
board_schema = BoardSchema()


class BoardResource(Resource):
    def get(self):
        boards = Board.query.all()
        boards = boards_schema.dump(boards).data
        return {'status': 'success', 'data': boards}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = board_schema.load(json_data)
        if errors:
            return errors, 422
        board = Board.query.filter_by(name=data['name']).first()
        if board:
            return {'message': 'Board already exists'}, 400
        board = Board(
            name=json_data['name'])

        db.session.add(board)
        db.session.commit()

        result = board_schema.dump(board).data

        return {"status": 'success', 'data': result}, 201

    def put(self):
            json_data = request.get_json(force=True)
            if not json_data:
                return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
            data, errors = board_schema.load(json_data)
            if errors:
                return errors, 422
            board = Board.query.filter_by(id=data['id']).first()
            if not board:
                return {'message': 'Board does not exist'}, 400
            board.name = data['name']
            db.session.commit()

            result = board_schema.dump(board).data

            return {"status": 'success', 'data': result}, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = board_schema.load(json_data)
        if errors:
            return errors, 422
        board = Board.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = board_schema.dump(board).data

        return {"status": 'success', 'data': result}, 204
