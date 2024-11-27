from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import timedelta
from flask_compress import Compress
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()
compress = Compress()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    # Set session and remember me durations
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(hours=1)  # Duration for 'remember me' sessions
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Duration for regular sessions

    app.config['SECRET_KEY'] = os.getenv('API_KEY')
    
    uri = os.getenv("DATABASE_URL")  # Get the database URL from environment variables
    if uri and uri.startswith("postgres://"):
        # Replace 'postgres://' with 'postgresql://'
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri

    db.init_app(app)
    migrate.init_app(app, db)
    compress.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

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
