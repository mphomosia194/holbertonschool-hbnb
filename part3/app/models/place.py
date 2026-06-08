from app import db

from app.models.base_model import BaseModel
from app.models.place_amenity import place_amenity


class Place(BaseModel):

    __tablename__ = "places"

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    owner_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    reviews = db.relationship(
        "Review",
        backref="place",
        lazy=True,
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref(
            "places",
            lazy=True
        )
    )

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner_id
    ):
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
