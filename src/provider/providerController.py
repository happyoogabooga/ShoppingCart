from flask import Blueprint, jsonify, request

from .providerService import providerService as ProviderService


class ProviderController:
    def __init__(self):
        self.blueprint = Blueprint(
            "providers", __name__, url_prefix="/api/providers"
        )
        self.blueprint.add_url_rule(
            "/", "get_provider", self.get_provider, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/", "post_provider", self.post_provider, methods=["POST"]
        )

    def register_legacy_routes(self, blueprint):
        blueprint.add_url_rule(
            "/provider", "get_provider", self.get_provider, methods=["GET"]
        )
        blueprint.add_url_rule(
            "/provider", "post_provider", self.post_provider, methods=["POST"]
        )

    def get_provider(self):
        providers = ProviderService().getProviders()
        return jsonify(providers), 200

    def post_provider(self):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        if not username or not password or not name:
            return jsonify(error="username, password, and name are required"), 400

        provider = ProviderService().makeProvider(username, password, name)
        return jsonify(provider), 201
