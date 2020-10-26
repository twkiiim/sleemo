from sleemo.utils import AppSyncTypeUtils, get_appsync_type_utils

def test_get_appsync_type_utils():
    utils = get_appsync_type_utils()
    
    assert utils is not None
    isinstance(utils, AppSyncTypeUtils)

def test_get_appsync_type_utils_with_timezone_offset():
    timezone_offset = 9
    utils = get_appsync_type_utils(timezone_offset=timezone_offset)

    assert utils is not None
    isinstance(utils, AppSyncTypeUtils)
    assert utils.get_timezone_offset() == timezone_offset

def test_utils_set_options_with_timezone_offset():
    utils = get_appsync_type_utils()
    timezone_offset = 9
    utils.set_options(timezone_offset=timezone_offset)
    
    assert utils.get_timezone_offset() == timezone_offset


def test_createUUID():
    utils = get_appsync_type_utils()
    uuid = utils.createUUID()
    
    assert type(uuid) == type('')

def test_createAWSDateTime():
    utils = get_appsync_type_utils(timezone_offset=0)
    t = utils.createAWSDateTime()

    assert type(t) == type('')
    