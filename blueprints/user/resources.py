from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse, marshal
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from . import *
from blueprints import app, db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.user.model import Users
from datetime import datetime
from blueprints import internal_required

bp_user= Blueprint('user',__name__)
api = Api(bp_user)

class UserResources(Resource):

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        qry = Users.query.filter_by(client_id=claims['id']).first()
        if qry is not None and qry.is_deleted != True:
            return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}
        return {'message':'USER NOT FOUND', "code":404}, 404, { 'Content-Type': 'application/json' }

    @internal_required
    def put(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('full_name', location='json')
            parser.add_argument('email', location='json')
            parser.add_argument('address', location='json')
            parser.add_argument('city', location='json')
            parser.add_argument('telephone', location='json')
            args = parser.parse_args()

            qry.full_name = args['full_name']
            qry.email = args['email']
            qry.address = args['address']
            qry.city = args['city']
            qry.telephone = args['telephone']
            qry.updated_at = datetime.now()
            
            db.session.commit()
            
            return marshal(qry, Users.response_fields), 200, {'Content-Type': 'application/json'}

    @internal_required
    @jwt_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            if qry.is_deleted :
                return {"message":"already deleted"}, 200,
            qry.is_deleted = True
            db.session.commit()
            return {"message":"success", "code":200, "status":"deleted"}, 200, { 'Content-Type': 'application/json' }
        return {'message':'USER NOT FOUND', "code":404}, 404, { 'Content-Type': 'application/json' }

class UserList(Resource):
    
    @internal_required
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        
        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Users.query.filter_by(is_deleted=False)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))
        
        return rows,200
    
api.add_resource(UserList, '/list')
api.add_resource(UserResources,'','/<id>')