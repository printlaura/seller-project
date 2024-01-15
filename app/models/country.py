from ..database import db
from sqlalchemy import CheckConstraint


class Country(db.Model):
    __tablename__ = 'Country'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    exchange_rate_eu = db.Column(db.Float, CheckConstraint('exchange_rate_eu > 0'))
    region_id = db.Column(db.BigInteger, db.ForeignKey('Region.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    # relationships
    region = db.relationship("Region", back_populates="countries")
    cities = db.relationship("City", back_populates="country")
    marketplaces = db.relationship("Marketplace", back_populates="country")
    items = db.relationship("Item", back_populates="country_of_sales")
