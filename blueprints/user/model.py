import random, logging
from blueprints import db
from flask_restful import fields
from blueprints.client.model import Clients
from sqlalchemy import Integer, String, Column, ForeignKey

class Users(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
	client_id = db.Column(db.Integer, ForeignKey(Clients.id, ondelete='CASCADE'), nullable=False)
	full_name = db.Column(db.String(255))
	email = db.Column(db.String(100), unique = True)
	address = db.Column(db.String(200))
	city = db.Column(db.String(200))
	telephone = db.Column(db.String(100))
	is_deleted = db.Column(db.Boolean, nullable=True, default=False)

	response_fields = {
		'id':fields.Integer,
		'client_id':fields.Integer,
		'full_name':fields.String,
		'email':fields.String,
		'address':fields.String,
		'city':fields.String,
		'telephone' :fields.String
	}

	def __init__(self, client_id, full_name, email, address, city, telephone, is_deleted):
		self.client_id = client_id
		self.full_name = full_name
		self.email = email
		self.address = address
		self.city = city
		self.telephone = telephone
		self.is_deleted = is_deleted

	def __repr__(self):
		return '<User %r>' % self.id