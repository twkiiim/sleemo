import datetime
import time
import pytz
import uuid

type_utils = None

class AppSyncTypeUtils(object):

    def __init__(
        self, 
        timezone_offset: int = 0
    ):
        self.timezone_offset = timezone_offset
    
    def createUUID(self):
        return str(uuid.uuid4())

    def createAWSDate(self):
        fmt = '%Y-%m-%d'

        if self.timezone_offset == 0:
            fmt += 'Z'
        else:
            fmt += '+' if self.timezone_offset > 0 else '-'
            fmt += str(abs(self.timezone_offset)).zfill(2)
            fmt += ':00:00'

        now = datetime.datetime.utcnow().date()
        now = now + datetime.timedelta(hours=self.timezone_offset)
        return now.strftime(fmt)
    
    def createAWSTime(self):
        fmt = '%H:%M:%S'

        if self.timezone_offset == 0:
            fmt += 'Z'
        else:
            fmt += '+' if self.timezone_offset > 0 else '-'
            fmt += str(abs(self.timezone_offset)).zfill(2)
            fmt += ':00:00'

        now = datetime.datetime.utcnow().time()
        now = now + datetime.timedelta(hours=self.timezone_offset)
        return now.strftime(fmt)

    def createAWSDateTime(self):
        fmt = '%Y-%m-%dT%H:%M:%S'

        if self.timezone_offset == 0:
            fmt += 'Z'
        else:
            fmt += '+' if self.timezone_offset > 0 else '-'
            fmt += str(abs(self.timezone_offset)).zfill(2)
            fmt += ':00:00'

        now = datetime.datetime.utcnow()
        now = now + datetime.timedelta(hours=self.timezone_offset)
        return now.strftime(fmt)

    def createAWSTimestamp(self):
        return time.time()

    # def createAWSJSON(self):
    #     pass


def get_type_utils(**kwargs: dict):
    global type_utils

    if type_utils is None or len(kwargs) > 0:
        type_utils = AppSyncTypeUtils(**kwargs)
    
    return type_utils