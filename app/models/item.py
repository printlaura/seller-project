from ..database import db
from sqlalchemy import CheckConstraint


class Item(db.Model):
    __tablename__ = 'Item'
    id = db.Column(db.BigInteger, primary_key=True)
    product_title = db.Column(db.String, CheckConstraint('LENGTH(product_title) >= 3 OR product_title IS NULL'))
    brand_id = db.Column(db.BigInteger, db.ForeignKey('Brand.id', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('Category.id', onupdate="CASCADE", ondelete="SET NULL"), nullable=False)
    country_of_sales_id = db.Column(db.BigInteger, db.ForeignKey('Country.id', onupdate="CASCADE", ondelete="SET NULL"))
    unit_price_local_currency = db.Column(db.Float, nullable=False)
    sales_margin = db.Column(db.Float, CheckConstraint('sales_margin > -1 and sales_margin < 1'))
    launched_at = db.Column(db.Date, CheckConstraint('launched_at <= CURRENT_DATE'))
    size = db.Column(db.String, CheckConstraint("size IN ('S', 'M', 'L', 'XL')"), nullable=False)
    item_type = db.Column(db.String, CheckConstraint("item_type IN ('A', 'B', 'C', 'D')"))
    in_stock = db.Column(db.Boolean, nullable=False)

    # relationships
    brand = db.relationship("Brand", back_populates="items")
    country_of_sales = db.relationship("Country", back_populates="items")
    categories = db.relationship('Category', secondary='ItemCategory',
                                 backref=db.backref('items', lazy='dynamic'))

