from flask import Flask
from flask import request, jsonify, Response
import json

app = Flask(__name__)
filme = []

@app.route('/movie/<int:numar>', methods = ["GET"])
def get_movie(numar):
    for film in filme:
        if film["id"] == numar:
            return film
    return jsonify({'status':'not found'}), 404

@app.route('/movie/<int:numar>', methods = ["PUT"])
def put_movie(numar):
    payload = request.get_json(silent=True)
    for film in filme:
        if film["id"] == numar:
            film["nume"] = payload["nume"]
            return jsonify({'status':'ok'}), 200
    return jsonify({'status':'not found'}), 404

@app.route('/movie/<int:numar>', methods = ["DELETE"])
def del_movie(numar):
    for film in filme:
        if film["id"] == numar:
            filme.remove(film)
            return jsonify({'status':'ok'}), 200
    return jsonify({'status':'not found'}), 404

@app.route('/movies', methods=["GET"])
def movies():
    return filme

@app.route('/movies', methods=["POST"])
def add_movies():
    payload = request.get_json(silent=True)

    if not payload:
        return Response(status=400)
    
    for film in filme:
        if film["nume"] == payload["nume"]:
            return jsonify({'status':'already exists'}), 202
    
    if len(filme) == 0:
        id = 1
    else:
        id = filme[len(filme) - 1]["id"] + 1
    filme.append({'id' : id, 'nume' : payload["nume"]})
    return jsonify({'status':'ok'}), 201

@app.route('/reset', methods = ["DELETE"])
def reset():
    filme.clear()
    return jsonify({'status':'ok'}), 200

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

