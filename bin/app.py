from flask import Flask, render_template
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

blueprint = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="index"
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()