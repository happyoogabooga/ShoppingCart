from flask import Blueprint, jsonify, request

from .cartService import cartService as CartService


class CartController:
    def __init__(self):
        self.blueprint = Blueprint("carts", __name__, url_prefix="/api/carts")
        self.blueprint.add_url_rule("/", "get_cart", self.get_cart, methods=["GET"])
        self.blueprint.add_url_rule("/", "post_cart", self.post_cart, methods=["POST"])

    def register_legacy_routes(self, blueprint):
        blueprint.add_url_rule("/cart", "get_cart", self.get_cart, methods=["GET"])
        blueprint.add_url_rule("/cart", "post_cart", self.post_cart, methods=["POST"])

    def get_cart(self):
        cart = CartService().makeCart()
        return jsonify(cart), 200

    def post_cart(self):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Exepected a JSON obeject"), 400

        cart_id = data.get("cart_id")
        sku = data.get("sku")
        user_id = data.get("user_id")

        if not cart_id or not sku or not user_id:
            return jsonify(error="cart_id, sku, and user_id required"), 400

        cart = CartService().makeCart(cart_id, sku, user_id)
        return jsonify(cart), 201
