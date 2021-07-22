import datetime

from flask import Flask
from flask import jsonify
from flask_restplus import Api
from flask_restplus import fields
from flask_restplus import Resource

from app.models.user import User
from app.utils.config_loader import load_config
from app.utils.db_connector import DBConnector
from app.utils.logger import Logger


app = Flask(__name__)
api = Api(app)

config_path = "deploy/config.yaml"
config = load_config(config_path)

logger = Logger(config["LOG_LEVEL"], config["LOG_FILE_NAME"]).logger()
logger.info("==============================================")
logger.info("=               SERVICE UP                   =")
logger.info("==============================================")
logger.info("now time is: {}".format(datetime.datetime.now()))
logger.debug('setting cfg: {}'.format(config))

db_connector = DBConnector(db_uri=config["DATABASE_URL"])
session = db_connector.session()

communicate_information_model = api.model("CommunicateInformation", {
    "email": fields.String(description="The email of user", example="charles@gmail.com", required=True),
    "mobile": fields.String(description="The mobile number of user", example="09xx-xxx-xxx", required=True),
})
user_model = api.model("User", {
    "name": fields.String(description="The name of user", example="Charles", required=True),
    "job_title": fields.String(description="The job title of user", example="SRE", required=True),
    "communicate_information": fields.Nested(communicate_information_model, description="The communicate information of user", required=True),
})


@api.route("/users")
class UserList(Resource):
    def get(self):
        try:
            users = [user.serialize()
                     for user in session.query(User).all()]
            logger.info("Get all users successfully!")

            return jsonify(users)
        except Exception as ex:
            logger.error("Get /users error: {}".format(ex))
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
            logger.info("Create a new user successfully!")

            return jsonify(user.serialize())
        except Exception as ex:
            logger.error("Post /users error: {}".format(ex))
            return jsonify("Post /users error: {}".format(ex)), 521


@ api.route("/users/<int:user_id>")
class UserInformation(Resource):
    def get(self, user_id):
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                logger.warning("Not found user! user_id: {}".format(user_id))
                return "Not found user! user_id: {}".format(user_id), 519
            logger.info("get user_id = {} successfully".format(user_id))

            return jsonify(user.serialize())
        except Exception as ex:
            logger.error("Get /users/user_id error: {}".format(ex))
            return jsonify("Get /users/user_id error: {}".format(ex)), 522

    @api.expect(user_model, validate=True)
    def put(self, user_id):
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                logger.warning("Not found user! user_id: {}".format(user_id))
                return "Not found user! user_id: {}".format(user_id), 519

            request_data = api.payload
            user.name = request_data["name"]
            user.job_title = request_data["job_title"]
            user.email = request_data["communicate_information"]["email"]
            user.mobile = request_data["communicate_information"]["mobile"]
            session.commit()
            logger.info("Update user_id = {} successfully".format(user_id))

            return jsonify(user.serialize())
        except Exception as ex:
            logger.error("Put /users/user_id error: {}".format(ex))
            return jsonify("Put /users/user_id error: {}".format(ex)), 523

    def delete(self, user_id):
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                logger.warning("Not found user! user_id: {}".format(user_id))
                return "Not found user! user_id: {}".format(user_id), 519

            session.delete(user)
            session.commit()
            logger.info("Delete user_id = {} successfully".format(user_id))

            return jsonify("Delete user successfully! user_id: {}".format(user_id))
        except Exception as ex:
            logger.error("Delete /users/user_id error: {}".format(ex))
            return jsonify("Delete /users/user_id error: {}".format(ex)), 524


if __name__ == "__main__":
    app.run(debug=config["DEBUG_MODE"])
