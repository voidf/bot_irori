import datetime
import hashlib
import json
import traceback
import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response, File, UploadFile
from typing import Optional
from pydantic import BaseModel
from cfg import *

from jose import jwt, JWTError
from passlib.context import CryptContext

import time

auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def encrypt(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest().encode('utf-8')


def generate_jwt(user):
    token_dict = {
        'iat': time.time(),  # 1天
        'id': str(user.id)
    }
    return jwt.encode(token_dict,  # payload, 有效载体
                      jwt_token,  # 进行加密签名的密钥
                      algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                      )


def verify_jwt(token):
    try:
        payload = jwt.decode(token, jwt_token, algorithms=['HS256'])
        if payload['iat'] < time.time() - 60*60*24:
            return None, "令牌过期"
        user = User.objects(pk=payload['id']).first()
        if not user:
            return None, "无此用户"
        return user, ""
    except:
        traceback.print_exc()
        return None, "数据错误"

class login_form(BaseModel):
    code: str

@auth_route.post('/signin')
async def signin_auth(f: login_form, rsp: Response):
    """登录，给我code，我把令牌给你，塞在'token'字段里，同时cookie也会把你令牌写入。
    
    fastapi重构的接口支持只用cookie认证，不用特意带上令牌"""
    print("code:\t",f.code)
    try:
        openid = await get_wx_login_openid(f.code)
    except:
        return falseReturn(500, traceback.format_exc())
    print("openid:\t", openid)
    user: User = User.objects(openid=openid).first()
    if not user:
        user = User(openid=openid).save()
    
    tk = generate_jwt(user)
    print('token:\t',tk)
    rsp.set_cookie("Authorization", tk, 86400)
    return trueReturn({
        'user': user,
        'token': tk,
        # 'is_admin': user.openid in admins,
        'is_bind': user.identity is not None
    })

class identity_lookup_form(BaseModel):
    phone: str
    name: str
    # studentid: str = ""



@auth_route.post('/bind', dependencies=[Depends(validsign)])
async def bind_auth(f: identity_lookup_form):
    """绑定信息，只允许首次绑定，phone不为空时视为已绑定"""

    if g().user.identity is not None:
        return falseReturn(403, "您已绑定过信息！")

    iden = Identity.objects(phone=f.phone, name=f.name).first()

    if not iden:
        return falseReturn(404, "找不到该身份！")

    g().user.identity = iden

    g().user.save()

    return trueReturn({
        'user':g().user.get_base_info(),
        'is_admin': g().user.openid in admins,
        'is_bind': g().user.identity is not None
    })

@auth_route.post('/lookup', dependencies=[Depends(validsign)])
async def lookup_auth(f: identity_lookup_form):
    """根据电话和名字检索一个身份"""

    iden = Identity.objects(phone=f.phone, name=f.name).first()

    if not iden:
        return falseReturn(404, "找不到该身份！")

    return trueReturn(iden.get_base_info())

@auth_route.get('/info', dependencies=[
    Depends(validsign)
])
async def info_auth(iid: str):
    """获取一个身份的具体信息，队长或者老师用，管理也能用"""
    iden = chkid(iid)
    team = Team.objects(members__contains=iden).first()
    if not team:
        return falseReturn(400, '这人不属于任何队伍')

    if g().user.identity not in [team.leader] + team.teachers:
        ret = validcall(0xFFFF)()
        logging.debug(ret)
        
        if ret is not None:
            return ret
    # print(iden)
    return trueReturn(iden.get_base_info())



@auth_route.post('/import', dependencies=[
    Depends(validsign), 
    Depends(validcall(0xFFFF))
])
async def import_auth(f: UploadFile = File(...)):
    """使用csv文件导入身份，注意导入后会清掉原有数据"""
    Identity.objects.delete()
    try:
        csv_reader = csv.reader(codecs.iterdecode(f.file,'utf-8-sig', errors='strict'), 
            dialect=CustomDialect
        )
        f.file.seek(0)
        next(csv_reader)
    except:
        csv_reader = csv.reader(codecs.iterdecode(f.file,'gbk', errors='strict'), 
            dialect=CustomDialect
        )
        f.file.seek(0)
        next(csv_reader)

    for row in csv_reader:
        # print(row[0], row[1], row[2])
        Identity(studentid = row[0], name = row[1], phone = row[2]).save()
    return trueReturn(
        {"total_count":len(Identity.objects())}
    )


@auth_route.get('/verify', dependencies=[Depends(validsign)])
async def verify_auth():
    """验证登录"""
    return trueReturn({'user':g().user.get_base_info(),'is_admin': g().user.openid in admins})
