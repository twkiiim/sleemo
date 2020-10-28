import pytest
import logging
from sleemo.framework import Sleemo, get_appsync_framework
from sleemo.settings import Logging


def test_logger():
    sleemo = get_appsync_framework(resolver_path='/')
    logger = sleemo.logger

    assert isinstance(logger, logging.Logger)

