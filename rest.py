import datetime
from flask import Flask
from flask import request, jsonify, Response
import json
from pymongo import MongoClient, ASCENDING
import logging
import os

app = Flask(__name__)



uri = "mongodb://root:toor@localhost:27017/"
client = MongoClient(uri)
db = client['tema2']

def verify_duplicate_country(name):
    country = db['country'].find_one({'nume': name})
    if country is not None:
        return True
    return False

@app.route('/api/countries', methods = ["POST"])
def add_country():
    payload = request.get_json(silent=True)
    if len(payload) != 3:
        return jsonify({'status':'wrong number of arguments'}), 400
    if ('nume' not in payload or
        'lat' not in payload or
        'lon' not in payload):
        return jsonify({'status':'wrong arguments'}), 400
    if (not isinstance(payload['nume'], str) or
        not isinstance(payload['lat'], float) or
        not isinstance(payload['lon'], float)):
        return jsonify({'status':'wrong types'}), 400
    
    if verify_duplicate_country(payload['nume']):
        return jsonify({'status':'duplicate country'}), 409

    result = db['country'].insert_one({'nume': payload['nume'], 'lat': payload['lat'], 'lon': payload['lon']})
    print(result.inserted_id)
    return jsonify({'id': str(result.inserted_id)}), 201

# @app.route('/api/countries', methods = ["GET"])
# def get_countries():

#     collections = db.list_collection_names()

#     return jsonify({'status':collections}), 200

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
    country_collection = db['country']
    country_collection.create_index([('id', ASCENDING)], unique=False)
    
    # if 'city' not in collections:
    #     db.create_collection('city')
    # if 'temperature' not in collections:
    #     db.create_collection('temperature')
    
    # city_collection = db['city']
    # city_collection.create_index([('id', ASCENDING)], unique=True)
    # temperature_collection = db['temperature']
    # temperature_collection.create_index([('id', ASCENDING)], unique=True)

if __name__ == '__main__':
    init_db()
    app.run('0.0.0.0', debug=True, port=3000)

