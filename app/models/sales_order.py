from ..database import db
from sqlalchemy import CheckConstraint


class SalesOrder(db.Model):
    __tablename__ = 'SalesOrder'
    id = db.Column(db.BigInteger, primary_key=True)
    buyer_id = db.Column(db.BigInteger, db.ForeignKey('Buyer.id'))
    shipping_country_id = db.Column(db.BigInteger, db.ForeignKey('Country.id'))
    shipping_city_id = db.Column(db.BigInteger, db.ForeignKey('City.id'))
    marketplace_id = db.Column(db.BigInteger, db.ForeignKey('Marketplace.id'))
    order_date = db.Column(db.Date)
    total_amount = db.Column(db.Float)

    # relationships
    buyer = db.relationship("Buyer", back_populates="sales_order")
    shipping_city = db.relationship("City")
    shipping_country = db.relationship("Country")
    marketplace = db.relationship("Marketplace")
