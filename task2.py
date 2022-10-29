from pyexpat import model
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import json
from healthcheck import HealthCheck
app = Flask(__name__)
health = HealthCheck()
app.config['MONGODB_SETTINGS'] = {
  'db': 'student',
  'host': 'localhost',
  'port': 27017
}
db = MongoEngine()
db.init_app(app)
class Workers(db.Document):
  Names = db.StringField()
  Work = db.StringField()
  WorkerId = db.IntField()
  def to_json(self):
    return {"Names": self.Names,
        "Work": self.Work,
        "WorkerId" : self.WorkerId}
@app.route("/")
def root_path():
  return("Welcome")
@app.route('/user/id/', methods=['GET'])
def get_user():
  workers = Workers.objects()
  if not workers:
    return jsonify({'error': 'data not found'})
  else:
    return jsonify(workers)

@app.route('/user/id/', methods=['POST'])
def add_user():
  record = json.loads(request.data)
  workers = Workers(Names=record["Names"],
        Work=record["Work"],
        WorkerId=record["WorkerId"])
  workers.save()
  return jsonify(workers)
@app.route('/user/<id>', methods=['PUT'])
def Update_user(id):
  record = json.loads(request.data)
  workers = Workers.objects.get_or_404(id=id)
  if not workers:
    return jsonify({'error': 'data not found'})
  else:
    workers.update(Names=record['Names'],
          Work=record['Work'],
          WorkerId=record["WorkerId"])
  return jsonify(workers)
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  workers = Workers.objects(id=id)
  if not workers:
    return jsonify({'error': 'data not found'})
  else:
    workers.delete()
  return jsonify(workers.to_json())

class Batch(db.Document):
  Names = db.StringField()
  Course = db.StringField()
  def to_json(self):
    return {"Names": self.Names,
        "Course": self.Course,}
@app.route('/batch/', methods=['GET'])
def get_batch():
  print('1')
  batch1 = Batch.objects()
  if not batch1:
    return jsonify({'error': 'data not found'})
  else:
    return jsonify(batch1)
@app.route('/batch/', methods=['POST'])
def add_batch():
  record = json.loads(request.data)
  batch1 = Batch(Names=record['Names'],
        Course=record['Course'])
  batch1.save()
  return jsonify(batch1)

@app.route('/batch/<id>', methods=['PUT'])
def put_batch():
  record = json.loads(request.data)
  batch1 = Batch(Names=record['Names'],
        Course=record['Course'])
  batch1.save()
  return jsonify(batch1)

@app.route('/batch/<id>', methods=['DELETE'])
def delete_batch():
  record = json.loads(request.data)
  batch1 = Batch(Names=record['Names'],
        Course=record['Course'])
  batch1.save()
  return jsonify(batch1)
  
app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())
if __name__ == "__main__":
  app.run(debug=True)