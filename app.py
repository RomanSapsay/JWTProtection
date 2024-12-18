from flask import Flask, jsonify, request
from db import db
from flask_smorest import Api
from resources.item import blp  # зміна з item_blp на blp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.config['API_TITLE'] = 'My Flask API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT Settings
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  #JWT Secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)  #JWT Token expiration date

db.init_app(app)

#JWT Initialisation
jwt = JWTManager(app)
revoked_tokens = set()

# JWT Error managing
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

#JWT tokens check
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  #JWT identifier
    return jti in revoked_tokens

#Login for JWT
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "admin" or password != "adminpassword":
        return jsonify({"msg": "Bad username or password"}), 401
    
    # JWT with 30 days generation
    access_token = create_access_token(identity=username, expires_delta=timedelta(days=30))
    return jsonify(access_token=access_token)

#Logout: JWT drop current token
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return jsonify({"message": "Successfully logged out."}), 200

#Endpoint to check revoked tokens
@app.route("/revoke", methods=["POST"])
@jwt_required()
def revoke():
    jti = get_jwt()["jti"]
    if jti in revoked_tokens:
        return jsonify({"message": "This token has already been revoked."}), 400
    
    revoked_tokens.add(jti)
    return jsonify({"message": "Token revoked successfully."}), 200

# Flask-Smorest initialisation
api = Api(app)
api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(debug=True)
