import pytest
from sleemo.framework import Sleemo, get_appsync_framework

def test_get_appsync_framework():
    sleemo = get_appsync_framework()
    
    assert sleemo is not None
    isinstance(sleemo, Sleemo)

def test_get_appsync_framework_with_resolver_path():
    resolver_path = '/'
    sleemo = get_appsync_framework(resolver_path=resolver_path)
    
    assert sleemo is not None
    isinstance(sleemo, Sleemo)
    assert sleemo.get_resolver_path() == resolver_path

def test_sleemo_set_options_with_resolver_path():
    resolver_path = '/'
    sleemo = get_appsync_framework()
    sleemo.set_options(resolver_path=resolver_path)

    assert sleemo is not None
    isinstance(sleemo, Sleemo)
    assert sleemo.get_resolver_path() == resolver_path

