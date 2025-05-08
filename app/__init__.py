from flask import Flask
from .db import db, migrate
import os
# from .models import task, goal
# from .routes import task_routes
# from .routes.task_routes import task_bp
# from .routes.goal_routes import goal_bp



def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.task_routes import task_bp
    from .routes.goal_routes import goal_bp
    app.register_blueprint(task_bp)
    app.register_blueprint(goal_bp)

    # Register Blueprints here
    # app.register_blueprint(task_routes.task_bp)
    # app.register_blueprint(goal_bp)

    return app
