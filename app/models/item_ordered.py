from ..database import db
from sqlalchemy import CheckConstraint


class ItemOrdered(db.Model):
    __tablename__ = 'ItemOrdered'
    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey('SalesOrder.id'))
    item_id = db.Column(db.BigInteger, db.ForeignKey('Item.id'))
    quantity = db.Column(db.Integer)

    # relationships
    sales_order = db.relationship("SalesOrder")
    item = db.relationship("Item")
