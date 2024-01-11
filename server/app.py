#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# has JSON responses printed on separate lines with indentation
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return "Index for Game/Review/User API"


@app.route("/games")
def games():
    games = []

    for game in Game.query.all():
        # for game in Game.query.order_by(Game.title).all():
        # for game in  Game.query.liit(10).all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }

        games.append(game_dict)

    response = make_response(
        # serializes args == jsonify accepts lists/dictionaries == changes from one format to json
        jsonify(games),
        200
    )

    response.headers["Content-Type"] = "application/json"

    return response

    # !!!TypeError: Object of type Game is not JSON serializable
    # return make_response(jsonify(Game.query.all()), 200)


# @app.route("/games/<int:id>")
# def game(id):
#     # SQLAlchemy object
#     game = Game.query.filter_by(id=id).first()

#     # python object
#     game_dict = {
#         "title": game.title,
#         "genre": game.genre,
#         "platform": game.platform,
#         "price": game.price,
#     }

#     response = make_response(
#         # Flask serializes (converts from one format to another) the SQLAlchemy object into a JSON object by getting a list of keys and values to pass to the client.
#         jsonify(game_dict),
#         200
#     )

#     response.headers["Content-Type"] = "application/json"

#     return response


@app.route("/games/<int:id>")
def game(id):
    game = Game.query.filter_by(id=id).first()

    # can now access reviews thanks to SerializerMixin + serialize_rules in models.py
    game_dict = game.to_dict()

    response = make_response(
        # it still needs to be JSON, after all
        jsonify(game_dict), 200
    )
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
