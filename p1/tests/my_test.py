import os
import pymongo
import redis
import time
import unittest
from mock import MagicMock
from src.service import Service
from app import app
from src.controller import Controller
from src.mongo_repository import MongoRepository
from src.redis_repository import RedisRepository


class TestingServiceUnit(unittest.TestCase):
    def setUp(self):
        self.cache = MagicMock()
        self.database = MagicMock()
        self.service = Service(self.database, self.cache, MagicMock())

    def test_get_not_calls_mongo(self):
        key = 'key'
        self.cache.get_file.return_value = 'Not None'

        self.service.get_file(key)

        self.database.get_file.assert_not_called()

    def test_get_calls_mongo(self):
        key = 'key'
        self.cache.get_file.return_value = None

        self.service.get_file(key)

        self.database.get_file.assert_called_with(key)

    def test_get_existing_file_ret_200(self):
        key = 'key'
        self.cache.get_file.return_value = 'Not None'

        response_repr, status_code = self.service.get_file(key)

        self.assertEqual(200, status_code)

    def test_get_non_existing_file_ret_404(self):
        key = 'key'
        self.cache.get_file.return_value = None
        self.database.get_file.return_value = None

        response_repr, status_code = self.service.get_file(key)

        self.assertEqual(404, status_code)


class TestingResponses(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.logger = MagicMock()
        self.service = MagicMock()
        self.controller = Controller(logger=self.logger)
        self.service.get_file.return_value = ('Message', 200)
        self.service.save_file.return_value = ('Message', 201)
        self.service.delete_file.return_value = ('Message', 204)
        app.config['controller'] = self.controller
        app.config['service'] = self.service

        self.app = app.test_client()

        self.assertEqual(app.debug, False)

    def test_delete_returns_204(self):
        response = self.app.delete('/storage/1', follow_redirects=True)

        self.assertEqual(204, response.status_code)

    def test_correct_put_returns_201(self):
        response = self.app.put('/storage/1', content_type='application/json',
                                data=b'"{\'\\"key\\":\\"key\\", \\"value\\":\\"value\\"}\'"', follow_redirects=True)
        self.assertEqual(201, response.status_code)

    def test_incorrect_put_returns_400(self):
        response = self.app.put('/storage/1', content_type='application/json',
                                data=b'{"lalal"', follow_redirects=True)
        self.assertEqual(400, response.status_code)


class TestingIntegrationCache(unittest.TestCase):
    def setUp(self):
        os.system('docker run --rm --detach --name redis-test --publish 6379:6379 redis')
        time.sleep(5)
        redis_c = redis.Redis(host='0.0.0.0', port=6379, decode_responses=True)
        self.redis_repository = RedisRepository(redis_c)

    def test_get_returns_value_from_cache(self):
        self.redis_repository.put_file('key', 'value')
        value = self.redis_repository.get_file('key')

        self.assertEqual('value', value)

    def tearDown(self):
        os.system('docker stop redis-test')


class TestingIntegrationDatabase(unittest.TestCase):
    def setUp(self):
        os.system('docker run --rm --detach --name mongo-test --publish 27017:27017 mongo')
        time.sleep(5)
        mongo_c = pymongo.MongoClient(host='0.0.0.0', port=27017)
        self.mongo_repository = MongoRepository(mongo_c['hw10']['files'])

    def test_get_returns_value_from_cache(self):
        self.mongo_repository.put_file('file_name', {})
        file_body = self.mongo_repository.get_file('file_name')

        self.assertEqual('{}', file_body)

    def tearDown(self):
        os.system('docker stop mongo-test')