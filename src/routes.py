from .album.albumController import AlbumController
from .albumlistings.albumlistingsController import AlbumListingsController
from .cart.cartController import CartController
from .checkout.checkoutController import CheckoutController
from .provider.providerController import ProviderController
from .user.userController import UserController

album_controller = AlbumController()
user_controller = UserController()
provider_controller = ProviderController()
cart_controller = CartController()
checkout_controller = CheckoutController()
album_listings_controller = AlbumListingsController()

api_blueprints = (
    album_controller.blueprint,
    user_controller.blueprint,
    provider_controller.blueprint,
    cart_controller.blueprint,
    checkout_controller.blueprint,
    album_listings_controller.blueprint,
)
