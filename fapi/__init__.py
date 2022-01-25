from fastapi import HTTPException


def trueReturn(data=None, msg=""):
    return {
        'data': data,
        'msg': msg,
        'status': True
    }


def falseReturn(code=500, msg="", data=None):
    raise HTTPException(code, {
        'data': data,
        'msg': msg,
        'status': False
    })
