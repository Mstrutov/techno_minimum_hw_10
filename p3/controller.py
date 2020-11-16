#from flask import request


class Controller:
    def __init__(self, logger):
        self.logger = logger

    def request_to_str(self, request):
        result = str(request.method) + ' ' + str(request.url) + ' '
        result += str(request.headers)
        result += request.get_data().decode()

        return result

    def check_request_validity(self, request):
        self.logger.info(self.request_to_str(request))
        # is get_json idempotent??
        if request.method == 'PUT' and request.get_json(silent=True) is None:
            return False
        else:
            return True
