from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import timedelta
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=30)  # 30 days

    app.config['SECRET_KEY'] = 'API_KEY'
    
    uri = os.getenv("DATABASE_URL")  # Get the database URL from environment variables
    if uri and uri.startswith("postgres://"):
        # Replace 'postgres://' with 'postgresql://'
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint, page_not_found
    app.register_blueprint(main_blueprint)

    # Register error handler
    app.register_error_handler(404, page_not_found)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')
