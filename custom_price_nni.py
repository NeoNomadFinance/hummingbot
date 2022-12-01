import asyncio

import aiohttp
from aiohttp import web

price = "0.01"
UPDATE_INTERVAL = 2.0


async def safe_wrapper(c):
    try:
        return await c
    except asyncio.CancelledError:
        raise
    except Exception as e:
        print(f"Unhandled error in background task: {str(e)}")


def safe_ensure_future(coro, *args, **kwargs):
    return asyncio.ensure_future(safe_wrapper(coro), *args, **kwargs)


async def update_price():
    global price, UPDATE_INTERVAL
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.coingecko.com/api/v3/coins/neonomad-finance?market_data=true"

                response = await session.get(url)
                result = await response.json()

                price = result["market_data"]["current_price"]["usd"]
                print(f"New price fetched: {price}")
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(UPDATE_INTERVAL)


async def get_price(request):
    global price

    return web.Response(text=str(price))


async def main():

    # Ref: https://stackoverflow.com/questions/64090183/python-nonblocking-server

    event_loop = asyncio.get_event_loop()
    # starts a loop in the background to update price at an interval.
    safe_ensure_future(update_price(), loop=event_loop)

    app = web.Application()
    app.add_routes([web.get('/', get_price)])
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    await aiohttp.web.TCPSite(runner, host='localhost', port=2357).start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
