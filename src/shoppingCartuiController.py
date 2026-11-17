from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .user.userService import userService as UserService
from .cart.cartService import cartService as CartService
from .checkout.checkoutService import checkoutService as CheckoutService
from .provider.providerService import providerService as ProviderService
ui_blueprint = Blueprint("shopping_cart_ui", __name__)


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
    cart_items = CartService().getCartByUserId(user_id)
    checkout_items = CheckoutService().getCheckoutsByUserId(user_id)

    return render_template(
        "dashboard.html",
        user=user,
        cart_items=cart_items,
        checkout_items=checkout_items
    )

@ui_blueprint.get("/account/provider_dashboard")
def provider_dashboard():
    provider_id = session.get("provider_id")
    if not provider_id:
        return redirect(url_for("shopping_cart_ui.login"))
    
    provider = ProviderService().getProviderById(provider_id)

    return render_template("provider_dashboard.html", provider = provider)

@ui_blueprint.get("/cart/remove/<int:cart_id>")
def remove_from_cart(cart_id):
    if "user_id" not in session:
        return redirect(url_for("shopping_cart_ui.login"))

    CartService().removeCart(cart_id)
    return redirect(url_for("shopping_cart_ui.dashboard"))
