from flask import Blueprint, jsonify, request

from .providerService import providerService as ProviderService


class ProviderController:
    blueprint = Blueprint("providers", __name__, url_prefix="/api/providers")

    def __init__(self):
        self.blueprint = type(self).blueprint

    @staticmethod
    @blueprint.get("/")
    def get_provider():
        providers = ProviderService().getProviders()
        return jsonify(providers), 200

    @staticmethod
    @blueprint.post("/")
    def post_provider():
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

    @staticmethod
    @blueprint.get("/search")
    def get_provider_by_name():
        name = request.args.get("name")
        if not name:
            return jsonify(error="name query parameter is required"), 400

        providers = ProviderService().getProviderByName(name)
        return jsonify(providers), 200

    @staticmethod
    @blueprint.get("/<int:provider_id>")
    def get_provider_by_id(provider_id):
        provider = ProviderService().getProviderById(provider_id)
        if provider is None:
            return jsonify(error="Provider not found"), 404
        return jsonify(provider), 200

    @staticmethod
    @blueprint.put("/<int:provider_id>")
    def update_provider(provider_id):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(error="Expected a JSON object"), 400

        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        if not username or not password or not name:
            return jsonify(error="username, password, and name are required"), 400

        provider = ProviderService().updateProvider(
            provider_id, username, password, name
        )
        if provider is None:
            return jsonify(error="Provider not found"), 404
        return jsonify(provider), 200

    @staticmethod
    @blueprint.delete("/<int:provider_id>")
    def delete_provider(provider_id):
        provider = ProviderService().deleteProvider(provider_id)
        if provider is None:
            return jsonify(error="Provider not found"), 404
        return jsonify(provider), 200