from ..database import db
from sqlalchemy import CheckConstraint


class City(db.Model):
    __tablename__ = 'City'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    country_id = db.Column(db.BigInteger, db.ForeignKey('Country.id', onupdate="CASCADE", ondelete="SET NULL"), nullable=False)

    # relationships
    country = db.relationship("Country", back_populates="cities")
