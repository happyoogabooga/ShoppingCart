from flask import Blueprint, jsonify, request

from .albumlistingsSerivce import albumlistingsService as AlbumListingsService


class AlbumListingsController:
    blueprint = Blueprint(
        "album_listings", __name__, url_prefix="/api/album-listings"
    )

    def __init__(self):
        self.blueprint = type(self).blueprint

    @staticmethod
    @blueprint.get("/")
    def get_albumlistings():
        album_listings = AlbumListingsService().getAlbumListings()
        return jsonify(album_listings), 200

    @staticmethod
    @blueprint.get("/provider/<int:provider_id>")
    def get_albumlistings_by_provider(provider_id):
        album_listings = AlbumListingsService().getAlbumListingsByProviderid(
            provider_id
        )
        return jsonify(album_listings), 200

    @staticmethod
    @blueprint.get("/<int:sku>")
    def get_albumlisting_by_sku(sku):
        album_listing = AlbumListingsService().getAlbumListingBysku(sku)
        if album_listing is None:
            return jsonify(error="Album listing not found"), 404
        return jsonify(album_listing), 200

    @staticmethod
    @blueprint.post("/")
    def post_albumlistings():
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        album_id = data.get("album_id")
        provider_id = data.get("provider_id")
        price = data.get("price")
        quantity = data.get("quantity")

        if (
            album_id is None
            or provider_id is None
            or price is None
            or quantity is None
        ):
            return jsonify(
                error="album_id, provider_id, price, and quantity required"
            ), 400

        album_listing = AlbumListingsService().makeAlbumListing(
            album_id, provider_id, price, quantity
        )
        return jsonify(album_listing), 201

    @staticmethod
    @blueprint.put("/<int:sku>")
    def update_albumlisting(sku):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        album_id = data.get("album_id")
        provider_id = data.get("provider_id")
        price = data.get("price")
        quantity = data.get("quantity")
        if (
            album_id is None
            or provider_id is None
            or price is None
            or quantity is None
        ):
            return jsonify(
                error="album_id, provider_id, price, and quantity are required"
            ), 400

        album_listing = AlbumListingsService().updateAlbumListing(
            sku, album_id, provider_id, price, quantity
        )
        if album_listing is None:
            return jsonify(error="Album listing not found"), 404
        return jsonify(album_listing), 200

    @staticmethod
    @blueprint.delete("/<int:sku>")
    def delete_albumlisting(sku):
        album_listing = AlbumListingsService().deleteAlbumListing(sku)
        if album_listing is None:
            return jsonify(error="Album listing not found"), 404
        return jsonify(album_listing), 200
