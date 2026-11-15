from flask import Blueprint, jsonify, request

from .cartService import cartService as CartService


class CartController:
    blueprint = Blueprint("carts", __name__, url_prefix="/api/carts")

    def __init__(self):
        self.blueprint = type(self).blueprint

    @staticmethod
    @blueprint.get("/")
    def get_cart():
        cart = CartService().getCart()
        return jsonify(cart), 200

    @staticmethod
    @blueprint.get("/user/<int:user_id>")
    def get_cart_by_user_id(user_id):
        carts = CartService().getCartByUserId(user_id)
        return jsonify(carts), 200

    @staticmethod
    @blueprint.get("/<int:cart_id>")
    def get_cart_by_id(cart_id):
        cart = CartService().getCartById(cart_id)
        if cart is None:
            return jsonify(error="Cart not found"), 404
        return jsonify(cart), 200

    @staticmethod
    @blueprint.post("/")
    def post_cart():
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Exepected a JSON obeject"), 400

        cart_id = data.get("cart_id")
        sku = data.get("sku")
        user_id = data.get("user_id")

        if cart_id is None or sku is None or user_id is None:
            return jsonify(error="cart_id, sku, and user_id required"), 400

        cart = CartService().makeCart(cart_id, sku, user_id)
        return jsonify(cart), 201

    @staticmethod
    @blueprint.put("/<int:cart_id>")
    def update_cart(cart_id):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        sku = data.get("sku")
        user_id = data.get("user_id")
        if sku is None or user_id is None:
            return jsonify(error="sku and user_id are required"), 400

        cart = CartService().updateCart(cart_id, sku, user_id)
        if cart is None:
            return jsonify(error="Cart not found"), 404
        return jsonify(cart), 200

    @staticmethod
    @blueprint.delete("/<int:cart_id>")
    def delete_cart(cart_id):
        cart = CartService().removeCart(cart_id)
        if cart is None:
            return jsonify(error="Cart not found"), 404
        return jsonify(cart), 200
