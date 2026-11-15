from flask import Blueprint, jsonify, request

from .albumService import AlbumService


class AlbumController:
    blueprint = Blueprint("albums", __name__, url_prefix="/api/albums")

    def __init__(self):
        self.blueprint = type(self).blueprint

    @staticmethod
    @blueprint.get("/")
    def get_albums():
        albums = AlbumService().getAlbums()
        return jsonify(albums), 200

    @staticmethod
    @blueprint.get("/search")
    def search_albums():
        title = request.args.get("title")
        artist = request.args.get("artist")
        if (title is None) == (artist is None):
            return jsonify(error="Provide exactly one of title or artist"), 400

        service = AlbumService()
        albums = (
            service.findBytitle(title)
            if title is not None
            else service.getAlbumArtist(artist)
        )
        return jsonify(albums), 200

    @staticmethod
    @blueprint.get("/<int:album_id>")
    def get_album_by_id(album_id):
        album = AlbumService().getAlbumById(album_id)
        if album is None:
            return jsonify(error="Album not found"), 404
        return jsonify(album), 200

    @staticmethod
    @blueprint.post("/")
    def post_albums():
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        title = data.get("title")
        description = data.get("description")
        image = data.get("image")
        artist = data.get("artist")
        if not title or not description or not image or not artist:
            return jsonify(
                error="title, description, image, and artist are required"
            ), 400

        album = AlbumService().makeAlbum(title, description, image, artist)
        return jsonify(album), 201

    @staticmethod
    @blueprint.put("/<int:album_id>")
    def update_album(album_id):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        title = data.get("title")
        description = data.get("description")
        image = data.get("image")
        artist = data.get("artist")
        if not title or not description or not image or not artist:
            return jsonify(
                error="title, description, image, and artist are required"
            ), 400

        album = AlbumService().updateAlbum(
            album_id, title, description, image, artist
        )
        if album is None:
            return jsonify(error="Album not found"), 404
        return jsonify(album), 200

    @staticmethod
    @blueprint.delete("/<int:album_id>")
    def delete_album(album_id):
        album = AlbumService().removeAlbum(album_id)
        if album is None:
            return jsonify(error="Album not found"), 404
        return jsonify(album), 200
