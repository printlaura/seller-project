from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from .database import db
from .routes import bp as main_bp
from config import DevelopmentConfig  # import ProductionConfig if working on prod environment

from flask_migrate import Migrate





def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(DevelopmentConfig)  # Load configurations

    db.init_app(app)  # Initialize the SQLAlchemy object with the app

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    app.register_blueprint(main_bp)

    @app.cli.command("create-db")
    def create_db():
        # Create the database tables.
        db.create_all()
        print("Database tables created successfully.")

        """
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        """
    # import models
    from app.models import Brand, BrandManager, Item, Category, Country, Region, Marketplace, City
    from app.models import MarketplaceUser, SalesOrder, ItemOrdered, Buyer

    return app
