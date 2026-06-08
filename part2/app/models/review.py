from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(
        self,
        text,
        rating,
        place,
        user
    ):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        self.validate()

    def validate(self):
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("text is required")

        if not isinstance(self.rating, int):
            raise ValueError("rating must be an integer")

        if self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.place, Place):
            raise ValueError("place must be a Place instance")

        if not isinstance(self.user, User):
            raise ValueError("user must be a User instance")
