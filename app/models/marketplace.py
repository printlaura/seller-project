from ..database import db
from sqlalchemy import CheckConstraint


class Marketplace(db.Model):
    __tablename__ = 'Marketplace'
    id = db.Column(db.BigInteger, primary_key=True)
    country_id = db.Column(db.BigInteger, db.ForeignKey('Country.id', onupdate="CASCADE", ondelete="SET NULL"), nullable=False)
    url_domain = db.Column(db.String, CheckConstraint("url_domain LIKE 'www.%'"), nullable=False)

    # relationships
    country = db.relationship("Country", back_populates="marketplaces")
    sales_orders = db.relationship("SalesOrder", back_populates="marketplace")
    marketplace_user = db.relationship("MarketplaceUser", back_populates="marketplace")

