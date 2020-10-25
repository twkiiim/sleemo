import functools
import os

sleemo = None

class Sleemo(object):
    resolver_path = None
    operations = []

    def __init__(self, **kwargs):
        # os.environ('DYNAMODB_TABLE_NAME')

        for key, value in kwargs.items():
            if key == 'resolver_path':
                print('resolver_path: {}'.format(value))
                self.resolver_path = value

            if key == 'operations':
                print('operations: {}'.format(operations))
                self.operations = value
        
        if self.resolver_path is None:
            raise Exception('resolver_path is not specified when initializing Sleemo. Put resolver_path when you getting the appsync framework.')

        if len(self.operations) == 0:
            print('default operations applied - all the python files under "{}/" will be registered as resolvers'.format(self.resolver_path))
            files = os.listdir(self.resolver_path)
            self.operations = [ f.replace('.py', '') for f in files ]

        self.logger = None

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