from flask import Flask
from db import init_app
from src.routes import api_blueprints, ui_blueprints
import os


def load_env_file():
    if not os.path.isfile(".env"):
        return

    with open(".env", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))

app = Flask(__name__)
init_app(app)
for blueprint in api_blueprints:
    app.register_blueprint(blueprint)
load_env_file()

app.config["DATABASE_URL"] = os.getenv("DB_ENCRYPTION_KEY")
for blueprint in ui_blueprints:
    app.register_blueprint(blueprint)
if __name__ == "__main__":
    app.run(debug=True, port=5001)