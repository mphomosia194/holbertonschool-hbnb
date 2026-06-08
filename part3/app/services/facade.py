from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import (
    UserRepository
)

from app.persistence.repository import (
    SQLAlchemyRepository
)


class HBnBFacade:

    def __init__(self):

    self.user_repo = UserRepository()

    self.place_repo = SQLAlchemyRepository(
        Place
    )

    self.review_repo = SQLAlchemyRepository(
        Review
    )

    self.amenity_repo = SQLAlchemyRepository(
        Amenity
    )

    # ====================
    # USERS
    # ====================

    def create_user(
        self,
        user_data
    ):

        user = User(
            **user_data
        )

        self.user_repo.add(
            user
        )

        return user

    def get_user(
        self,
        user_id
    ):

        return self.user_repo.get(
            user_id
        )

    def get_all_users(self):

        return (
            self.user_repo.get_all()
        )

    def get_user_by_email(
        self,
        email
    ):

        return (
            self.user_repo
            .get_user_by_email(
                email
            )
        )

    def update_user(
        self,
        user_id,
        data
    ):

        user = self.get_user(
            user_id
        )

        if not user:
            return None

        if "password" in data:

            user.hash_password(
                data.pop(
                    "password"
                )
            )

        user.update(data)

        from app import db

        db.session.commit()

        return user

    # ====================
    # PLACES
    # ====================

    def create_place(
        self,
        data
    ):

        place = Place(**data)

        self.place_repo.add(
            place
        )

        return place

    def get_place(
        self,
        place_id
    ):

        return self.place_repo.get(
            place_id
        )

    def get_all_places(self):

        return (
            self.place_repo.get_all()
        )

    def update_place(
        self,
        place_id,
        data
    ):

        self.place_repo.update(
            place_id,
            data
        )

        return self.get_place(
            place_id
        )

    # ====================
    # REVIEWS
    # ====================

    def create_review(
        self,
        data
    ):

        review = Review(**data)

        self.review_repo.add(
            review
        )

        return review

    def get_review(
        self,
        review_id
    ):

        return self.review_repo.get(
            review_id
        )

    def get_all_reviews(self):

        return (
            self.review_repo.get_all()
        )

    def get_reviews_by_place(
        self,
        place_id
    ):

        return [
            review
            for review
            in self.review_repo.get_all()
            if review.place_id == place_id
        ]

    def update_review(
        self,
        review_id,
        data
    ):

        self.review_repo.update(
            review_id,
            data
        )

        return self.get_review(
            review_id
        )

    def delete_review(
        self,
        review_id
    ):

        self.review_repo.delete(
            review_id
        )

        return True

def create_amenity(
    self,
    data
):

    amenity = Amenity(
        **data
    )

    self.amenity_repo.add(
        amenity
    )

    return amenity


def get_amenity(
    self,
    amenity_id
):

    return self.amenity_repo.get(
        amenity_id
    )


def get_all_amenities(
    self
):

    return self.amenity_repo.get_all()


def update_amenity(
    self,
    amenity_id,
    data
):

    self.amenity_repo.update(
        amenity_id,
        data
    )

    return self.get_amenity(
        amenity_id
    )


def delete_amenity(
    self,
    amenity_id
):

    self.amenity_repo.delete(
        amenity_id
    )

    return True
