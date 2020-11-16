import json


class MongoRepository:
    def __init__(self, mongo_table):
        self.table = mongo_table

    def get_file(self, file_name):
        found_file = self.table.find_one({'file_name': file_name})
        if found_file is None:
            return None
        return json.dumps(found_file['file_body'])

    def delete_file(self, file_name):
        self.table.delete_many({'file_name': file_name})

    def put_file(self, file_name, file_body):
        self.table.insert_one({'file_name': file_name, 'file_body': file_body})