from flask import Flask
from dotenv import load_dotenv


load_dotenv()  # This loads environment variables from the .env file



def create_app():
    app = Flask(__name__)
    
    # Configurations can go here
    app.config['SECRET_KEY'] = 'hemmelig'
    
    # Register blueprints or routes
    from .routes import main
    app.register_blueprint(main)

    return app
