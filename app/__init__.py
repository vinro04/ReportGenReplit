from flask import Flask
from flask_login import LoginManager
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

logger.debug("Flask app initialized")

# Set secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

logger.debug("Secret key set")

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logger.debug("LoginManager initialized")

try:
    from app.models import User, users

    @login_manager.user_loader
    def load_user(user_id):
        user_data = next((data for username, data in users.items() if str(data['id']) == user_id), None)
        if user_data:
            username = next(username for username, data in users.items() if data['id'] == user_data['id'])
            return User(user_data['id'], username, user_data['password_hash'])
        return None

    logger.debug("User loader function defined")

    # Import routes
    from app import routes
    logger.debug("Routes imported")
except Exception as e:
    logger.error(f"Error during app initialization: {str(e)}", exc_info=True)

logger.debug("App initialization completed")