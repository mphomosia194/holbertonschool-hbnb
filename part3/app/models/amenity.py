from app import db

from app.models.base_model import BaseModel


class Amenity(BaseModel):

    __tablename__ = "amenities"

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    def __init__(self, name):
        self.name = name
