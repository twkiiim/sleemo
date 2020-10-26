import datetime
import pytz
import uuid

utils = None

class AppSyncTypeUtils(object):
    __timezone_offset = 0

    def __init__(self, **kwargs):
        self.set_options(**kwargs)
    
    def set_options(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'timezone_offset':
                self.__set_timezone_offset(value)
    
    def __set_timezone_offset(self, timezone_offset):
        if type(timezone_offset) != type(0):
            raise Exception('timezone_offset must be integer type')

        self.__timezone_offset = timezone_offset

    def get_timezone_offset(self):
        return self.__timezone_offset

    def createUUID(self):
        return str(uuid.uuid4())
        
    
    def createAWSDateTime(self):
        time_fmt = '%Y-%m-%dT%H:%M:%S'
        
        if self.__timezone_offset == 0:
            time_fmt += 'Z'
        else:
            time_fmt += '+' if self.__timezone_offset > 0 else '-'
            time_fmt += str(abs(self.__timezone_offset)).zfill(2)
            time_fmt += ':00:00'
        
        now = datetime.datetime.utcnow()
        now = now + datetime.timedelta(hours=self.__timezone_offset)
        return now.strftime(time_fmt)

    def getAWSDateTime(self, value):
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')

def get_appsync_type_utils(**kwargs: dict):
    global utils

    if utils is None or len(kwargs) > 0:
        utils = AppSyncTypeUtils(**kwargs)
    
    return utils