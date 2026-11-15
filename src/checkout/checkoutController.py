from flask import Blueprint, jsonify, request

from .checkoutService import checkoutService as CheckoutService


class CheckoutController:
    blueprint = Blueprint("checkouts", __name__, url_prefix="/api/checkouts")

    def __init__(self):
        self.blueprint = type(self).blueprint

    @staticmethod
    @blueprint.get("/")
    def get_checkouts():
        user_id = request.args.get("user_id", type=int)
        cart_id = request.args.get("cart_id", type=int)

        if (user_id is None) == (cart_id is None):
            return jsonify(error="Provide exactly one of user_id or cart_id"), 400

        service = CheckoutService()
        if user_id is not None:
            checkouts = service.getCheckoutsByUserId(user_id)
        else:
            checkouts = service.getCheckoutByCartId(cart_id)
            if checkouts is None:
                return jsonify(error="Checkout not found"), 404
        return jsonify(checkouts), 200

    @staticmethod
    @blueprint.get("/<int:order_number>")
    def get_checkout_by_id(order_number):
        checkout = CheckoutService().getCheckoutById(order_number)
        if checkout is None:
            return jsonify(error="Checkout not found"), 404
        return jsonify(checkout), 200

    @staticmethod
    @blueprint.post("/")
    def post_checkout():
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        user_id = data.get("user_id")
        total_amount = data.get("total_amount")
        cart_id = data.get("cart_id")

        if not user_id or not total_amount or not cart_id:
            return jsonify(error="user_id, total_amount, and cart_id required"), 400

        checkout = CheckoutService().makeCheckout(user_id, total_amount, cart_id)
        return jsonify(checkout), 201

    @staticmethod
    @blueprint.put("/<int:order_number>")
    def update_checkout(order_number):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        user_id = data.get("user_id")
        total_amount = data.get("total_amount")
        cart_id = data.get("cart_id")
        if user_id is None or total_amount is None or cart_id is None:
            return jsonify(
                error="user_id, total_amount, and cart_id are required"
            ), 400

        checkout = CheckoutService().updateCheckout(
            order_number, user_id, total_amount, cart_id
        )
        if checkout is None:
            return jsonify(error="Checkout not found"), 404
        return jsonify(checkout), 200

    @staticmethod
    @blueprint.delete("/<int:order_number>")
    def delete_checkout(order_number):
        checkout = CheckoutService().deleteCheckout(order_number)
        if checkout is None:
            return jsonify(error="Checkout not found"), 404
        return jsonify(checkout), 200
