from ..database import db
from sqlalchemy import CheckConstraint


class MarketplaceUser(db.Model):
    __tablename__ = 'MarketplaceUser'
    id = db.Column(db.BigInteger, primary_key=True)
    user_name = db.Column(db.String, unique=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    marketplace_id = db.Column(db.BigInteger, db.ForeignKey('Marketplace.id', onupdate="CASCADE", ondelete="SET NULL"))
    last_updated = db.Column(db.Date)

    # relationships
    buyers = db.relationship("Buyer", back_populates="user")
    marketplace = db.relationship("Marketplace")
