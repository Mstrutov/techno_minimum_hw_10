

class Service:
    def __init__(self, mongo_table, redis_cache, logger):
        self.mongo_repository = mongo_table
        self.redis_repository = redis_cache
        self.logger = logger

    def get_file(self, file_name):
        self.logger.debug('get from cache key [%s]', file_name)
        requested_file = self.redis_repository.get_file(file_name)

        if requested_file is None:
            self.logger.warning('key [%s] not found in cache', file_name)
            self.logger.debug('get from database key [%s]', file_name)
            requested_file = self.mongo_repository.get_file(file_name)
            if requested_file is not None:
                self.redis_repository.put_file(file_name, requested_file)

        if requested_file is not None:
            return requested_file + '\r\n', 200
        else:
            self.logger.error('key [%s] not found in database', file_name)
            return 'File not found\r\n', 404

    def save_file(self, file_name, file_body):
        self.mongo_repository.put_file(file_name, file_body)
        return 'File saved\r\n', 201

    def delete_file(self, file_name):
        self.redis_repository.delete_file(file_name)
        self.mongo_repository.delete_file(file_name)
        return 'File deleted\r\n', 204



