import datetime
from bson import ObjectId
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

def verify_duplicate(name, collection):
    country = db[collection].find_one({'nume': name})
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
        not (isinstance(payload['lat'], float) or isinstance(payload['lat'], int)) or
        not (isinstance(payload['lon'], int) or isinstance(payload['lon'], float))):
        return jsonify({'status':'wrong types'}), 400
    
    if verify_duplicate(payload['nume'], "country"):
        return jsonify({'status':'duplicate country'}), 409

    result = db['country'].insert_one({'nume': payload['nume'], 'lat': payload['lat'], 'lon': payload['lon']})
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/api/countries', methods = ["GET"])
def get_countries():

    countries = []
    for country in db['country'].find():
        country['_id'] = str(country['_id'])
        c = {"id":str(country['_id']),
            "nume":country['nume'],
            "lat":country['lat'],
            "lon":country['lon']}
        countries.append(c)
    return countries, 200

@app.route('/api/countries/<id>', methods = ["PUT"])
def modify_country(id):

    ok = False
    for country in db['country'].find():
        if str(country['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'country not found'}), 404

    payload = request.get_json(silent=True)    
    if len(payload) != 4:
        return jsonify({'status':'wrong number of arguments'}), 400
    if ('id' not in payload or
        'nume' not in payload or
        'lat' not in payload or
        'lon' not in payload):
        return jsonify({'status':'wrong arguments'}), 400
    if (not isinstance(payload['id'], str) or
        not isinstance(payload['nume'], str) or
        not (isinstance(payload['lat'], float) or isinstance(payload['lat'], int)) or
        not (isinstance(payload['lon'], int) or isinstance(payload['lon'], float))):
        return jsonify({'status':'wrong types'}), 400
    if str(payload['id']) != id:
        return jsonify({'status':'wrong id'}), 409
    
    filter = {'_id': ObjectId(id)} 
    db['country'].update_one(filter, {'$set': {'nume': payload['nume'], 'lat': payload['lat'], 'lon': payload['lon']}})

    return jsonify({'status':'ok'}), 200

@app.route('/api/countries/<id>', methods = ["DELETE"])
def rm_country(id):
    ok = False
    for country in db['country'].find():
        if str(country['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'country not found'}), 404
    
    filter = {'_id': ObjectId(id)}
    db['country'].delete_one(filter)

    return jsonify({'status':'ok'}), 200

@app.route('/api/cities', methods = ["POST"])
def add_city():

    # {idTara: Int, nume: Str, lat: Double, lon: Double}
    payload = request.get_json(silent=True)

    if len(payload) != 4:
        return jsonify({'status':'wrong number of arguments'}), 400
    if ('idTara' not in payload or
        'nume' not in payload or
        'lat' not in payload or
        'lon' not in payload):
        return jsonify({'status':'wrong arguments'}), 400
    if (not isinstance(payload['nume'], str) or
        not (isinstance(payload['lat'], float) or isinstance(payload['lat'], int)) or
        not (isinstance(payload['lon'], int) or isinstance(payload['lon'], float))):
        return jsonify({'status':'wrong types'}), 400

    id = payload['idTara']
    ok = False
    for country in db['country'].find():
        if str(country['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'country not found'}), 404

    if verify_duplicate(payload['nume'], "city"):
        return jsonify({'status':'duplicate city'}), 409

    result = db['city'].insert_one({'idTara': id, 'nume': payload['nume'], 'lat': payload['lat'], 'lon': payload['lon']})
    return jsonify({'id':str(result.inserted_id)}), 201

@app.route('/api/cities', methods = ["GET"])
def get_cities():

    cities = []
    for city in db['city'].find():
        city['_id'] = str(city['_id'])
        c = {"id":str(city['_id']),
            "idTara":str(city['idTara']),
            "nume":city['nume'],
            "lat":city['lat'],
            "lon":city['lon']}
        cities.append(c)
    return cities, 200

@app.route('/api/cities/country/<id>', methods = ["GET"])
def get_cities_country(id):

    ok = False
    for country in db['country'].find():
        if str(country['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'country not found'}), 404
    
    cities = []
    for city in db['city'].find():
        if str(city['idTara']) == id:
            city['_id'] = str(city['_id'])
            c = {"id":str(city['_id']),
                "idTara":str(city['idTara']),
                "nume":city['nume'],
                "lat":city['lat'],
                "lon":city['lon']}
            cities.append(c)
    return cities, 200

@app.route('/api/cities/<id>', methods = ["PUT"])
def change_city(id):

    ok = False
    for city in db['city'].find():
        if str(city['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'city not found'}), 404
    
    payload = request.get_json(silent=True)    
    if len(payload) != 5:
        return jsonify({'status':'wrong number of arguments'}), 400
    if ('id' not in payload or
        'idTara' not in payload or
        'nume' not in payload or
        'lat' not in payload or
        'lon' not in payload):
        return jsonify({'status':'wrong arguments'}), 400
    if (not isinstance(payload['nume'], str) or
        not (isinstance(payload['lat'], float) or isinstance(payload['lat'], int)) or
        not (isinstance(payload['lon'], int) or isinstance(payload['lon'], float))):
        return jsonify({'status':'wrong types'}), 400
    if str(payload['id']) != id:
        return jsonify({'status':'wrong id'}), 409
    
    ok = False
    for country in db['country'].find():
        if str(country['_id']) == payload['idTara']:
            ok = True
            break
    if not ok:
        return jsonify({'status':'country not found'}), 404

    filter = {'_id': ObjectId(id)} 
    db['city'].update_one(filter, {'$set': {'idTara':payload['idTara'], 'nume': payload['nume'], 'lat': payload['lat'], 'lon': payload['lon']}})

    return jsonify({'status':'ok'}), 200

@app.route('/api/cities/<id>', methods = ["DELETE"])
def rm_city(id):

    ok = False
    for city in db['city'].find():
        if str(city['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'city not found'}), 404
    
    filter = {'_id': ObjectId(id)}
    db['city'].delete_one(filter)

    return jsonify({'status':'ok'}), 200

@app.route('/api/temperatures', methods = ["POST"])
def add_temp():

    payload = request.get_json(silent=True)
    if len(payload) != 2:
        return jsonify({'status':'wrong number of arguments'}), 400
    if ('idOras' not in payload or
        'valoare' not in payload):
        return jsonify({'status':'wrong arguments'}), 400
    if (not (isinstance(payload['valoare'], float) or isinstance(payload['valoare'], int))):
        return jsonify({'status':'wrong types'}), 400

    id = payload['idOras']
    ok = False
    for city in db['city'].find():
        if str(city['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'city not found'}), 404
    
    timestamp = datetime.datetime.now()
    result = db['temperature'].insert_one({"idOras": payload['idOras'], "valoare": payload['valoare'], "timestamp": timestamp})
    return jsonify({'id': str(result.inserted_id)}), 201

# def get_all_temps():
#     temperatures = []
#     for temp in db['temperature'].find():
#         temp['_id'] = str(temp['_id'])
#         t = {"id":str(temp['_id']),
#             "idOras":str(temp['idOras']),
#             "valoare":temp['valoare'],
#             "timestamp":temp['timestamp']}
#         temperatures.append(t)
#     return temperatures

# def get_temp(type: str, lat: float, lon: float, date_from: datetime, date_until: datetime):
    
#     if type is None:
            

        

# @app.route('/api/temperatures', methods = ["GET"])
# def get_precise_temp():
#     lat = request.args.get('lat', type=float)
#     lon = request.args.get('lon', type=float)
#     date_from = request.args.get('from', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
#     date_until = request.args.get('until', type=lambda d: datetime.strptime(d, '%Y-%m-%d'))
    
    
#     res = get_temp(None, lat, lon, date_from, date_until)
#     if res == 0:
#         return jsonify({'status':'no data'}), 404
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

@app.route('/api/temperatures/<id>', methods = ["PUT"])
def change_temp(id):

    ok = False
    for temp in db['temperature'].find():
        if str(temp['_id']) == id:
            ok = True
            time_id = temp['timestamp']
            break
    if not ok:
        return jsonify({'status':'temp not found'}), 404

    payload = request.get_json(silent=True)
    if len(payload) != 3:
        return jsonify({'status':'wrong number of arguments'}), 400
    if ('id' not in payload or
        'idOras' not in payload or
        'valoare' not in payload):
        return jsonify({'status':'wrong arguments'}), 400
    if (not (isinstance(payload['valoare'], float) or isinstance(payload['valoare'], int))):
        return jsonify({'status':'wrong types'}), 400
    if str(payload['id']) != id:
        return jsonify({'status':'wrong id'}), 409

    idc = payload['idOras'] 
    ok = False
    for city in db['city'].find():
        if str(city['_id']) == idc:
            ok = True
            break
    if not ok:
        return jsonify({'status':'city not found'}), 404

    filter = {'_id': ObjectId(id)}
    db['temperature'].update_one(filter, {'$set': {'idOras': payload['idOras'], 'valoare': payload['valoare']}})

    return jsonify({'status':'ok'}), 200

@app.route('/api/temperatures/<id>', methods = ["DELETE"])
def delete_temp(id):
    ok = False
    for temp in db['temperature'].find():
        if str(temp['_id']) == id:
            ok = True
            break
    if not ok:
        return jsonify({'status':'city not found'}), 404
    
    filter = {'_id': ObjectId(id)}
    db['city'].delete_one(filter)

    return jsonify({'status':'ok'}), 200



def init_db():

    collections = db.list_collection_names()

    if 'country' not in collections:
        db.create_collection('country')
    country_collection = db['country']
    country_collection.create_index([('id', ASCENDING)], unique=False)
    
    if 'city' not in collections:
        db.create_collection('city')
    city_collection = db['city']
    city_collection.create_index([('id', ASCENDING)], unique=False)

    if 'temperature' not in collections:
        db.create_collection('temperature')    
    temperature_collection = db['temperature']
    temperature_collection.create_index([('id', ASCENDING)], unique=False)

if __name__ == '__main__':
    init_db()
    app.run('0.0.0.0', debug=True, port=3000)

