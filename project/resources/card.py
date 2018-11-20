from flask import request
from flask_restful import Resource
from model import db, Card, CardSchema


cards_schema = CardSchema(many=True)
card_schema = CardSchema()


class CardResource(Resource):
    def get(self):
        cards = Card.query.all()
        cards = cards_schema.dump(cards).data
        return {'status': 'success', 'data': cards}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = card_schema.load(json_data)
        if errors:
            return errors, 422
        card = Card.query.filter_by(name=data['name']).first()
        if card:
            return {'message': 'card already exists'}, 400
        card = Card(
            name=json_data['name'])

        db.session.add(card)
        db.session.commit()

        result = card_schema.dump(card).data

        return {"status": 'success', 'data': result}, 201

    def put(self):
            json_data = request.get_json(force=True)
            if not json_data:
                return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
            data, errors = card_schema.load(json_data)
            if errors:
                return errors, 422
            card = Card.query.filter_by(id=data['id']).first()
            if not card:
                return {'message': 'Card does not exist'}, 400
            card.name = data['name']
            db.session.commit()

            result = card_schema.dump(card).data

            return {"status": 'success', 'data': result}, 204

    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = card_schema.load(json_data)
        if errors:
            return errors, 422
        card = Card.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = card_schema.dump(card).data

        return {"status": 'success', 'data': result}, 204
