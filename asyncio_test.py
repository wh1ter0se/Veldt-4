import asyncio, time
from threading import Thread

async def print_nums(q:asyncio.Queue):
    print('coro started')
    await asyncio.sleep(1)
    i = 0
    while True:
        await q.put(str(i))
        time.sleep(1)
        # print(f'sending {i}')
        i += 1

async def main():
    q = asyncio.Queue()
    # task = asyncio.create_task(print_nums(q))
    # await asyncio.get_event_loop().run_in_executor(None, print_nums, q)
    loop = asyncio.new_event_loop()

    def f(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    t = Thread(target=f, args=(loop,))
    t.start() 
    # loop.call_soon_threadsafe(asyncio.async, ())
    future = asyncio.run_coroutine_threadsafe(print_nums(q), loop)

    await q.join()
    print('Queue joined')
    while True:
        try:
            print(q.get_nowait())
        except asyncio.QueueEmpty: pass