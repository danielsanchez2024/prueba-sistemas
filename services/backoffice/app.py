from flask import Flask, request, jsonify
from pymongo import MongoClient
from redis import Redis
from elasticsearch import Elasticsearch
from config import config

app = Flask(__name__)

config_mongo = config["mongo"]
config_redis = config["redis"]
config_es = config["elasticsearch"]

mongo_client = MongoClient(
    host=config_mongo["host"],
    port=int(config_mongo["port"]),
    username=config_mongo["username"],
    password=config_mongo["password"]
)
mongo_db = mongo_client[config_mongo["database"]]


redis_client = Redis(host=config_redis["host"], port=int(config_redis["port"]), decode_responses=True)

es_client = Elasticsearch([{
    'host': config_es["host"],
    'port': int(config_es["port"]),
    'scheme': config_es["scheme"]
}])

#MONGO
@app.route('/mongo/user', methods=['GET'])
def get_mongo_users():
    users_collection = mongo_db["users"]
    users = list(users_collection.find({}, {'_id': 0}))
    return jsonify(users)

@app.route('/mongo/user', methods=['POST'])
def add_mongo_user():
    users_collection = mongo_db["users"] 
    data = request.json
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    user = {
        'username': data['username'],
        'email': data['email'],
        'password': data['password']
    }
    users_collection.insert_one(user) 

    return jsonify({'status': 'Usuario agregado a MongoDB'}), 201

#REDIS
@app.route('/redis/user', methods=['GET'])
def get_redis_users():
    users = {}
    keys = redis_client.keys("user:*")  

    for key in keys:
        key_str = key.decode("utf-8") if isinstance(key, bytes) else key  # Asegurar formato de clave
        key_type = redis_client.type(key_str)

        if key_type == b'hash' or key_type == "hash":  # Si es un hash, obtener todos sus valores
            user_data = redis_client.hgetall(key_str)
            users[key_str] = { 
                (k.decode("utf-8") if isinstance(k, bytes) else k): 
                (v.decode("utf-8") if isinstance(v, bytes) else v) 
                for k, v in user_data.items() 
            }  
        elif key_type == b'string' or key_type == "string":  
            value = redis_client.get(key_str)
            users[key_str] = value.decode("utf-8") if isinstance(value, bytes) else value
        else:
            users[key_str] = f"[Tipo de dato no compatible: {key_type if isinstance(key_type, str) else key_type.decode('utf-8')}]"

    if users:
        return jsonify(users), 200
    else:
        return jsonify({"error": "No hay usuarios en Redis"}), 404  # Se retorna directamente en un solo return




@app.route('/redis/user', methods=['POST'])
def insert_redis_user():
    data = request.json
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    user_key = f"user:{data['username']}"

    redis_client.hset(user_key, mapping={
        'username': data['username'],
        'email': data['email'],
        'password': data['password'] 
    })

    return jsonify({'message': 'Usuario insertado en Redis'}), 201

#ELASTICSEARCH
@app.route('/elasticsearch/user', methods=['GET'])
def get_elasticsearch_users():
    results = es_client.search(
        index=config_es["index"],
        body={"query": {"match_all": {}}}
    )
    users = [hit["_source"] for hit in results['hits']['hits']]

    return (jsonify(users), 200) if users else (jsonify({"error": "No hay usuarios en Elasticsearch"}), 404)

@app.route('/elasticsearch/user', methods=['POST'])
def insert_elasticsearch_user():
    data = request.json
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    user_doc = {
        'username': data['username'],
        'email': data['email'],
        'password': data['password']  
    }

    es_client.index(index="user", body=user_doc)

    return jsonify({'message': 'Usuario insertado en Elasticsearch'}), 201

@ app.route('/livez')
def livez():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    config_app = config["app"]
    app.run(debug=True, host=config_app["host"], port=int(config_app["port"]))