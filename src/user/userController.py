from flask import Blueprint, jsonify, request

from .userService import userService as UserService


class UserController:
    blueprint = Blueprint("users", __name__, url_prefix="/api/users")

    def __init__(self):
        self.blueprint = type(self).blueprint

    @staticmethod
    @blueprint.get("/")
    def get_users():
        users = UserService().getUsers()
        return jsonify(users), 200

    @staticmethod
    @blueprint.get("/<int:user_id>")
    def get_user_by_id(user_id):
        user = UserService().getUserById(user_id)
        if user is None:
            return jsonify(error="User not found"), 404
        return jsonify(user), 200

    @staticmethod
    @blueprint.post("/")
    def post_user():
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

    @staticmethod
    @blueprint.put("/<int:user_id>")
    def update_user(user_id):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        username = data.get("username")
        password = data.get("password")
        location = data.get("location")
        if not username or not password or not location:
            return jsonify(error="username, password, and location are required"), 400

        user = UserService().updateUser(user_id, username, password, location)
        if user is None:
            return jsonify(error="User not found"), 404
        return jsonify(user), 200

    @staticmethod
    @blueprint.delete("/<int:user_id>")
    def delete_user(user_id):
        user = UserService().deleteUser(user_id)
        if user is None:
            return jsonify(error="User not found"), 404
        return jsonify(user), 200
