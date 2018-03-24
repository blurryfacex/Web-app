import json,logging,inspect,functools

class APIError(Exception):
    def __init__(self,error,data='',message=''):
        super(APIError,self).__init__(message)
        self.error=error
        self.data=data
        self.message=message


class APIValueError(APIError):
    def __init__(self,field,message=''):
        super(APIValueError,self).__init__('ValueError',field,message)


class APINotFoundError(APIError):
    def __init__(self,field,message=''):
        super(APINotFoundError,self).__init__('NotFoundError',field,message)

class APIPermissionError(APIError):
    def __init__(self,message):
        super(APIPermissionError,self).__init__('Forbidden','permission',message)
