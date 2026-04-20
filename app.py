from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="")
    CORS(app)

    @app.get("/")
    def home():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
