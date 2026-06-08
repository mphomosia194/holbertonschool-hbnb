import re

from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(
        self,
        first_name,
        last_name,
        email,
        is_admin=False
    ):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.validate()

    def validate(self):
        if not isinstance(self.first_name, str) or not self.first_name.strip():
            raise ValueError("first_name is required")

        if len(self.first_name) > 50:
            raise ValueError("first_name must not exceed 50 characters")

        if not isinstance(self.last_name, str) or not self.last_name.strip():
            raise ValueError("last_name is required")

        if len(self.last_name) > 50:
            raise ValueError("last_name must not exceed 50 characters")

        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("email is required")

        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"

        if not re.match(email_pattern, self.email):
            raise ValueError("invalid email format")
