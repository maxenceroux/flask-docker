from flask_restful import Api
from app import app  
from .flower import Flower
from .user import User
from .user_by_id import UserById

rest_srv = Api(app)
rest_srv.add_resource(Flower, "/api/v1.0/flower")
rest_srv.add_resource(User, "/api/v1.0/user")

rest_srv.add_resource(UserById, "/api/v1.0/user/id/<string:user_id>")
