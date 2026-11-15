from flask import Blueprint, jsonify, request
from .album import albumService
from .user import userService
from .cart import cartService
from .provider import providerService
from .checkout import checkoutService
from .albumlistings import albumlistingsSerivce

album_bp = Blueprint("albums", __name__, url_prefix="/api/albums")
user_bp = Blueprint("users", __name__, url_prefix="/api/users")
provider_bp = Blueprint("providers", __name__, url_prefix="/api/providers")
cart_bp = Blueprint("carts", __name__, url_prefix="/api/carts")
checkout_bp = Blueprint("checkouts", __name__, url_prefix="/api/checkouts")
album_listings_bp = Blueprint("album_listings", __name__, url_prefix="/api/album-listings")

api_blueprints = (
    album_bp,
    user_bp,
    provider_bp,
    cart_bp,
    checkout_bp,
    album_listings_bp,
)
@checkout_bp.get("/")
def get_checkouts():
    user_id = request.args.get("user_id", type=int)
    cart_id = request.args.get("cart_id", type=int)

    if (user_id is None) == (cart_id is None):
        return jsonify(error="Provide exactly one of user_id or cart_id"), 400

    service = checkoutService.checkoutService()
    if user_id is not None:
        checkouts = service.getCheckoutsByUserId(user_id)
    else:
        checkouts = service.getCheckoutByCartId(cart_id)
    return jsonify(checkouts), 200

@checkout_bp.post("/")
def post_checkout():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(error = "Expected a JSON object"), 400

    user_id = data.get("user_id")
    total_amount = data.get("total_amount")
    cart_id = data.get("cart_id")

    if not user_id or not total_amount  or not cart_id:
        return jsonify(error = "user_id, total_amount, and cart_id required"), 400

    checkout = checkoutService.checkoutService().makeCheckout(user_id, total_amount, cart_id)
    return jsonify(checkout), 201

@cart_bp.get("/")
def get_cart():
    cart = cartService.cartService().makeCart()
    return jsonify(cart), 200

@cart_bp.post("/")
def post_cart():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(error = "Exepected a JSON obeject"), 400

    cart_id = data.get("cart_id")
    sku = data.get("sku")
    user_id = data.get("user_id")

    if not cart_id or not sku or not user_id:
        return jsonify(error = "cart_id, sku, and user_id required"), 400

    cart = cartService.cartService().makeCart(cart_id, sku, user_id)
    return jsonify(cart), 201

@album_listings_bp.get("/")
def get_albumlistings():
    albumlisting = albumlistingsSerivce.albumlistingsService().getAlbumListings()
    return jsonify(albumlisting)

@album_listings_bp.post("/")
def post_albumlistings():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(error = "Expected a JSON object"), 400

    album_id = data.get("album_id")
    provider_id = data.get("provider_id")
    price = data.get("price")
    quantity = data.get("quantity")

    if not album_id or not provider_id or not price or not quantity:
        return jsonify(error = "album_id, provider_id, price, and quantity required"), 400

    albumListing = albumlistingsSerivce.albumlistingsService().makeAlbumListing(album_id, provider_id, price, quantity)
    return jsonify(albumListing), 201
@provider_bp.get("/")
def get_provider():
    provider = providerService.providerService().getProviders()
    return jsonify(provider), 200

@provider_bp.post("/")
def post_provider():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400

    username = data.get("username")
    password = data.get("password")
    name = data.get("name")
    if not username or not password or not name:
        return jsonify(error="username, password, and name are required"), 400
    provider = providerService.providerService().makeProvider(username, password, name)

    return jsonify(provider), 201
@album_bp.get("/")
def get_albums():
    albums = albumService.AlbumService().getAlbums()
    return jsonify(albums), 200

@album_bp.post("/")
def post_albums():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(error = "Expected a JSON object"), 400

    title = data.get("title")
    description = data.get("description")
    image = data.get("image")
    artist = data.get("artist")
    if not title or not description or not image or not artist:
        return jsonify(error = "title, description, image, and artist are required")

    album = albumService.AlbumService().makeAlbum(title, description, image, artist)
    return jsonify(album), 201
@user_bp.get("/")
def get_users():
    users = userService.userService().getUsers()
    return jsonify(users), 201

@user_bp.post("/")
def post_user():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400

    username = data.get("username")
    password = data.get("password")
    location = data.get("location")
    if not username or not password or not location:
        return jsonify(error="username, password, and location are required"), 400

    users = userService.userService().makeUser(
        username=username,
        password=password,
        location=location,
    )
    return jsonify(users), 201