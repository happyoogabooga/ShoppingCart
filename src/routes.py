from .album.albumController import AlbumController
from .albumlistings.albumlistingsController import AlbumListingsController
from .checkout.checkoutController import CheckoutController
from .provider.providerController import ProviderController
from .shoppingCartuiController import ui_blueprint
from .user.userController import UserController

ui_blueprints = (ui_blueprint,)

album_controller = AlbumController()
user_controller = UserController()
provider_controller = ProviderController()
checkout_controller = CheckoutController()
album_listings_controller = AlbumListingsController()

api_blueprints = (
    album_controller.blueprint,
    user_controller.blueprint,
    provider_controller.blueprint,
    checkout_controller.blueprint,
    album_listings_controller.blueprint,
)
