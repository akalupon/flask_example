import os

from flask import Flask, jsonify
from flask import request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/health', methods=["GET", "POST"])
    def health():
        if request.method == "GET":
            return jsonify(status="OK", method="GET"), 200
        elif request.method == "POST":
            return jsonify(status="OK", method="POST"), 200
        else:
            return jsonify("test")

    @app.route('/send_value', methods=["GET", "POST"])
    def send_value():
        course = request.args["course"]
        rating = request.args.get("rating")
        return {"message": f"{course} with rating {rating}"}

    return app
