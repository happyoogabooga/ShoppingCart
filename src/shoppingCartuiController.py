from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from .user.userService import userService as UserService


ui_blueprint = Blueprint("shopping_cart_ui", __name__)


@ui_blueprint.route("/account/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if not username or not password:
        return render_template(
            "login.html",
            error="Username and password are required.",
        ), 400

    user = UserService().authenticateUser(username, password)
    if user is None:
        return render_template("login.html", error="Invalid username or password."), 401

    return redirect(url_for("shopping_cart_ui.dashboard"))


@ui_blueprint.get("/account/dashboard")
def dashboard():
    return render_template("dashboard.html")