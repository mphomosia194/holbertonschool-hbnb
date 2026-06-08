from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner
    ):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

        self.validate()

    def validate(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title is required")

        if len(self.title) > 100:
            raise ValueError("title must not exceed 100 characters")

        if not isinstance(self.price, (int, float)):
            raise ValueError("price must be numeric")

        if self.price <= 0:
            raise ValueError("price must be positive")

        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("latitude must be between -90 and 90")

        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("longitude must be between -180 and 180")

        if not isinstance(self.owner, User):
            raise ValueError("owner must be a User instance")

    def add_review(self, review):
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")

        self.amenities.append(amenity)
        self.save()
