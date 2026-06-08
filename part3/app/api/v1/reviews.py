from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import facade

api = Namespace(
    "reviews",
    description="Review operations"
)

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True),
        "rating": fields.Integer(required=True),
        "place_id": fields.String(required=True)
    }
)


@api.route("/")
class ReviewList(Resource):

    def get(self):

        reviews = facade.get_all_reviews()

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            }
            for review in reviews
        ], 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    def post(self):

        data = api.payload

        current_user = get_jwt_identity()

        place = facade.get_place(
            data["place_id"]
        )

        if not place:
            return {
                "error": "Place not found"
            }, 404

        if place.owner_id == current_user:
            return {
                "error":
                "You cannot review your own place"
            }, 400

        existing_reviews = facade.get_reviews_by_place(
            data["place_id"]
        )

        for review in existing_reviews:
            if review.user_id == current_user:
                return {
                    "error":
                    "You have already reviewed this place"
                }, 400

        data["user_id"] = current_user

        review = facade.create_review(data)

        return {
            "id": review.id,
            "message":
            "Review created successfully"
        }, 201


@api.route("/<review_id>")
class ReviewResource(Resource):

    def get(self, review_id):

        review = facade.get_review(review_id)

        if not review:
            return {
                "error":
                "Review not found"
            }, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id
        }, 200

    @jwt_required()
    def put(self, review_id):

        review = facade.get_review(review_id)

        if not review:
            return {
                "error":
                "Review not found"
            }, 404

        current_user = get_jwt_identity()

        if review.user_id != current_user:
            return {
                "error":
                "Unauthorized action"
            }, 403

        facade.update_review(
            review_id,
            api.payload
        )

        return {
            "message":
            "Review updated successfully"
        }, 200

    @jwt_required()
    def delete(self, review_id):

        review = facade.get_review(review_id)

        if not review:
            return {
                "error":
                "Review not found"
            }, 404

        current_user = get_jwt_identity()

        if review.user_id != current_user:
            return {
                "error":
                "Unauthorized action"
            }, 403

        facade.delete_review(
            review_id
        )

        return {
            "message":
            "Review deleted successfully"
        }, 200
