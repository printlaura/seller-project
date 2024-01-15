from ..database import db
from sqlalchemy import CheckConstraint


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
