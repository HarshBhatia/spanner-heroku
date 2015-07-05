from flask import Flask,request,abort,render_template,jsonify,make_response
from flask.ext.sqlalchemy import SQLAlchemy
from models import User,Post
from flask.ext.httpauth import HTTPBasicAuth


app = Flask(__name__)

#app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.enivron['DATABASE_URL']

#db and auth initialization
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'spanshots':
        return 'killer'

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

#REST API
@app.route('/postApi',methods = ['POST'])
@auth.login_required
def poster():
    if not request.json:
       abort(400)

    if not User.query.filter_by(facebookId = request.json['postOwnerId']).first():
        return "User not registered yet",400


    # Post Initialization:
    #    __init__(self,CDNLink,title,postOwnerId,views = 0)

    tempPost = Post(str(request.json['CDNLink']),str(request.json['title']),str(request.json['postOwnerId']))
    db.session.add(tempPost)
    db.session.commit()

    return ("Post added with id "+ Post.query.filterby( CDNLink = request.json['CDNLink'])),201


@app.route('/postViewBeta/<int:postId>')
def postViewBeta(postId):

    post = Post.query.filter_by(id = postId).first().__dict__
    user = User.query.filter_by(facebookId = post['postOwnerId']).first().__dict__

    return render_template('postView.html',user= user,post=post)

@app.route('/userViewBeta/<user>')
def userViewBeta(user):

    postList = User.query.filter_by(userName = user).first().posts.all()

    return render_template('userViewBeta.html',postList = postList)



