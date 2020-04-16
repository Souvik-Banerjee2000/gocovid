from models.user import *
from flask_restful import Resource, reqparse, request
from werkzeug.security import safe_str_cmp
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)
from blacklists import BLACKLIST
class UserProfileResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field can not be left blank'
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field can not be left blank'
    )
    parser.add_argument(
        'isadmin',
        type=int,
        required=True,
        help='This field can not be left blank'
    )

    
    def post(self):
        admin_password = '/20#admin@covid'
        data = self.parser.parse_args()
        
        data['isadmin'] = bool(data['isadmin'])


        if UserProfile.find_by_username(data['username']):
            return {'msg': 'A user alreadyexists with this username'}, 400
        

        if data['isadmin'] and data['password']!=admin_password:
            return {'msg':'If you are a admin try to enter the correct admin password'}    

        user = UserProfile(username=data['username'], password=data['password'], isadmin = data['isadmin'], no_of_posts = 0)
        user.save_to_db()
        return {"msg": "User created successfully."}, 201



class Fetch_by_Name(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserProfile.find_by_id(id = user_id)
        if user:
            return {'msg':user.username} 
        return {'msg' :'User Does not exist'}       



class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field can not be left blank'
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field can not be left blank'
    )
    def post(self):
        data = self.parser.parse_args()

        user = UserProfile.find_by_username(name = data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            },200
        return {'msg': 'No user with that username or password is wrong'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {'access_token': new_token}, 200

class AddPosts(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'home_town', type=str, required=True, help='Home Town must be provided is required'
    )

    parser.add_argument(
        'OutingNo', type=int, required=True, help='OutingNo Must be there'
    )
    parser.add_argument(
        'RatioOut', type=int, required=True, help='RatioOut Must be there'
    )
    parser.add_argument(
        'RatioIn', type=int, required=True, help='RatioIn Must be there'
    )

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        current_user_id = get_jwt_identity()
        current_user = UserProfile.find_by_id(id = current_user_id)

        if current_user.isadmin == 0:
            if current_user.no_of_posts>=1:
                return {'msg':'You have already added your information you can not add more'}
 




        if data['OutingNo'] is None:
            data['OutingNo'] = 0
        if data['RatioOut'] is None:
            data['RatioOut'] = 0
        if data['RatioIn'] is None:
            data['RatioIn'] = 0

        user_name = current_user.username

        post = UserPosts(user_name=current_user.username,home_town=data['home_town'], OutingNo=int(data['OutingNo']), RatioOut=int(data['RatioOut']), RatioIn=int(data['RatioIn']), user = current_user)
        post.save_to_db()
        current_user.no_of_posts+=1
        current_user.save_to_db()
        return {'msg': 'Post added successfully'}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
