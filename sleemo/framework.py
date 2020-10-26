import functools
import os

sleemo = None

class Sleemo(object):
    __resolver_path = None
    __operations = None
    __logger = None

    def __init__(self, **kwargs):
        self.set_options(**kwargs)

    def set_options(self, **kwargs):
        # os.environ('DYNAMODB_TABLE_NAME')
        for key, value in kwargs.items():
            if key == 'resolver_path':
                self.__set_resolver_path(value)
            
            if key == 'logger':
                raise Exception('logger option not implemented yet')
    
    def __set_resolver_path(self, resolver_path):
        if type(resolver_path) != type(''):
            raise Exception('resolver_path must be string type')
    
        print('resolver_path: {}'.format(resolver_path))
        self.__resolver_path = resolver_path
        self.__register_opertaions()

    def __register_opertaions(self):
        try:
            if self.__resolver_path:
                files = os.listdir(self.__resolver_path)
                self.__operations = [ f.replace('.py', '') for f in files ]
                print('Python files under "{}/" directory has been registered as GraphQL resolvers'.format(self.__resolver_path))
            else:
                raise Exception('No resolver_path has been set.')
        except Exception as e:
            raise Exception('An exception occurred while registering GraphQL operations, given resolver_path: "{}"'.format(self.__resolver_path))

    def get_resolver_path(self):
        return self.__resolver_path

    def get_operations(self):
        return self.__operations

    def default_gateway(self):
        def _gateway(func, **kwargs):
            @functools.wraps(func)
            def wrapper(event, context):
                print('before default gateway lambda - should log some useful information')
                print(event)
                ret = func(event, context)
                print(ret)
                print('after default gateway lambda - should log some useful information')
                return ret
            return wrapper
        return _gateway

    def resolve(self, event):
        resolver = None

        for op in self.__operations:
            if op == event['info']['fieldName']:
                import sys
                sys.path.append(self.__resolver_path)

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