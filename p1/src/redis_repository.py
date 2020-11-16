class RedisRepository:
    def __init__(self, redis_client):
        self.cache = redis_client

    def get_file(self, file_name):
        return self.cache.get(file_name)

    def delete_file(self, file_name):
        self.cache.delete(file_name)

    def put_file(self, file_name, file_body):
        self.cache.set(file_name, file_body)