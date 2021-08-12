import os
from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from reluni_review.config import Config

db = SQLAlchemy()
migrate_db = Migrate(db)
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "users.login"  # This line will redirect user when user tries to access unauthorized pages
login_manager.login_message_category = 'warning'  # This line will display an error message during unauthorized access


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate_db.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from reluni_review.users.routes import users
    from reluni_review.posts.routes import posts
    from reluni_review.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
