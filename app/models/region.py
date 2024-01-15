from ..database import db
from sqlalchemy import CheckConstraint


class Region(db.Model):
    __tablename__ = 'Region'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # relationships
    countries = db.relationship("Country", back_populates="region")
