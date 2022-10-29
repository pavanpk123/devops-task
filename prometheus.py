from pyexpat import model
from urllib.robotparser import RequestRate
from flask import Flask, request, jsonify, url_for
from flask_mongoengine import MongoEngine
import json
from healthcheck import HealthCheck
import pytest
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
health = HealthCheck()
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

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

def test_name():
    client = app.test_client()
    url = '/user/'
    response = client.get(url)
    assert response.get_data() == b'Welcome'



@app.route('/user/id/', methods=['GET'])
def get_user():
    user = User.objects()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user)


def test_name():
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.get_data() == b'Welcome'


@app.route('/user/id/', methods=['POST'])
def add_user():
    record = json.loads(request.data)
    user = User(name=record['name'],
                branch=record['branch'],
                age=record["age"])
    user.save()
    return jsonify(user)


@app.route('/user/id/', methods=['PUT'])
def Update_user(id):
    record = json.loads(request.data)
    user = User.objects.get_or_404(id=id)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(name=record['name'],
                    branch=record['branch'],
                    age=record["age"])
    return jsonify(user)

@app.route('/user/id/', methods=['DELETE'])
def delete_user(id):
    user = User.objects(id=id)
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user)


app.add_url_rule('/healthcheck','healthcheck',view_func=lambda: health.run())

if __name__=="__main__":
	app.run(debug=True)