import datetime
from flask import Flask
from flask import request, jsonify, Response
import json
from pymongo import MongoClient
import logging
import os

app = Flask(__name__)

country_id = 0
city_id = 0
temp_id = 0
uri = "mongodb://root:toor@mongo:27017/"
client = MongoClient(uri)
db = client['tema2']

@app.route('/api/countries', methods = ["GET"])
def get_countries():

    collections = db.list_collection_names()

    return jsonify({'status':collections}), 200

# @app.route('/api/countries', methods = ["POST"])
# def add_country():
#     payload = request.get_json(silent=True)
#     if len(payload) != 3:
#         return jsonify({'status':'not enaugh arguments'}), 400
#     if ('nume' not in payload or
#         'lat' not in payload or
#         'lon' not in payload):
#         return jsonify({'status':'wrong arguments'}), 400
#     if (not isinstance(payload['nume'], str) or
#         not isinstance(payload['lat'], float) or
#         not isinstance(payload['lon'], float)):
#         return jsonify({'status':'wrong types'}), 400
    
#     country_id += 1
#     db['country'].insert_one({'id': country_id, 'nume': payload['nume'], 'lat': payload['lat'], 'lon': payload['lon']})
#     return jsonify({'id': country_id}), 200


# @app.route('/api/countries/<int:numar>', methods = ["PUT"])
# def modify_country(numar):
#     return jsonify({'status':'ok modify country'}), 200

# @app.route('/api/countries/<int:numar>', methods = ["DELETE"])
# def rm_country(numar):
#     return jsonify({'status':'ok rm country'}), 200

# @app.route('/api/cities', methods = ["POST"])
# def add_city():
#     return jsonify({'status':'ok add city'}), 200

# @app.route('/api/cities', methods = ["GET"])
# def get_cities():
#     return jsonify({'status':'ok get cities'}), 200

# @app.route('/api/cities/country/<int:id>', methods = ["GET"])
# def get_cities_country(id):
#     return jsonify({'status':'ok get cities country'}), 200

# @app.route('/api/cities/<int:id>', methods = ["PUT"])
# def change_city():
#     return jsonify({'status':'ok change city'}), 200

# @app.route('/api/cities/<int:id>', methods = ["DELETE"])
# def rm_city():
#     return jsonify({'status':'ok rm city'}), 200

# @app.route('/api/temperatures', methods = ["POST"])
# def add_temp():
#     return jsonify({'status':'ok add temp'}), 200

# @app.route('/api/temperatures', methods = ["GET"])
# def get_precise_temp():
#     lat = request.args.get('lat', type=float)
#     lon = request.args.get('lon', type=float)
#     date_from = request.args.get('from', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#     date_until = request.args.get('until', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#     return jsonify({'status':'ok get precise temp'}), 200

# @app.route('/api/temperatures/<int:id>', methods = ["GET"])
# def get_city_temp_interval(id):
#     date_from = request.args.get('from', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#     date_until = request.args.get('until', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#     return jsonify({'status':'ok get city interval temp'}), 200

# @app.route('/api/temperatures/countries/<int:id>', methods = ["GET"])
# def get_country_temp_interval(id):
#     date_from = request.args.get('from', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#     date_until = request.args.get('until', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#     return jsonify({'status':'ok get country interval temp'}), 200

# @app.route('/api/temperatures/<int:id>', methods = ["PUT"])
# def change_temp(id):
#     return jsonify({'status':'ok change temp'}), 200

# @app.route('/api/temperatures', methods = ["DELETE"])
# def delete_temp():
#     return jsonify({'status':'ok delete temp'}), 200

def init_db():

    collections = db.list_collection_names()

    if 'country' not in collections:
        db.create_collection('country')
    if 'city' not in collections:
        db.create_collection('city')
    if 'temperature' not in collections:
        db.create_collection('temperature')

if __name__ == '__main__':
    init_db()
    app.run('0.0.0.0', debug=True, port=3000)

