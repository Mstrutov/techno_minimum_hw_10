#!/usr/bin/python3
from flask import Flask
from flask import request
import logging.config
import os
import pymongo
import redis
import sys
import subprocess
from service import Service
from controller import Controller
from redis_repository import RedisRepository
from mongo_repository import MongoRepository

app = Flask(__name__)


@app.route('/storage/<file_name>', methods=['GET', 'PUT', 'DELETE'])
def get_file(file_name):
    if controller.check_request_validity(request):
        if request.method == 'GET':
            return service.get_file(file_name)
        elif request.method == 'PUT':
            return service.save_file(file_name, request.get_json(silent=True))
        elif request.method == 'DELETE':
            return service.delete_file(file_name)
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
    controller = Controller(logger)

    app.run(port=8080, host='0.0.0.0')
