from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime
from sqlalchemy_utils import PasswordType
from flask_login import UserMixin
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class Flowers(Base):
    """
    Example Flower table
    """
    __tablename__ = 'flowers'
    id = Column(Integer, primary_key=True)
    nom = Column(String(256))
    espece = Column(String(256), unique=True)
    date_creation = Column(DateTime())
    date_modification = Column(DateTime)

class FlowersSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nom', 'espece', 'date_creation', 'date_modification')


class Users(UserMixin, Base):
    """
    Example Flower table
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    utilisateur = Column(String(256))
    email = Column(String(256), unique=True)   
    mdp = Column(String(1000))
    roles = Column(String(256))
    date_creation = Column(DateTime())
    date_modification = Column(DateTime)

class UsersSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('utilisateur', 'email','roles' 'date_creation', 'date_modification')

class SpotifyUsers(Base):
    """
    Example Flower table
    """
    __tablename__ = 'spotify_users'
    id = Column(Integer, primary_key=True)
    display_name = Column(String(256))
    logged_in_email = Column(String(256))   
    spotify_email= Column(String(256))

class UsersSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('utilisateur', 'email','roles' 'date_creation', 'date_modification')




flower_schema = FlowersSchema()
flowers_schema = FlowersSchema(many=True)
user_schema=UsersSchema()
users_schema=UsersSchema(many=True)