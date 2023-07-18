from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
#CORS(app, support_credentials=True)

# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8081"}})

CORS(app, support_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/postgres"
db = SQLAlchemy(app)

# class Item(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(80), unique=True, nullable=False)
#   content = db.Column(db.String(120), unique=True, nullable=False)

#   def __init__(self, id, title, content):
#     self.id = id
#     self.title = title
#     self.content = content

class Bezirksgrenzen(db.Model):
  __tablename__ = 'bezirksgrenzen'
  gml_id = db.Column(db.Integer, primary_key=True)
  gemeinde_name = db.Column(db.String(), nullable=True)
  gemeindeschlÜssel = db.Column(db.Integer, nullable=True)
  land_name = db.Column(db.String(), nullable=True)
  land_schluessel = db.Column(db.Integer, nullable=True)
  schluessel_gesamt = db.Column(db.Integer, nullable=True)
  def __init__(self, gml_id, gemeinde_name, gemeindeschlÜssel,land_name, land_schluessel, schluessel_gesamt):
     self.gml_id = gml_id
     self.gemeinde_name = gemeinde_name
     self.gemeindeschlÜssel = gemeindeschlÜssel
     self.land_name = land_name
     self.land_schluessel = land_schluessel
     self.schluessel_gesamt = schluessel_gesamt

class LorPlanungsRaeume_2021(db.Model):
  __tablename__ = 'lor_planungs_raeume_2021'
  plr_id = db.Column(db.Integer, primary_key=True)
  plr_name = db.Column(db.String(), nullable=True)
  tessellate = db.Column(db.Integer, nullable=True)
  visibility = db.Column(db.Integer, nullable=True)
  #bez = db.Column(db.String(), nullable=True) # foreign key
  bez = db.Column(db.Integer, db.ForeignKey('bezirksgrenzen.gml_id'))
  bezirksgrenzen = db.relationship("Bezirksgrenzen", backref=db.backref("bezirksgrenzen", uselist=False))
  stand = db.Column(db.Date(), nullable=True)
  grÖsse_m2 = db.Column(db.Float(), nullable=True)
  
  def __init__(self, plr_id, plr_name, tessellate,visibility, bez, stand, grÖsse_m2):
     self.plr_id = plr_id
     self.plr_name = plr_name
     self.tessellate = tessellate
     self.visibility = visibility
     self.bez = bez
     self.stand = stand
     self.grÖsse_m2 = grÖsse_m2

class Fahrraddiebstahl(db.Model):
  __tablename__ = 'fahrraddiebstahl'
  fahrraddiebstahl_id  = db.Column(db.Integer, primary_key=True)
  angelegt_am = db.Column(db.Date(), nullable=True)
  tatzeit_anfang_datum = db.Column(db.Date(), nullable=True)
  tatzeit_anfang_stunde = db.Column(db.Integer, nullable=True)
  tatzeit_ende_datum = db.Column(db.Date(), nullable=True)
  tatzeit_ende_stunde = db.Column(db.Integer, nullable=True)
  lor = db.Column(db.Integer, db.ForeignKey('lor_planungs_raeume_2021.plr_id'))
  lor_planungs_raeume_2021 = db.relationship("LorPlanungsRaeume_2021", backref=db.backref("lor_planungs_raeume_2021", uselist=False))
  schadenshoehe = db.Column(db.Integer, nullable=True)
  versuch = db.Column(db.String(), nullable=True)
  art_des_fahrrads = db.Column(db.String(), nullable=True)
  delikt = db.Column(db.String(), nullable=True)
  erfassungsgrund = db.Column(db.String(), nullable=True)
  
  
  def __init__(self, fahrraddiebstahl_id, angelegt_am, tatzeit_anfang_datum,tatzeit_anfang_stunde, 
               tatzeit_ende_datum, tatzeit_ende_stunde, lor, schadenshoehe, versuch, art_des_fahrrads, delikt, erfassungsgrund):
     self.fahrraddiebstahl_id = fahrraddiebstahl_id
     self.angelegt_am = angelegt_am
     self.tatzeit_anfang_datum = tatzeit_anfang_datum
     self.tatzeit_anfang_stunde = tatzeit_anfang_stunde
     self.tatzeit_ende_datum = tatzeit_ende_datum
     self.tatzeit_ende_stunde = tatzeit_ende_stunde
     self.lor = lor
     self.schadenshoehe = schadenshoehe
     self.versuch = versuch
     self.art_des_fahrrads = art_des_fahrrads
     self.delikt = delikt
     self.erfassungsgrund = erfassungsgrund

#db.create_all()
"""
API health checker
"""
@app.route('/hello', methods=['GET'])
def say_hello():
  return "hello world"


"""
Insert data in BEZ table 
"""
@app.route('/bezirksgrenzen', methods=['POST', 'OPTIONS'])
@cross_origin(origin='*', supports_credentials=True)
def create_bezirksgrenzen_item():
  body = request.get_json()
  bez = db.session.execute(db.select(Bezirksgrenzen.gml_id).order_by(Bezirksgrenzen.gml_id.desc()).limit(1)).scalar_one()
  db.session.add(Bezirksgrenzen(bez+1, body['gemeinde_name'], body['gemeindeschlÜssel'], body["land_name"], body["land_schluessel"], body["schluessel_gesamt"]))
  db.session.commit()
  return "item created"

"""
Update Bezirksgrenzen
"""
@app.route('/bezirksgrenzen/<id>', methods=['PUT', 'OPTIONS'])
@cross_origin(origin='*', supports_credentials=True)
def update_bezirksgrenzens_item(id):
  body = request.get_json()
  db.session.query(Bezirksgrenzen).filter_by(gml_id=id).update(
    dict(gemeinde_name=body['gemeinde_name'], 
         gemeindeschlÜssel = body['gemeindeschlÜssel'], 
         land_name = body["land_name"], 
         land_schluessel = body["land_schluessel"], 
         schluessel_gesamt = body["schluessel_gesamt"]))
  db.session.commit()
  return "item updated"

"""
Get all BEZ
"""
@app.route('/bezirksgrenzens', methods=['GET', 'OPTIONS'])
@cross_origin(origin='*', supports_credentials=True)
def get_bezirksgrenzen():
  items = []
  for item in db.session.query(Bezirksgrenzen).all():
    del item.__dict__['_sa_instance_state']
    items.append(item.__dict__)
  return jsonify(items)


"""
Get BEZ by bez_id
"""
@app.route('/bezirksgrenzen/<bez_id>', methods=['GET', 'OPTIONS'])
@cross_origin(origin='*', supports_credentials=True)
def get_bezirksgrenzen_by_bez_id(bez_id):
  item = Bezirksgrenzen.query.get(bez_id)
  del item.__dict__['_sa_instance_state']
  return jsonify(item.__dict__)

"""
Get all FAHR
"""
@app.route('/fahrraddiebstahls', methods=['GET'])
def get_fahrraddiebstahl():
  items = []
  for item in db.session.query(Fahrraddiebstahl).all():
    del item.__dict__['_sa_instance_state']
    items.append(item.__dict__)
  return jsonify(items)

"""
Get FAHR by fahr_id
"""
@app.route('/fahrraddiebstahl/<fahr_id>', methods=['GET'])
def get_fahrraddiebstahl_by_fahr_id(fahr_id):
  item = Fahrraddiebstahl.query.get(fahr_id)
  del item.__dict__['_sa_instance_state']
  return jsonify(item.__dict__)

"""
Get all LOR
"""
@app.route('/lorPlanungsRaeume2021s', methods=['GET'])
def get_lorPlanungsRaeume2021():
  items = []
  for item in db.session.query(LorPlanungsRaeume_2021).all():
    del item.__dict__['_sa_instance_state']
    items.append(item.__dict__)
  return jsonify(items)


"""
Get LOR by lor_id
"""
@app.route('/lorPlanungsRaeume2021/<lor_id>', methods=['GET'])
def get_lorPlanungsRaeume2021_by_lor_id(lor_id):
  item = LorPlanungsRaeume_2021.query.get(lor_id)
  del item.__dict__['_sa_instance_state']
  return jsonify(item.__dict__)


"""
Join between BEZ and LOR
"""
@app.route('/gemeinde_name_from_lor/<lor_id>', methods=['GET'])
def get_gemeinde_name_from_lor_table(lor_id):
  lor_ref = LorPlanungsRaeume_2021.query.get(lor_id)
  result_of_join = {}
  result_of_join["lor_id"] = lor_id
  result_of_join["plr_name"] = lor_ref.plr_name
  result_of_join["gemeinde_name"] = lor_ref.bezirksgrenzen.gemeinde_name
  return jsonify(result_of_join)


"""
Join between LOR and FAHR
"""
@app.route('/plr_name_from_fahr/<fahr_id>', methods=['GET'])
def get_plr_name_from_fahr_table(fahr_id):
  fahr_ref = Fahrraddiebstahl.query.get(fahr_id)
  result_of_join = {}
  result_of_join["fahr_id"] = fahr_id
  result_of_join["art_des_fahrrads"] = fahr_ref.art_des_fahrrads
  result_of_join["plr_name"] = fahr_ref.lor_planungs_raeume_2021.plr_name
  return jsonify(result_of_join)

"""
Delete row in BEZ table by bez_id
"""
@app.route('/bezirksgrenzen/<gml_id>', methods=['DELETE'])
def delete_bezirksgrenzenid(gml_id):
  db.session.query(Bezirksgrenzen).filter_by(gml_id=gml_id).delete()
  db.session.commit()
  return "item deleted"

"""
Delete row in FAHR table by fahr_id
"""
@app.route('/fahrraddiebstahl/<fahrraddiebstahl_id>', methods=['DELETE'])
def delete_fahrraddiebstahl(fahrraddiebstahl_id):
  db.session.query(Fahrraddiebstahl).filter_by(fahrraddiebstahl_id=fahrraddiebstahl_id).delete()
  db.session.commit()
  return "item deleted"

"""
Delete row in LOR table by plr_id
"""
@app.route('/lorPlanungsRaeume2021/<plr_id>', methods=['DELETE'])
def delete_lorPlanungsRaeume2021(plr_id):
  db.session.query(LorPlanungsRaeume_2021).filter_by(plr_id=plr_id).delete()
  db.session.commit()
  return "item deleted"


# @app.route('/items/<id>', methods=['GET'])
# def get_item(id):
#   item = Item.query.get(id)
#   del item.__dict__['_sa_instance_state']
#   return jsonify(item.__dict__)

# @app.route('/items', methods=['GET'])
# def get_items():
#   items = []
#   for item in db.session.query(Item).all():
#     del item.__dict__['_sa_instance_state']
#     items.append(item.__dict__)
#   return jsonify(items)

# @app.route('/items', methods=['POST'])
# def create_item():
#   body = request.get_json()
#   db.session.add(Item(1, body['title'], body['content']))
#   db.session.commit()
#   return "item created"

# @app.route('/items/<id>', methods=['PUT'])
# def update_item(id):
#   body = request.get_json()
#   db.session.query(Item).filter_by(id=id).update(
#     dict(title=body['title'], content=body['content']))
#   db.session.commit()
#   return "item updated"

# @app.route('/items/<id>', methods=['DELETE'])
# def delete_item(id):
#   db.session.query(Item).filter_by(id=id).delete()
#   db.session.commit()
#   return "item deleted"

if __name__ == '__main__':
    app.run(debug=True)
