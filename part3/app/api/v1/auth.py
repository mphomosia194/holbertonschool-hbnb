from flask_restx import Namespace
from flask_restx import Resource
from flask_restx import fields

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from app.services import facade

api = Namespace(
    "auth",
    description="Authentication operations"
)

login_model = api.model(
    "Login",
    {
        "email": fields.String(
            required=True,
            description="User email"
        ),
        "password": fields.String(
            required=True,
            description="User password"
        )
    }
)


@api.route("/login")
class Login(Resource):

    @api.expect(login_model, validate=True)
    def post(self):
        """
        Authenticate user and return JWT
        """

        credentials = api.payload

        user = facade.get_user_by_email(
            credentials["email"]
        )

        if (
            not user or
            not user.verify_password(
                credentials["password"]
            )
        ):
            return {
                "error":
                "Invalid credentials"
            }, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "is_admin": user.is_admin
            }
        )

        return {
            "access_token":
            access_token
        }, 200


@api.route("/protected")
class Protected(Resource):

    @jwt_required()
    def get(self):

        current_user = get_jwt_identity()

        claims = get_jwt()

        return {
            "message":
            f"Hello user {current_user}",
            "is_admin":
            claims["is_admin"]
        }, 200
