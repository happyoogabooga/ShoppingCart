from flask import Blueprint

from .album.albumController import AlbumController
from .albumlistings.albumlistingsController import AlbumListingsController
from .cart.cartController import CartController
from .checkout.checkoutController import CheckoutController
from .provider.providerController import ProviderController
from .user.userController import UserController

legacy_blueprint = Blueprint(
    "legacy_album_routes", __name__, url_prefix="/api/albums"
)

album_controller = AlbumController()
user_controller = UserController()
provider_controller = ProviderController()
cart_controller = CartController()
checkout_controller = CheckoutController()
album_listings_controller = AlbumListingsController()

for controller in (
    user_controller,
    provider_controller,
    cart_controller,
    checkout_controller,
    album_listings_controller,
):
    controller.register_legacy_routes(legacy_blueprint)

api_blueprints = (
    album_controller.blueprint,
    user_controller.blueprint,
    provider_controller.blueprint,
    cart_controller.blueprint,
    checkout_controller.blueprint,
    album_listings_controller.blueprint,
    legacy_blueprint,
)
