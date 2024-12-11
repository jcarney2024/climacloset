from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import timedelta
from flask_compress import Compress
import os
from flask_mail import Mail

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()
compress = Compress()
login_manager = LoginManager()
mail = Mail()

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

    # Mail configuration should be set before initializing Mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    compress.init_app(app)
    mail.init_app(app)  # Initialize mail after setting config
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint, page_not_found
    app.register_blueprint(main_blueprint)
    
    # blueprint for profile routes
    from .edit import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    # Register error handler
    app.register_error_handler(404, page_not_found)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')
