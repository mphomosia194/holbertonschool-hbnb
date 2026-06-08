from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model(
    'Review',
    {
        'text': fields.String(
            required=True,
            description='Review text'
        ),
        'rating': fields.Integer(
            required=True,
            description='Rating 1-5'
        ),
        'user_id': fields.String(
            required=True,
            description='User ID'
        ),
        'place_id': fields.String(
            required=True,
            description='Place ID'
        )
    }
)


@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create review"""

        try:
            review = facade.create_review(
                api.payload
            )

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(
        200,
        'List of reviews retrieved successfully'
    )
    def get(self):
        """Get all reviews"""

        reviews = facade.get_all_reviews()

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            }
            for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(
        200,
        'Review details retrieved successfully'
    )
    @api.response(
        404,
        'Review not found'
    )
    def get(self, review_id):
        """Get review by ID"""

        review = facade.get_review(review_id)

        if not review:
            return {
                'error': 'Review not found'
            }, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(
        200,
        'Review updated successfully'
    )
    @api.response(
        404,
        'Review not found'
    )
    def put(self, review_id):
        """Update review"""

        try:
            review = facade.update_review(
                review_id,
                api.payload
            )

            if not review:
                return {
                    'error': 'Review not found'
                }, 404

            return {
                'message': 'Review updated successfully'
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(
        200,
        'Review deleted successfully'
    )
    @api.response(
        404,
        'Review not found'
    )
    def delete(self, review_id):
        """Delete review"""

        deleted = facade.delete_review(
            review_id
        )

        if not deleted:
            return {
                'error': 'Review not found'
            }, 404

        return {
            'message': 'Review deleted successfully'
        }, 200
