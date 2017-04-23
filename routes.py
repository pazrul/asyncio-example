from aiohttp import web


def setup_application(loop, gatherer):
    app = web.Application(loop=loop)
    app.gatherer = gatherer

    app.router.add_get('/', test)
    app.router.add_get('/status', gatherer.stored_data)
    app.router.add_get('/endpoints', gatherer.endpoints)
    return app


async def test(request):
    return web.Response(text='test')
