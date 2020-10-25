import datetime
import pytz
import uuid

utils = None

class AppSyncTypeUtils(object):

    def __init__(self):
        pass

    def createID(self):
        """ TODO
        - id type should be configured on the init phase (default is UUID)
        """
        return str(uuid.uuid4())
        
    
    def createAWSDateTime(self):
        """ TODO
        - local timezone parameter : this should be configured on the init phase
        """
        # local_tz = pytz.timezone('Asia/Tokyo')
        # now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz).strftime('%Y-%m-%dT%H:%M:%SZ')
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        return now

    def getAWSDateTime(self, value):
        """ TODO
        - type checking
        - utc checking and return value according to the timezone (+-, etc)
        """
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')

def get_appsync_type_utils():
    global utils

    if utils is None:
        utils = AppSyncTypeUtils()
    
    return utils