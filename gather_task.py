import asyncio
import logging
import time
from aiohttp import web

log = logging.getLogger(__name__)

LONG_RESOLUTION = 10
SHORT_RESOLUTION = 5


class GatherTask:
    def __init__(self, urls, session, loop):
        self.loop = loop
        self.session = session
        self.urls = urls
        self.statuses = {}

    def start(self):
        return asyncio.gather(
            self.loop.create_task(self.gather_short_loop()),
            self.loop.create_task(self.gather_long_loop())
        )

    async def gather_short_loop(self):
        while True:
            try:
                await self.collect_short()
            except:
                log.exception('ping errors!')
                await asyncio.sleep(SHORT_RESOLUTION)

    async def collect_short(self):
        current_time = time.time()
        url = self.urls['short']
        log.info(f'{url} - Short')
        self.write_data('short', 'test1')

        latency_of_telemetry_calls = (time.time() - current_time)
        await asyncio.sleep(
            SHORT_RESOLUTION - latency_of_telemetry_calls, loop=self.loop)

    async def gather_long_loop(self):
        while True:
            try:
                await self.collect_long()
            except:
                log.exception('health errors')
                await asyncio.sleep(LONG_RESOLUTION)

    async def collect_long(self):
        current_time = time.time()
        url = self.urls['long']
        log.info(f'{url} - Long')
        self.write_data('long', 'test2')

        latency_of_telemetry_calls = (time.time() - current_time)
        await asyncio.sleep(
            LONG_RESOLUTION - latency_of_telemetry_calls, loop=self.loop)

    def write_data(self, key, value):
        self.statuses[key] = value

    async def stored_data(self, request):
        print('working!')
        return web.json_response(data=self.statuses)

    async def endpoints(self, request):
        return web.json_response(data={'enpoints': list(self.urls.keys())})
