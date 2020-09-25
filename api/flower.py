from flask_restful import Resource
from flask import  jsonify

import logging as logger
from models import Flowers, FlowersSchema
flowers_schema = FlowersSchema(many=True)


class Flower(Resource):
    def get(self):
        logger.debug("Inside get method")
        all_flowers = Signups.query \
            .all()
        result = flowers_schema.dump(all_flowers)
        return jsonify(result)

    def post(self):
        logger.debug("Inside post method")
        return {"message":"inside post method"}, 200

    def put(self):
        logger.debug("Inside put method")
        return {"message":"inside put method"}, 200

    def delete(self):
        logger.debug("Inside delete method")
        return {"message":"inside delete method"}, 200


