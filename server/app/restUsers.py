from flask import g
from flask_restful import Resource, reqparse, fields, marshal, abort
from app import api, db, basic_auth, token_auth, multi_auth
from app.models import User
from app.views import APIv1

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@token_auth.error_handler
@basic_auth.error_handler
def unauthorized():
    abort(401, message="Unauthorized access")

@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

users_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'url': fields.Url('user')
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'phone': fields.String,
    'url': fields.Url('user')
}

class UserList(Resource):
    method_decorators = {'get': [multi_auth.login_required]}

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True,
            help = 'No username provided', location = 'json')
        self.reqparse.add_argument('password', type = str, required = True,
            help = 'No password provided', location = 'json')
        self.reqparse.add_argument('phone', type = str, required = True,
            help = 'No phone provided', location = 'json')
        self.reqparse.add_argument('fts_key', type = int, required = True,
            help = 'No ftskey provided', location = 'json')
        super(UserList, self).__init__()

    def get(self):
        users = User.query.all()
        self.abortIfUsersDoesntExist(users)
        return { 'users': marshal(users, users_fields) }

    def post(self):
        args = self.reqparse.parse_args()
        self.abortIfUserAlreadyExist(args['username'], args['phone'])
        user = User(
            username = args['username'],
            phone = args['phone'],
            fts_key = args['fts_key'])
        user.hash_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return { 'user': marshal(user, user_fields) }, 201

    @staticmethod
    def abortIfUsersDoesntExist(users):
        if len(users) == 0:
            abort(404, message="Users don't exist in database")

    @staticmethod
    def abortIfUserAlreadyExist(username, phone):
        users = db.session.query(User).filter(
            (User.username == username) | (User.phone == phone)).all()
        if len(users) != 0:
            abort(409, message="Username '{}' and/or phone {} already exist".format(username, phone))

class Users(Resource):
    method_decorators = [multi_auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, location = 'json')
        self.reqparse.add_argument('password', type = str, location = 'json')
        self.reqparse.add_argument('phone', type = str, location = 'json')
        self.reqparse.add_argument('fts_key', type = int, location = 'json')
        super(Users, self).__init__()

    def get(self, id):
        user = User.query.get(id)
        self.abortIfUserDoesntExist(user, id)
        return { 'user': marshal(user, user_fields) }

    def put(self, id):
        args = self.reqparse.parse_args()
        user = User.query.get(id)
        self.abortIfUserDoesntExist(user, id)
        self.abortIfUserAlreadyExist(args['username'], args['phone'])
        for key, value in args.items():
            if value is not None:
                if key == "password":
                    user.hash_password(value)
                    continue
                setattr(user, key, value)
        db.session.commit()
        return { 'user': marshal(user, user_fields) }

    @staticmethod
    def abortIfUserDoesntExist(user, id):
        if user is None:
            abort(404, message="User id {} doesn't exist".format(id))

    @staticmethod
    def abortIfUserAlreadyExist(username="", phone=""):
        users = db.session.query(User).filter(
            (User.username == username) | (User.phone == phone)).all()
        print(users)
        if len(users) != 0:
            abort(409, message="Username '{}' and/or phone {} already exist".format(username, phone))

class UserInfo(Resource):
    method_decorators = [multi_auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, location = 'json')
        self.reqparse.add_argument('password', type = str, location = 'json')
        self.reqparse.add_argument('phone', type = str, location = 'json')
        self.reqparse.add_argument('fts_key', type = int, location = 'json')
        super(UserInfo, self).__init__()

    def get(self):
        user = User.query.filter_by(username = g.user.username).first()
        print(g.user.username)
        return { 'user': marshal(user, user_fields) }

    def put(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(username = g.user.username).first()
        self.abortIfUserAlreadyExist(args['username'], args['phone'])
        for key, value in args.items():
            if value is not None:
                if key == "password":
                    user.hash_password(value)
                    continue
                setattr(user, key, value)
        db.session.commit()
        return { 'user': marshal(user, user_fields) }

    @staticmethod
    def abortIfUserAlreadyExist(username="", phone=""):
        users = db.session.query(User).filter(
            (User.username == username) | (User.phone == phone)).all()
        print(users)
        if len(users) != 0:
            abort(409, message="Username '{}' and/or phone {} already exist".format(username, phone))

api.add_resource(UserList, APIv1 + '/users', endpoint = 'users')
api.add_resource(Users, APIv1 + '/users/<int:id>', endpoint = 'user')
api.add_resource(UserInfo, APIv1 + '/users/me', endpoint = 'userme')

class Token(Resource):
    method_decorators = [basic_auth.login_required]

    def get(self):
        user = User.query.filter_by(username = g.user.username).first()
        token = user.generate_auth_token()
        return { 'token': token.decode('ascii') }

api.add_resource(Token, APIv1 + '/token', endpoint = 'token')