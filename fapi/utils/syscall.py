from basicutils.network import *
import os

async def sys_exec(ent: CoreEntity, args: list): return f"""{exec(' '.join(args))}"""
async def sys_eval(ent: CoreEntity, args: list): 
    import fapi
    import fapi.routers
    import fapi.models
    from fapi.models.Routiner import Routiner
    from fapi.Sessions import SessionManager
    return f"""{eval(' '.join(args))}"""
async def sys_run(ent: CoreEntity, args: list): return f"""{os.popen(' '.join(args)).read()}"""
async def sys_help(ent: CoreEntity, args: list): return '目前仅支持exec, eval, run, send四个命令'
async def sys_unauthorized(ent: CoreEntity, args: list): return "您没有权限执行此调用"
