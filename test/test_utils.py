import uuid
from sleemo.utils import AppSyncTypeUtils, get_type_utils


def test_get_type_utils():
    type_utils = get_type_utils()
    
    assert type_utils is not None
    isinstance(type_utils, AppSyncTypeUtils)

def test_get_type_utils_with_timezone_offset():
    timezone_offset = 9
    type_utils = get_type_utils(timezone_offset=timezone_offset)

    assert type_utils.timezone_offset == timezone_offset

def test_createUUID():
    type_utils = get_type_utils()
    id = type_utils.createUUID()
    
    assert type(id) == type(str(uuid.uuid4()))
    assert len(id) == len(str(uuid.uuid4()))
