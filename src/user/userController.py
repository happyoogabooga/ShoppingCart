from flask import Blueprint, jsonify, request

from .userService import userService as UserService


class UserController:
    def __init__(self):
        self.blueprint = Blueprint("users", __name__, url_prefix="/api/users")
        self.blueprint.add_url_rule(
            "/", "get_users", self.get_users, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/", "post_user", self.post_user, methods=["POST"]
        )

    def register_legacy_routes(self, blueprint):
        blueprint.add_url_rule(
            "/user", "get_users", self.get_users, methods=["GET"]
        )
        blueprint.add_url_rule(
            "/user", "post_user", self.post_user, methods=["POST"]
        )

    def get_users(self):
        users = UserService().getUsers()
        return jsonify(users), 201

    def post_user(self):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        username = data.get("username")
        password = data.get("password")
        location = data.get("location")
        if not username or not password or not location:
            return jsonify(error="username, password, and location are required"), 400

        users = UserService().makeUser(
            username=username,
            password=password,
            location=location,
        )
        return jsonify(users), 201
