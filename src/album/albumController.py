from flask import Blueprint, jsonify, request

from .albumService import AlbumService


class AlbumController:
    def __init__(self):
        self.blueprint = Blueprint("albums", __name__, url_prefix="/api/albums")
        self.blueprint.add_url_rule(
            "/", "get_albums", self.get_albums, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/", "post_albums", self.post_albums, methods=["POST"]
        )

    def get_albums(self):
        albums = AlbumService().getAlbums()
        return jsonify(albums), 200

    def post_albums(self):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        title = data.get("title")
        description = data.get("description")
        image = data.get("image")
        artist = data.get("artist")
        if not title or not description or not image or not artist:
            return jsonify(error="title, description, image, and artist are required")

        album = AlbumService().makeAlbum(title, description, image, artist)
        return jsonify(album), 201
