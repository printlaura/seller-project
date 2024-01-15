from sqlalchemy import CheckConstraint
from ..database import db


class Brand(db.Model):
    __tablename__ = 'Brand'
    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    brand_manager_id = db.Column(db.BigInteger, db.ForeignKey('BrandManager.id', onupdate="CASCADE", ondelete="SET NULL"))
    acquired_at = db.Column(db.Date, CheckConstraint('acquired_at <= CURRENT_DATE'), nullable=False)

    # relationships
    brand_manager = db.relationship("BrandManager", back_populates="brands")
    items = db.relationship("Item", back_populates="brand")
