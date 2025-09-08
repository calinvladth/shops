from datetime import timedelta
from flask import request
from flask_restful import Resource
from models.users import UserModel
from flask_jwt_extended import create_access_token, get_jwt_identity
from models import db
from services import send_email
from wrappers import auth_required, shop_required


class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return "email missing", 500

        password = data.get("password")

        if not password:
            return "password missing", 500

        user_exists = UserModel.query.filter_by(email=email).first()

        if user_exists:
            return "server error", 400

        user = UserModel(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return "ok", 201


class RegisterShop(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return "email missing", 500

        password = data.get("password")

        if not password:
            return "password missing", 500

        user_exists = UserModel.query.filter_by(email=email).first()

        if user_exists:
            return "server error", 400

        user = UserModel(email=email, is_shop=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return "ok", 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return "email missing", 500

        password = data.get("password")

        if not password:
            return "password missing", 500

        user = UserModel.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return "invalid credentials", 401

        token = create_access_token(identity=str(user.id))

        return token, 200


class ForgotPassword(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        if not email:
            return "email is missing", 500

        user = UserModel.query.filter_by(email=email).first()

        if not user:
            return "server error", 500

        reset_token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(minutes=1000000)
        )

        if not reset_token:
            return "server error", 500

        mail_sent = send_email(
            to=user.email,
            subject="Reset your password",
            body=f"http://localhost:8000/reset-password?reset_token={reset_token}",
        )

        if not mail_sent:
            return "server error", 500

        return "ok", 200


class ResetPassword(Resource):
    @auth_required()
    def post(self):
        data = request.get_json()
        new_password = data.get("new_password")

        if not new_password:
            return "password missing", 500

        user_id = get_jwt_identity()

        if not user_id:
            return "server error", 500

        user = UserModel.query.get(user_id)

        if not user:
            return "no user", 404

        user.set_password(new_password)
        db.session.commit()

        return "ok", 200


class RestrictedRoute(Resource):
    @shop_required()
    def get(self, user):

        user_id = get_jwt_identity()

        return user.to_dict()
