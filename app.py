#!/usr/bin/python3
from flask import Flask
from flask import request
import json 
import os
import sys
import subprocess
import datetime
import redis
import pymongo

app = Flask(__name__)


class Controller:
    def check_request_validity(self, request):
        # is get_json idempotent??
        if request.method == 'PUT' and request.get_json(silent=True) is None:
            return False
        else:
            return True


class Service:
    def __init__(self, repository):
        self.repository = repository

    def process_request(self, request, file_name):
        if request.method == 'GET':
            got_file = self.repository.get_file(file_name)
            if got_file is not None:
                return got_file + '\r\n', 200
            else:
                return 'File not found\r\n', 404
        elif request.method == 'PUT':
            self.repository.put_file(file_name, request.get_json(silent=True))
            return 'File saved\r\n', 201
        elif request.method == 'DELETE':
            self.repository.delete_file(file_name)
            return 'File deleted\r\n', 204


class Repository:
    def __init__(self, redis_client, mongo_table):
        self.cache = redis_client
        self.table = mongo_table

    def get_file_from_cache(self, file_name):
        return self.cache.get(file_name)

    def get_file_from_db(self, file_name):
        found_file = self.table.find_one({'file_name': file_name})
        self.cache.set(found_file['file_name'], json.dumps(found_file['file_body']))
        return json.dumps(found_file['file_body'])

    def get_file(self, file_name):
        if self.cache.exists(file_name):
            return self.get_file_from_cache(file_name)
        elif self.table.find_one({'file_name': file_name}) is not None:
            return self.get_file_from_db(file_name)
        else:
            return None

    def delete_file(self, file_name):
        self.cache.delete(file_name)
        self.table.delete_many({'file_name': file_name})

    def put_file(self, file_name, file_body):
        self.table.insert_one({'file_name': file_name, 'file_body': file_body})


def log_request(request):
    with open('/var/log/server.log', 'a') as log_storage:
        log_storage.write('GOT REQUEST AT: ' + str(datetime.datetime.now()) + '\r\n')
        log_storage.write(str(request.method) + ' ' + str(request.url) + '\r\n')
        log_storage.write(str(request.headers))
        log_storage.write(request.get_data().decode() + '\r\n\r\n')


@app.route('/storage/<file_name>', methods=['GET', 'PUT', 'DELETE'])
def get_file(file_name):
    log_request(request)
    if controller.check_request_validity(request):
        return service.process_request(request, file_name)
    else:
        return 'Wrong file format\r\n', 400


if __name__ == '__main__':
    try:
        os.makedirs('/var/log')
    except:
        pass

    if os.geteuid() != 0:
        subprocess.call(['sudo', 'python3', *sys.argv])
        sys.exit()

    redis_c = redis.Redis(host='0.0.0.0', port=6379, decode_responses=True)
    mongo_c = pymongo.MongoClient(host='0.0.0.0', port=27017)

    repository = Repository(redis_c, mongo_c['hw9']['files'])
    service = Service(repository)
    controller = Controller()

    app.run(port=8080, host='0.0.0.0')
