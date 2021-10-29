from flask import Flask,request,abort,jsonify
from flask_bcrypt import Bcrypt
from config import ApplicationConfig
from models import db,User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config.from_object(ApplicationConfig)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "kwehhehojowoojow"  # Change this!
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/register", methods= ["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exist = User.query.filter_by(email = email).first() is not None

    if user_exist:
        abort(409)

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.email)

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "adm": new_user.adm,
        "token": access_token
    })

########################################################
@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    #session["user_id"] = user.id

    access_token = create_access_token(identity=user.email)

    return jsonify({
        "id": user.id,
        "email": user.email,
        "adm": user.adm,
        "token": access_token
    })

##################################################

####################################################
@app.route('/delete',methods=['DELETE'])       #
def delete_article():                            #
    le = request.json["id"]
    lo = int(le)
    article = User.query.filter(id= lo)
    db.session.delete(article)
    db.session.commit()
    dictionary = {
        "message": "all done"
    }
    return jsonify(dictionary), 200


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    dictionary = {
        "message":"almost there"
    }
    return jsonify(dictionary), 200

if __name__ == '__main__':
    app.run(debug=True)