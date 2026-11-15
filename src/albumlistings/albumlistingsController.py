from flask import Blueprint, jsonify, request

from .albumlistingsSerivce import albumlistingsService as AlbumListingsService


class AlbumListingsController:
    def __init__(self):
        self.blueprint = Blueprint(
            "album_listings", __name__, url_prefix="/api/album-listings"
        )
        self.blueprint.add_url_rule(
            "/", "get_albumlistings", self.get_albumlistings, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/", "post_albumlistings", self.post_albumlistings, methods=["POST"]
        )

    def register_legacy_routes(self, blueprint):
        blueprint.add_url_rule(
            "/albumlistings",
            "get_albumlistings",
            self.get_albumlistings,
            methods=["GET"],
        )
        blueprint.add_url_rule(
            "/albumlistings",
            "post_albumlistings",
            self.post_albumlistings,
            methods=["POST"],
        )

    def get_albumlistings(self):
        album_listings = AlbumListingsService().getAlbumListings()
        return jsonify(album_listings)

    def post_albumlistings(self):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        album_id = data.get("album_id")
        provider_id = data.get("provider_id")
        price = data.get("price")
        quantity = data.get("quantity")

        if not album_id or not provider_id or not price or not quantity:
            return jsonify(
                error="album_id, provider_id, price, and quantity required"
            ), 400

        album_listing = AlbumListingsService().makeAlbumListing(
            album_id, provider_id, price, quantity
        )
        return jsonify(album_listing), 201
