import logging
import random
import string

from flask import Blueprint, Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from redis import StrictRedis
from sqlalchemy.sql.expression import func


stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

db = SQLAlchemy()
redis_store = FlaskRedis.from_custom_provider(StrictRedis)

page = Blueprint('page', __name__)


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    db.init_app(app)
    redis_store.init_app(app)

    app.register_blueprint(page)
    app.logger.addHandler(stream_handler)

    return app

@page.route('/')
def index():
    """
    Render the home page where visitors can feed Moby Dock.

    :return: Flask response
    """
    turn = 0
    card = 0
    code = None

    """
    if request.args.get('code'):
    code = request.args.get('code')
     if request.args.get('next'):
    """

    if request.args.get('code'):
        code = request.args.get('code')

    if code is None:
        chars=string.ascii_uppercase + string.digits
        code= ''.join(random.sample(chars*6, 6))
        return render_template('select.html', code=code)
    else:
        if db.session.query(PlaneRift).filter_by(code=code).first() is None:
            planerift = PlaneRift(code=code)
            db.session.add(planerift)
            db.session.commit()
        
        result=db.session.query(PlaneRift).filter_by(code=code).first() 
        if result.turn is None:
            result.card = random.randint(1,40)
            result.turn = 1
            db.session.commit()
            db.session.query(PlaneRift).filter_by(code=code).first() 
        else:
            if request.args.get('next'):
                card_count = redis_store.incr('card_count')
                result.card = random.randint(1,40)
                result.turn += 1
                db.session.commit()
            turn = result.turn
            card = result.card
        card_count = redis_store.get('card_count')        
        return render_template('layout.html', card_count=card_count, code=code, turn=turn, card=card)


@page.route('/seed')
def seed():
    """
    Reset the database and seed it with a few messages.

    :return: Flask redirect
    """
    db.drop_all()
    db.create_all()

    codes = [
        "1234",
        'QWER',
        "zxcv"
    ]

    for code in codes:
        planerift = PlaneRift(code=code)
        db.session.add(planerift)
        db.session.commit()

    return redirect(url_for('page.index'))


class PlaneRift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text())
    turn = db.Column(db.Integer)
    card =  db.Column(db.Integer)
