#!/usr/bin/python3
from flask import Flask
from flask import request
import logging.config
import os
import pymongo
import redis
import sys
import subprocess
from src.service import Service
from src.controller import Controller
from src.redis_repository import RedisRepository
from src.mongo_repository import MongoRepository

app = Flask(__name__)


@app.route('/storage/<file_name>', methods=['GET', 'PUT', 'DELETE'])
def get_file(file_name):
    if app.config['controller'].check_request_validity(request):
        if request.method == 'GET':
            return app.config['service'].get_file(file_name)
        elif request.method == 'PUT':
            return app.config['service'].save_file(file_name, request.get_json(silent=True))
        elif request.method == 'DELETE':
            return app.config['service'].delete_file(file_name)
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

    logging.config.fileConfig('/file-server/logging.conf')
    logger = logging.getLogger('root')

    mongo_repository = MongoRepository(mongo_c['hw9']['files'])
    redis_repository = RedisRepository(redis_c)
    service = Service(mongo_repository, redis_repository, logger)
    app.config['service'] = service
    controller = Controller(logger)
    app.config['controller'] = controller
    app.run(port=8080, host='0.0.0.0')
