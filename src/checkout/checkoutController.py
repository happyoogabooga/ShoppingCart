from flask import Blueprint, jsonify, request

from .checkoutService import checkoutService as CheckoutService


class CheckoutController:
    def __init__(self):
        self.blueprint = Blueprint(
            "checkouts", __name__, url_prefix="/api/checkouts"
        )
        self.blueprint.add_url_rule(
            "/", "get_checkouts", self.get_checkouts, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/", "post_checkout", self.post_checkout, methods=["POST"]
        )

    def register_legacy_routes(self, blueprint):
        blueprint.add_url_rule(
            "/checkout", "get_checkouts", self.get_checkouts, methods=["GET"]
        )
        blueprint.add_url_rule(
            "/checkout", "post_checkout", self.post_checkout, methods=["POST"]
        )

    def get_checkouts(self):
        user_id = request.args.get("user_id", type=int)
        cart_id = request.args.get("cart_id", type=int)

        if (user_id is None) == (cart_id is None):
            return jsonify(error="Provide exactly one of user_id or cart_id"), 400

        service = CheckoutService()
        if user_id is not None:
            checkouts = service.getCheckoutsByUserId(user_id)
        else:
            checkouts = service.getCheckoutByCartId(cart_id)
        return jsonify(checkouts), 200

    def post_checkout(self):
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
