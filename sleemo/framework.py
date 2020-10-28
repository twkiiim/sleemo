import functools
import os

from sleemo.settings import Logging

sleemo = None

class Sleemo(object):

    def __init__(
        self, 
        resolver_path: str = None,
        logging: Logging = Logging()
    ):
        self.logger = logging.logger
        self.resolver_path = resolver_path

        try:
            if self.resolver_path:
                files = os.listdir(self.resolver_path)
                self.operations = [ f.replace('.py', '') for f in files ]
                self.logger.info('Python files under "{}/" directory has been registered as GraphQL resolvers'.format(self.resolver_path))
            else:
                raise Exception('No resolver_path has been set.')
        except Exception as e:
            raise Exception('An exception occurred while registering GraphQL operations, given resolver_path: "{}"'.format(self.resolver_path))


    def default_gateway(self):
        def _gateway(func, **kwargs):
            @functools.wraps(func)
            def wrapper(event, context):
                self.logger.info(event)
                result = func(event, context)
                self.logger.info(result)
                return result
            return wrapper
        return _gateway

    def resolve(self, event):
        resolver = None

        for op in self.operations:
            if op == event['info']['fieldName']:
                import sys
                sys.path.append(self.resolver_path)

                resolver = __import__(op)
                break

        if resolver is not None:
            kwargs = {}
            for key in event['arguments'].keys():
                kwargs[key] = event['arguments'][key]
            
            kwargs['event'] = event
            
            return getattr(resolver, op)(**kwargs)
        else:
            return { 'error': 'No matching resolver' }
            
def get_appsync_framework(**kwargs: dict) -> Sleemo:
    global sleemo

    if sleemo is None or len(kwargs) > 0:
        sleemo = Sleemo(**kwargs)
    
    return sleemo

def get_logger():
    if sleemo is None:
        raise Exception('get_appsync_framework() must be called before get_logger()')
    
    return sleemo.logger