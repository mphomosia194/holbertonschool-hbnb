from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model(
    'Amenity',
    {
        'name': fields.String(
            required=True,
            description='Name of the amenity'
        )
    }
)


@api.route('/')
class AmenityList(Resource):

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""

        amenity_data = api.payload

        try:
            amenity = facade.create_amenity(
                amenity_data
            )

            return {
                'id': amenity.id,
                'name': amenity.name
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(
        200,
        'List of amenities retrieved successfully'
    )
    def get(self):
        """Retrieve all amenities"""

        amenities = facade.get_all_amenities()

        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    @api.response(
        200,
        'Amenity details retrieved successfully'
    )
    @api.response(
        404,
        'Amenity not found'
    )
    def get(self, amenity_id):
        """Retrieve amenity by ID"""

        amenity = facade.get_amenity(
            amenity_id
        )

        if not amenity:
            return {
                'error': 'Amenity not found'
            }, 404

        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(
        200,
        'Amenity updated successfully'
    )
    @api.response(
        404,
        'Amenity not found'
    )
    @api.response(
        400,
        'Invalid input data'
    )
    def put(self, amenity_id):
        """Update amenity"""

        amenity = facade.get_amenity(
            amenity_id
        )

        if not amenity:
            return {
                'error': 'Amenity not found'
            }, 404

        try:
            updated_amenity = facade.update_amenity(
                amenity_id,
                api.payload
            )

            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
