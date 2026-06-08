from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.validate()

    def validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name is required")

        if len(self.name) > 50:
            raise ValueError("name must not exceed 50 characters")
