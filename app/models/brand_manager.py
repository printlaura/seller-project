from ..database import db
from sqlalchemy import CheckConstraint


class BrandManager(db.Model):
    __tablename__ = 'BrandManager'
    id = db.Column(db.BigInteger, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String(128))

    # relationships
    brands = db.relationship("Brand", back_populates="brand_manager")
