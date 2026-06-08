from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model(
    'Place',
    {
        'title': fields.String(
            required=True,
            description='Place title'
        ),
        'description': fields.String(
            required=False,
            description='Place description'
        ),
        'price': fields.Float(
            required=True,
            description='Price per night'
        ),
        'latitude': fields.Float(
            required=True,
            description='Latitude'
        ),
        'longitude': fields.Float(
            required=True,
            description='Longitude'
        ),
        'owner_id': fields.String(
            required=True,
            description='Owner ID'
        ),
        'amenity_ids': fields.List(
            fields.String,
            required=False,
            description='List of amenity IDs'
        )
    }
)


@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""

        try:
            place = facade.create_place(
                api.payload
            )

            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(
        200,
        'List of places retrieved successfully'
    )
    def get(self):
        """Retrieve all places"""

        places = facade.get_all_places()

        return [
            {
                'id': place.id,
                'title': place.title,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude
            }
            for place in places
        ], 200


@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(
        200,
        'Place details retrieved successfully'
    )
    @api.response(
        404,
        'Place not found'
    )
    def get(self, place_id):
        """Retrieve place by ID"""

        place = facade.get_place(place_id)

        if not place:
            return {
                'error': 'Place not found'
            }, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {
                    'id': amenity.id,
                    'name': amenity.name
                }
                for amenity in place.amenities
            ]
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(
        200,
        'Place updated successfully'
    )
    @api.response(
        404,
        'Place not found'
    )
    @api.response(
        400,
        'Invalid input data'
    )
    def put(self, place_id):
        """Update place"""

        try:
            place = facade.update_place(
                place_id,
                api.payload
            )

            if not place:
                return {
                    'error': 'Place not found'
                }, 404

            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):

    @api.response(
        200,
        'List of reviews for the place retrieved successfully'
    )
    @api.response(
        404,
        'Place not found'
    )
    def get(self, place_id):
        """Get reviews for a place"""

        reviews = facade.get_reviews_by_place(
            place_id
        )

        if reviews is None:
            return {
                'error': 'Place not found'
            }, 404

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id
            }
            for review in reviews
        ], 200
