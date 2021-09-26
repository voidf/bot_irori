from io import BytesIO
import sys
import argparse
from typing import Union
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

from cfg import dist_host, web_port
def server_api(relative_path: str) -> str:
    return f"{dist_host}:{web_port}{relative_path}"

import requests
def convert_to_amr(typ: str, lnk: Union[bytes, str], mode: int=0):
    if isinstance(lnk, str):
        ret = requests.post(
            server_api(f'/convert/amr?format={typ}&mode={mode}'),
            data={'lnk': lnk}
        ).json()['url']
    else:
        ret = requests.post(
            server_api(f'/convert/amr?format={typ}&mode={mode}'),
            files={'f': BytesIO(lnk)}
        ).json()['url']
    return server_api('/worker/oss/'+ret)

def convert_file_to_amr(typ: str, fp, mode: int=0):
    ret = requests.post(
        server_api(f'/convert/amr?format={typ}&mode={mode}'),
        files={'f': open(fp,'rb')}
    ).json()['url']
    return server_api('/worker/oss/'+ret)
import base64
from PIL import Image as PImage
def pimg_base64(img: PImage.Image) -> str:
    bio = BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    return base64.b64encode(bio.read()).decode('utf-8')
# def convert_to_amrb(typ: str, content: bytes):
#     ret = requests.post(
#         server_api(f'/convert/amr?format={typ}&mode=0'),
#         data={'lnk': lnk}
#     ).json()['url']
#     return server_api('/worker/oss/'+ret)