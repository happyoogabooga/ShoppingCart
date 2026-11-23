from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .user.userService import userService as UserService
from .provider.providerService import providerService as ProviderService
from .album.albumService import AlbumService as AlbumService
from .albumlistings.albumlistingsSerivce import albumlistingsService as AlbumListingsService
from .cartitems.cartitemsService import cartitemsService as CartItemsService
from .carts.cartsService import cartsService as CartsService
ui_blueprint = Blueprint("shopping_cart_ui", __name__)


def _get_album_listing(sku):
    return next(
        (
            listing
            for listing in AlbumListingsService().getAlbumListings()
            if listing["sku"] == sku
        ),
        None,
    )


@ui_blueprint.get("/")
def index():
    if "user_id" in session:
        return redirect(url_for("shopping_cart_ui.user_home"))
    if "provider_id" in session:
        return redirect(url_for("shopping_cart_ui.provider_dashboard"))
    return redirect(url_for("shopping_cart_ui.login"))


@ui_blueprint.route("/account/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    role = request.form.get("role", "")
    if not username or not password or not role:
        return render_template(
            "login.html",
            error="Username and password are required.",
        ), 400

    if role == "user":
        user = UserService().authenticateUser(username, password)
        if user is None:
            return render_template("login.html", error="Invalid username or password."), 401

        # Save user_id in Flask session so dashboard knows who is logged in
        session["user_id"] = user["user_id"]
        return redirect(url_for("shopping_cart_ui.dashboard"))
    
    elif role == "provider":
        provider = ProviderService().authenticateProvider(username, password)
        if provider is None:
            return render_template("login.html", error="Invalid username or password."), 401
        session["provider_id"] = provider["provider_id"]
        return redirect(url_for("shopping_cart_ui.provider_dashboard"))
@ui_blueprint.route("/account/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    location = request.form.get("location", "")
    name = request.form.get("name", "name")
    role = request.form.get("role", "")

    if not username or not password or not location:
        return render_template(
            "signup.html",
            error="username, password, and location required"
        ), 400

    if role == "user":
        UserService().makeUser(username, password, location, name)
        userAuth = UserService().authenticateUser(username, password)
        if userAuth is None:
            return render_template("login.html", error="Invalid username or password."), 401

        session["user_id"] = userAuth["user_id"]
        return redirect(url_for("shopping_cart_ui.dashboard"))

    elif role == "provider":
        ProviderService().makeProvider(username, password, name)
        providerAuth = ProviderService().authenticateProvider(username, password)
        if providerAuth is None:
            return render_template("login.html", error = "Invalid username or password")
        session["provider_id"] = providerAuth["provider_id"]
        return redirect(url_for("shopping_cart_ui.provider_dashboard"))

    return render_template("login.html", error = "Invalid username, password, name, or location"), 401

@ui_blueprint.get("/account/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("shopping_cart_ui.login"))
    
    user = UserService().getUserById(user_id)
    if user is None:
        session.pop("user_id", None)
        return redirect(url_for("shopping_cart_ui.login"))
    user_cart = CartsService().getCartsByUserId(user_id)
    cart_item = []
    if user_cart is not None:
        for item in CartItemsService().getCartItemsByCartsId(user_cart["carts_id"]):
            listing = _get_album_listing(item["sku"])
            if listing is not None:
                cart_item.append({**listing, "cartitem_id": item["cartitem_id"]})
    return render_template(
        "dashboard.html",
        user=user,
        cart_item=cart_item,
    )

@ui_blueprint.get("/account/provider_dashboard")
def provider_dashboard():
    provider_id = session.get("provider_id")
    if not provider_id:
        return redirect(url_for("shopping_cart_ui.login"))
    
    provider = ProviderService().getProviderById(provider_id)
    albumListing = AlbumListingsService().getAlbumListingsByProviderid(provider_id)
    return render_template("provider_dashboard.html", provider = provider, albumListing = albumListing)

@ui_blueprint.route("/provider/create_album_listing", methods=["GET", "POST"])
def create_album_listing():
    provider_id = session.get("provider_id")
    if not provider_id:
        return redirect(url_for("shopping_cart_ui.login"))

    albums = AlbumService().getAlbums()
    if request.method == "GET":
        return render_template("create_album_listing.html", albums=albums)

    mode = request.form.get("album_mode")
    price_text = request.form.get("price", "").strip()
    quantity = request.form.get("quantity", type=int)
    error = None

    try:
        price = Decimal(price_text)
        if not price.is_finite() or price < 0:
            error = "Enter a valid non-negative price."
    except InvalidOperation:
        price = None
        error = "Enter a valid non-negative price."

    if quantity is None or quantity < 0:
        error = "Enter a valid non-negative stock quantity."

    if error is None and mode == "existing":
        album_id = request.form.get("album_id", type=int)
        if album_id is None:
            error = "Please select an album."
    elif error is None and mode == "new":
        title = request.form.get("title", "").strip()
        artist = request.form.get("artist", "").strip()
        description = request.form.get("description", "").strip()
        image = request.form.get("image", "").strip()
        if not title or not artist or not description or not image:
            error = "Complete all new album fields."
        else:
            album = AlbumService().makeAlbum(title, description, image, artist)
            album_id = album["album_id"]
    elif error is None:
        error = "Choose whether to use an existing album or add a new one."

    if error is not None:
        return render_template(
            "create_album_listing.html",
            albums=albums,
            error=error,
        ), 400

    AlbumListingsService().makeAlbumListing(
        album_id, provider_id, price, quantity
    )
    return redirect(url_for("shopping_cart_ui.provider_dashboard"))

@ui_blueprint.route("/provider/edit_album_listing/<int:sku>", methods=["GET", "POST"])
def edit_album_listing(sku):
    if "provider_id" not in session:
        return redirect(url_for("shopping_cart_ui.login"))

    oldlisting = AlbumListingsService().getAlbumListingBysku(sku)

    if request.method == "GET":
        return render_template("edit_album_listing.html", listing=oldlisting)
    newPrice = Decimal(request.form.get("price_text", "").strip())
    newQuantity = request.form.get("quantity", type=int)

    AlbumListingsService().updateAlbumListing(sku, oldlisting.get("album_id"), oldlisting.get("provider_id"), newPrice, newQuantity)

    return redirect(url_for("shopping_cart_ui.provider_dashboard"))
#note, it may be a good idea to delete based on the quantity
@ui_blueprint.get("/provider/delete_album/<int:sku>")
def remove_from_listings(sku):
    if "provider_id" not in session:
        return redirect(url_for("shopping_cart_ui.provider_dashboard"))

    AlbumListingsService().deleteAlbumListing(sku)
    return redirect(url_for("shopping_cart_ui.provider_dashboard"))

@ui_blueprint.post("/cart/remove/<int:cartitem_id>")
def remove_from_cart(cartitem_id):
    if "user_id" not in session:
        return redirect(url_for("shopping_cart_ui.login"))

    user_cart = CartsService().getCartsByUserId(session["user_id"])
    if user_cart is None:
        abort(404)
    cart_items = CartItemsService().getCartItemsByCartsId(user_cart["carts_id"])
    if not any(item["cartitem_id"] == cartitem_id for item in cart_items):
        abort(404)
    CartItemsService().removeCartItem(cartitem_id)
    return redirect(url_for("shopping_cart_ui.dashboard"))

@ui_blueprint.get("/user/home")
def user_home():
    if "user_id" not in session:
        return redirect(url_for("shopping_cart_ui.login"))
    
    album_listings = AlbumListingsService().getAlbumListings()
    query = request.args.get("q", "").strip()
    if query:
        query_lower = query.casefold()
        album_listings = [
            listing for listing in album_listings
            if query_lower in listing["title"].casefold()
        ]
    return render_template(
        "home.html",
        album_listings=album_listings,
        search_query=query,
    )

@ui_blueprint.get("/album/details/<int:sku>")
def album_details(sku):
    if "user_id" not in session:
        return redirect(url_for("shopping_cart_ui.login"))
    listing = _get_album_listing(sku)
    if listing is None:
        abort(404)
    provider = ProviderService().getProviderById(listing["provider_id"])
    return render_template(
        "details.html",
        listing=listing,
        provider=provider,
    )

@ui_blueprint.post("/album/cart/add/<int:sku>")
def add_to_cart(sku):
    if "user_id" not in session:
        return redirect(url_for("shopping_cart_ui.login"))

    listing = _get_album_listing(sku)
    if listing is None:
        abort(404)
    if listing["quantity"] < 1:
        flash("This album is currently out of stock.", "error")
        return redirect(url_for("shopping_cart_ui.album_details", sku=sku))

    user_cart = CartsService().makeCarts(session["user_id"])
    CartItemsService().makeCartItem(user_cart["carts_id"], sku)
    return redirect(url_for("shopping_cart_ui.album_details", sku=sku))
