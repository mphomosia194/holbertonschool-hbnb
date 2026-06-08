from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import fields

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

from app.services import facade

api = Namespace(
    "users",
    description="User operations"
)

user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True)
    }
)


@api.route("/")
class UserList(Resource):

    @jwt_required()
    @api.expect(user_model, validate=True)
    def post(self):

        claims = get_jwt()

        if not claims.get("is_admin"):
            return {
                "error":
                "Admin privileges required"
            }, 403

        data = api.payload

        existing = facade.get_user_by_email(
            data["email"]
        )

        if existing:
            return {
                "error":
                "Email already registered"
            }, 400

        user = facade.create_user(data)

        return {
            "id": user.id,
            "message":
            "User created successfully"
        }, 201

    def get(self):

        users = facade.get_all_users()

        return [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
            for user in users
        ], 200


@api.route("/<user_id>")
class UserResource(Resource):

    def get(self, user_id):

        user = facade.get_user(user_id)

        if not user:
            return {
                "error":
                "User not found"
            }, 404

        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, 200

    @jwt_required()
    def put(self, user_id):

        claims = get_jwt()

        if not claims.get("is_admin"):
            return {
                "error":
                "Admin privileges required"
            }, 403

        data = api.payload

        email = data.get("email")

        if email:
            existing = facade.get_user_by_email(
                email
            )

            if (
                existing and
                existing.id != user_id
            ):
                return {
                    "error":
                    "Email already in use"
                }, 400

        user = facade.update_user(
            user_id,
            data
        )

        if not user:
            return {
                "error":
                "User not found"
            }, 404

        return {
            "message":
            "User updated successfully"
        }, 200
