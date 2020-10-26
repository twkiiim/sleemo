import uuid
from sleemo.utils import get_appsync_type_utils

utils = get_appsync_type_utils()


def test_get_appsync_type_utils():
    utils = get_appsync_type_utils()
    assert utils is not None

def test_createID():
    id = utils.createID()
    assert id is not None
    assert type(id) == type('')
    assert len(id) == len(str(uuid.uuid4()))

def test_createcreateAWSDateTime():
    pass
