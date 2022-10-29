from pyexpat import model
from urllib.robotparser import RequestRate
from flask import Flask, request, jsonify, url_for
from flask_mongoengine import MongoEngine
import json
from healthcheck import HealthCheck
import pytest

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

@app.route("/user/")
def root_path():
  return("Welcome")

def test_names():
    client = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.get_data() == b'Welcome'

@app.route('/user/id/', methods=['GET'])
def get_user():
  workers = Workers.objects()
  if not workers:
    return jsonify({'error': 'data not found'})
  else:
    return jsonify(workers)

def test_name():
    client = app.test_client()
    url = '/user/id/'
    response = client.get(url)
    assert response.status_code == 200

@app.route('/user/id/', methods=['POST'])
def add_user():
  record = json.loads(request.data)
  workers = Workers(Names=record["Names"],
        Work=record["Work"],
        WorkerId=record["WorkerId"])
  workers.save()
  return jsonify(workers)

def test_status():
    client = app.test_client()
    url = '/user/id'
    response = client.get(url)
    assert response.status_code == 308

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

app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())
if __name__ == "__main__":
  app.run(debug=True)
