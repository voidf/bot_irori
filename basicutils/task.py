from io import BytesIO
import sys
import argparse
from typing import Union
from loguru import logger

class ArgumentParser(argparse.ArgumentParser):    
    def _get_action_from_name(self, name):
        """Given a name, get the Action instance registered with this parser.
        If only it were made available in the ArgumentError object. It is 
        passed as it's first arg...
        """
        container = self._actions
        if name is None:
            return None
        for action in container:
            if '/'.join(action.option_strings) == name:
                return action
            elif action.metavar == name:
                return action
            elif action.dest == name:
                return action
    def error(self, message):
        raise argparse.ArgumentError(None, message)
        # exc = sys.exc_info()[1]
        # print('====>', exc)
        # if exc:
            # exc.argument = self._get_action_from_name(exc.argument_name)
            # raise exc
        # super(ArgumentParser, self).error(message)
try:
    from cfg import dist_host, web_port, internal_host
except ImportError:
    logger.warning('<dist_host> or <web_port> or <internal_host> not found, using http://localhost:1234 instead')
    dist_host, web_port, internal_host = 'http://localhost', 1234, 'http://localhost'
    
def server_api(relative_path: str) -> str:
    return f"{dist_host}:{web_port}{relative_path}"

def internal_api(relative_path: str) -> str:
    return f"{internal_host}:{web_port}{relative_path}"


# def convert_to_amrb(typ: str, content: bytes):
#     ret = requests.post(
#         server_api(f'/convert/amr?format={typ}&mode=0'),
#         data={'lnk': lnk}
#     ).json()['url']
#     return server_api('/worker/oss/'+ret)