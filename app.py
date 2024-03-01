"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify
from models import connet_db, Cupcake, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connet_db(app)

@app.route('/')
def root():
  """Render homepage"""

  return render_template("index.html")

@app.route('/api/cupcakes')
def list_cupcakes():
  """List all cupcakes"""
  all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
  return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def specific_cupcake_info(cupcake_id):
  """show information on a specific cupcake"""
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():

  print(request.json)
  new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"] or None)
  db.session.add(new_cupcake)
  db.session.commit()

  response_json = jsonify(cupcake=new_cupcake.serialize())
  return (response_json,201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
  """updating cupcake"""
  cupcake = Cupcake.query.get_or_404(cupcake_id)

  cupcake.flavor = request.json.get("flavor", cupcake.flavor)
  cupcake.size = request.json.get("size", cupcake.size)
  cupcake.rating = request.json.get("rating", cupcake.rating)
  cupcake.image = request.json.get("image", cupcake.image)

  db.session.commit()

  return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
  """Deletes cupcake"""
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  
  db.session.delete(cupcake)
  db.session.commit()

  return jsonify(message="Deleted")
