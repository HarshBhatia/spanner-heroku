from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.types import PickleType


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facebookId = db.Column(db.String(100),unique = True)
    userName = db.Column(db.String(80), unique=True)
    #email = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post',backref = db.backref('user',lazy = 'joined'),lazy='dynamic')
    attributes = db.Column(PickleType)

    def __init__(self,facebookId,userName):

        self.userName = userName
        self.facebookId = facebookId

    def __repr__(self):
        return str({'userName':self.userName,'id':self.id})

class Post(db.Model):

        id = db.Column(db.Integer,primary_key = True)
        views  = db.Column(db.Integer)
        CDNLink = db.Column(db.String(400))
        pageLink = db.Column(db.String(200))
        title = db.Column(db.String(150))
        postOwnerId = db.Column(db.String(100),db.ForeignKey('user.facebookId'))
        attributes = db.Column(PickleType)

        def __init__(self,CDNLink,title,postOwnerId,views = 0):

            self.CDNLink = CDNLink
            self.title = title
            self.postOwnerId = postOwnerId
            self.views = views


        def __repr__(self):
            return 'Post: {} User: {}'.format(self.title,self.postOwnerId)

db.create_all()