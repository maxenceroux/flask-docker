from flask_restful import Resource
from flask import  jsonify, request
import datetime
import logging as logger
from models import Users, UsersSchema
from database import db_session

users_schema = UsersSchema(many=True)
user_schema = UsersSchema()


class User(Resource):
    def get(self):
        logger.debug("Inside get method")
        all_users = Users.query \
            .all()
        result = users_schema.dump(all_users)
        return jsonify(result)

    def post(self):
        logger.debug("Inside post method")
        username = request.json['utilisateur']
        email = request.json['email']            
        new_user = Users(utilisateur=username, email=email, date_creation=datetime.datetime.now(), date_modification=datetime.datetime.now())
        db_session.add(new_user)
        db_session.commit() 
        return jsonify(user_schema.dump(new_user))

   
    def put(self):
        logger.debug("Inside put method")
        return {"message":"inside put method"}, 200

    def delete(self):
        logger.debug("Inside delete method")
        return {"message":"inside delete method"}, 200


