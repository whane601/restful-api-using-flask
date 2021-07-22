from flask import Flask
from flask import jsonify
from flask_restplus import Api
from flask_restplus import fields
from flask_restplus import Resource

from app.models.user import User
from app.utils.config_loader import load_config
from app.utils.db_connector import DBConnector


app = Flask(__name__)
api = Api(app)

config_path = "deploy/config.yaml"
config = load_config(config_path)

db_connector = DBConnector(db_uri=config["DATABASE_URL"])
session = db_connector.session()

communicate_information_model = api.model("CommunicateInformation", {
    "email": fields.String(description="The email of user", example="charles@gmail.com", required=True),
    "mobile": fields.String(description="The mobile number of user", example="09xx-xxx-xxx", required=True),
})
user_model = api.model("User", {
    "name": fields.String(description="The name of user", example="Charles", required=True),
    "job_title": fields.String(description="The job title of user", example="SRE", required=True),
    "communicate_information": fields.Nested(communicate_information_model),
})


@api.route("/users")
class UserList(Resource):
    def get(self):
        try:
            users = [user.serialize()
                     for user in session.query(User).all()]

            return jsonify(users)
        except Exception as ex:
            return jsonify("Get /users error: {}".format(ex)), 520

    @api.expect(user_model, validate=True)
    def post(self):
        try:
            request_data = api.payload
            user = User(
                name=request_data["name"],
                job_title=request_data["job_title"],
                email=request_data["communicate_information"]["email"],
                mobile=request_data["communicate_information"]["mobile"],
            )
            session.add(user)
            session.commit()

            return jsonify(user.serialize())
        except Exception as ex:
            return jsonify("Post /users error: {}".format(ex)), 521


@ api.route("/users/<int:user_id>")
class UserInformation(Resource):
    def get(self, user_id):
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                return "Not found user! user_id: {}".format(user_id), 519

            return jsonify(user.serialize())
        except Exception as ex:
            return jsonify("Get /users/user_id error: {}".format(ex)), 522

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                return "Not found user! user_id: {}".format(user_id), 519

            request_data = api.payload
            user.name = request_data["name"]
            user.job_title = request_data["job_title"]
            user.email = request_data["communicate_information"]["email"]
            user.mobile = request_data["communicate_information"]["mobile"]
            session.commit()

            return jsonify(user.serialize())
        except Exception as ex:
            return jsonify("Put /users/user_id error: {}".format(ex)), 523

    def delete(self, user_id):
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                return "Not found user! user_id: {}".format(user_id), 519

            session.delete(user)
            session.commit()

            return jsonify("Delete user successfully! user_id: {}".format(user_id))
        except Exception as ex:
            return jsonify("Delete /users/user_id error: {}".format(ex)), 524


if __name__ == "__main__":
    app.run(debug=config["DEBUG_MODE"])
