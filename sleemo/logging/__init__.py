import json
import logging
import os
import uuid
from typing import Dict


class JsonFormatter(logging.Formatter):
    """JSON log formatter."""

    def format(self, record):   # type: ignore
        """Format log record to JSON."""
        ret = {}
        for attr, value in record.__dict__.items():
            if attr == 'created':
                value = self.formatTime(record)
            if attr == 'exc_info' and value is not None:
                value = self.formatException(value)
            if attr == 'stack_info' and value is not None:
                value = self.formatStack(value)
            if attr == 'msg':
                if not isinstance(value, dict):
                    value = str(value)
            ret[attr] = value
        return json.dumps(ret)


class ContextLogger(logging.Logger):
    """Sleemo default logger."""

    def __init__(self, *args, **kwargs):    # type: ignore
        super(ContextLogger, self).__init__(*args, **kwargs)
        self.context = {
            'aws_region': os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION'),
            'function_name': os.environ.get('AWS_LAMBDA_FUNCTION_NAME'),
            'function_version': os.environ.get('AWS_LAMBDA_FUNCTION_VERSION'),
            'function_memory_size': os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE'),
            'log_group_name': os.environ.get('AWS_LAMBDA_LOG_GROUP_NAME'),
            'log_stream_name': os.environ.get('AWS_LAMBDA_LOG_STREAM_NAME')
        }

    def update_context(self, attrs: Dict) -> None:
        """
        Inject addtional infomation to logs.

        Usage::
            >>> from sleemo.framework import get_appsync_framework
            >>> sleemo = get_appsync_framework()
            >>> sleemo.logger.update_context(
            >>>     {
            >>>         "attribute1": "value1",
            >>>         "attribute2": "value2",
            >>>         "attribute3": "value3"
            >>>     }
            >>> )
        """
        self.context.update(attrs)

    def makeRecord(self, *args, **kwargs):  # type: ignore
        record = super(ContextLogger, self).makeRecord(*args, **kwargs)
        for k, v in self.context.items():
            setattr(record, k, v)
        return record


def generate_correlation_id() -> str:
    """Generate correlation id."""
    return str(uuid.uuid4())
