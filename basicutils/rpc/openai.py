import hashlib
import random
import json
import http
from typing import List
import urllib
import requests
from basicutils.rpc.translate import Baidu
from loguru import logger

class OpenAI:
    api_key = None

    @classmethod
    def get_cred(cls):
        if cls.api_key is None:
            from fapi.models.Auth import IroriConfig
            cfg = IroriConfig.objects().first()
            cls.api_key = cfg.api_keys['openaikey']
        return cls.api_key

    @classmethod
    def chat(cls, prompt: str, translate=True) -> List[str]:
        k = cls.get_cred()
        if translate:
            prompt = Baidu.trans('zh', 'en', prompt)
            logger.debug(f'translated: {prompt}')
        r = requests.post("https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + k
            },
            json={
                "model": "text-davinci-003",
                "prompt": prompt, 
                "temperature": 60, 
                "max_tokens": 4000
            }
        )
        choices = []
        for i in r.json()['choices']:
            choices.append(i['text'].strip())
            if translate:
                logger.debug(f'before translation: {choices[-1]}')
                choices[-1] = Baidu.trans('en', 'zh', choices[-1])
        return choices

        
