import json,logging,inspect,functools

class ApiError(Exception):
    def __init__(self,error,data='',message=''):
        super(ApiError,self).__init__(message)
        self.error=error
        self.data=data
        self.message=message


class APIValueError(ApiError):
    def __init__(self,field,message):
        super(APIValueError,self).__init__('ValueError',field,message)


class APINotFoundError(ApiError):
    def __init__(self,field,message):
        super(APINotFoundError,self).__init__('NotFoundError',field,message)

class ApripermissionError(ApiError):
    def __init__(self,message):
        super(ApripermissionError,self).__init__('Forbidden','permission',message)
