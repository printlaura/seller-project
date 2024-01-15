from ..database import db


class Buyer(db.Model):
    __tablename__ = 'Buyer'
    id = db.Column(db.BigInteger, primary_key=True)
    marketplace_user_id = db.Column(db.BigInteger, db.ForeignKey('MarketplaceUser.id'))
    billing_city_id = db.Column(db.BigInteger, db.ForeignKey('City.id'))
    tax_id = db.Column(db.String)

    # relationships
    user = db.relationship("MarketplaceUser", back_populates="buyers")
    billing_city = db.relationship("City")
    sales_order = db.relationship("SalesOrder")
