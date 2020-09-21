from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship
# from blueprints.customer.model import Customers
# from blueprints.seller.model import Sellers

class Clients(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    status = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user = db.relationship("Users", cascade="all, delete-orphan", passive_deletes=True)

    response_fields ={
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
        }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'status' : fields.Boolean
    }

    def __init__(self, username, password, status, salt):
        self.username = username
        self.password = password
        self.status = status
        self.salt = salt
      

    def __repr__(self):
        return '<Client %r>'%self.id