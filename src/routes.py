from flask import Blueprint, jsonify, request
from . import albumService
from ..user import userService

album_bp = Blueprint("albums", __name__, url_prefix="/api/albums")

@album_bp.get("/")
def get_albums():
    albums = albumService.AlbumService().getAlbums()
    return jsonify(albums), 200


@album_bp.get("/user")
def get_users():
    users = userService.userService().getUsers()
    return jsonify(users), 203
@album_bp.post("/user")
def post_user():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400

    username = data.get("username")
    password = data.get("password")
    location = data.get("location")
    if not username or not password or not location:
        return jsonify(error="username, password, and location are required"), 400
    
    users = userService.userService().makeUser(
        username=username,
        password=password,
        location=location,
    )
    return jsonify(users), 201