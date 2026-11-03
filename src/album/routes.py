from flask import Blueprint, jsonify
from . import albumService

album_bp = Blueprint("albums", __name__, url_prefix="/api/albums")

@album_bp.get("/")
def get_albums():
    albums = albumService.AlbumService().getAlbums()
    return jsonify(albums), 200