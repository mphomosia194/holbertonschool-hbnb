from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import facade

api = Namespace(
    "places",
    description="Place operations"
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True),
        "description": fields.String(required=True),
        "price": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True)
    }
)


@api.route("/")
class PlaceList(Resource):

    def get(self):
        places = facade.get_all_places()

        return [
            {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner_id
            }
            for place in places
        ], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):

        data = api.payload

        data["owner_id"] = get_jwt_identity()

        place = facade.create_place(data)

        return {
            "id": place.id,
            "message": "Place created successfully"
        }, 201


@api.route("/<place_id>")
class PlaceResource(Resource):

    def get(self, place_id):

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id
        }, 200

    @jwt_required()
    def put(self, place_id):

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        current_user = get_jwt_identity()

        if place.owner_id != current_user:
            return {"error": "Unauthorized action"}, 403

        facade.update_place(
            place_id,
            api.payload
        )

        return {
            "message": "Place updated successfully"
        }, 200
