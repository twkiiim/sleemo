import pytest
from sleemo.framework import Sleemo, get_appsync_framework

def test_get_appsync_framework():
    sleemo = get_appsync_framework(resolver_path='/')
    
    assert sleemo is not None
    isinstance(sleemo, Sleemo)