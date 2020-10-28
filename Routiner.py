from graia.broadcast.entities.event import BaseEvent
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from graia.broadcast.protocols.executor import ExecutorProtocol
from graia.broadcast.entities.listener import Listener
from graia.broadcast import Broadcast
from graia.broadcast.entities.decorater import Decorater
from graia.broadcast.builtin.decoraters import Depend, Middleware
from graia.broadcast.interfaces.decorater import DecoraterInterface
from graia.broadcast.exceptions import PropagationCancelled
from graia.application.event.messages import GroupMessage
import random
import asyncio
import time
import copy
import datetime

# class GroupMessage(MiraiEvent):
#     type: str = "GroupMessage"
#     messageChain: MessageChain
#     sender: Member

#     class Dispatcher(BaseDispatcher):
#         mixin = [MessageChainCatcher, ApplicationDispatcher]

#         @staticmethod
#         def catch(interface: DispatcherInterface):
#             if interface.annotation is Group:
#                 return interface.event.sender.group
#             elif interface.annotation is Member:
#                 return interface.event.sender

class parseminus(BaseDispatcher):
    @staticmethod
    async def catch(interface: DispatcherInterface):
        print(interface.name)
        if interface.name == "extDict":
            print('etx')
            return {'a':233}

class D1(BaseDispatcher):
    @staticmethod
    def catch(interface: DispatcherInterface):
        if interface.annotation == dict:
            return random.random()

class D2(BaseDispatcher):
    mixin = [D1]
    @staticmethod
    async def catch(interface: DispatcherInterface):
        if interface.annotation == "13":
            r = await interface.execute_with(interface.name, "123", interface.default)
            return r

class TestEvent(BaseEvent):
    extDict: dict

    class Dispatcher(BaseDispatcher):
        mixin = [D2]

        @staticmethod
        def catch(interface: DispatcherInterface):
            # print(interface.parameter_contexts)
            if interface.name == "u":
                yield 1
            elif interface.annotation == str:
                yield 12

event = TestEvent()
loop = asyncio.get_event_loop()
broadcast = Broadcast(loop=loop, debug_flag=True)

i = 0
l = asyncio.Lock()

async def r(extDict: dict):
    global i
    async with l:
        i += 1

# for _ in range(15):
@broadcast.receiver(TestEvent, headless_decoraters=[Depend(r)], dispatchers=[parseminus])
async def test():
    print(datetime.datetime.now())
        # print(extDict)

@broadcast.receiver(TestEvent, headless_decoraters=[Depend(r)])
async def test2(extDict: dict):
    print(extDict)

@broadcast.receiver(TestEvent, headless_decoraters=[Depend(r)])
async def test3():
    print('coconmsl')

async def main(start):
    print("将在 1 s 后开始测试.")
    for i in range(1, 2):
        print(i)
        await asyncio.sleep(1)
    print("测试开始.", start)
    for _ in range(10):
        broadcast.postEvent(TestEvent())
    end = time.time()
    print(f"事件广播完毕, 总共 10 个, 当前时间: {end}, 用时: {end - start - 5}")

start = time.time()
loop.run_until_complete(main(start))

end = time.time()
print(f"测试结束, 1s 后退出, 用时 {end - start - 5}")
loop.run_until_complete(asyncio.sleep(1))

print(i)
#import pdb; pdb.set_trace()
print("退出....", time.time() - start)