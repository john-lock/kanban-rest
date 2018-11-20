from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    cards = db.relationship('Card')

    def __init__(self, name):
        self.name = name


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.Integer())

    def __init__(self, card, board_id):
        self.card = card
        self.board_id = board_id


class BoardSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class CardSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    board_id = fields.Integer(required=True)
    card = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
