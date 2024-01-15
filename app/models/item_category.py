from ..database import db

class ItemCategory(db.Model):

    __tablename__ = 'ItemCategory'
    item_id = db.Column(db.BigInteger, db.ForeignKey('Item.id'), primary_key=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('Category.id'), primary_key=True)

    # relationships
    item = db.relationship('Item', backref=db.backref('item_categories', cascade='all, delete-orphan'))
    category = db.relationship('Category', backref=db.backref('item_categories', cascade='all, delete-orphan'))
