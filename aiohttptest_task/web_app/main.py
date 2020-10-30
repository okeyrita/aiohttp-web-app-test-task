import logging
import sys

import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiohttptest_task.middlewares import setup_middlewares
from aiohttptest_task.routes import setup_routes
from aiohttptest_task.settings import get_config


async def init_app(argv=None):

    app = web.Application()

    app['config'] = get_config(argv)

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('aiohttptest_task', 'templates'))

    # setup views and routes
    setup_routes(app)

    setup_middlewares(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    app = init_app(argv)

    config = get_config(argv)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
