from flask_restful import Resource
import logging as logger
from flask import request, json, Response, Blueprint,jsonify
import datetime
from models import Users, UsersSchema
from database import db_session

users_schema = UsersSchema(many=True)
user_schema = UsersSchema()

class UserById(Resource):
    def get(self, user_id):
        logger.debug("Inside get method")
        user = Users.query \
            .get(user_id)
        if user is not None:
            user_schema = UsersSchema()
            return jsonify(user_schema.dump(user))
        else:
            return {'message':f"user not found, id = {user_id}"}
        result = user_schema.dump(user)
        return jsonify(result)

    def post(self):
        logger.debug("Inside post method of task by id")
        return {"message":f"inside post method of task by id, TASK-ID = {task_id}"}, 200
        
    
    def put(self, user_id):
        user = Users.query.get(user_id)
        username = request.json['utilisateur']
        email = request.json['email']
        user.email = email
        user.utilisateur = username
        user.date_modification = datetime.datetime.now()
        db_session.commit()
        return user_schema.jsonify(user)

    def delete(self,user_id):
        user = Users.query.get(user_id)
        db_session.delete(user)
        db_session.commit()
        return user_schema.jsonify(user)

