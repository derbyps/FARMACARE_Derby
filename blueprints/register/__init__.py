from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
import json
from blueprints import db, app
from blueprints.client.model import Clients
from blueprints.user.model import Users
from sqlalchemy import desc
import uuid, hashlib
from blueprints import internal_required

bp_register = Blueprint('register', __name__)
api = Api(bp_register)

class RegisterResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', location='json')
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json')
        parser.add_argument('status',type=bool, location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('address', location='json')
        parser.add_argument('city', location='json')
        parser.add_argument('telephone', location='json')
        parser.add_argument('is_deleted',type=bool, location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        client = Clients(args['username'], hash_pass, args['status'], salt)
        db.session.add(client)
        db.session.flush()
        
        user = Users(client.id, args['full_name'], args['email'], args['address'], args['city'], args['telephone'], args['is_deleted'])
        db.session.add(user)
        
        db.session.commit()

        app.logger.debug('DEBUG: %s', client)
        app.logger.debug('DEBUG: %s', user)
        
        return {'message':'SUCCESS'}, 200
        
        # return marshal(client, Clients.response_fields), 200
            
api.add_resource(RegisterResource, '', '/<id>')
