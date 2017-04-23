import asyncio
import logging
import os
import aiohttp
import toml

import log_module
from aiohttp import web
from routes import setup_application
import gather_task

log = logging.getLogger(__name__)


def load_cfg():
    config_file = os.environ['CONFIG_FILE']
    log.info(f"Loading config file {config_file}")
    with open(config_file) as conffile:
        config = toml.load(conffile)

    log.info(f"Configuration: {config}")
    return config


def main():
    log.info("---Starting Main---")
    loop = asyncio.get_event_loop()

    cfg = load_cfg()
    urls = cfg.get('urls')
    port = cfg.get('application_port')

    session = aiohttp.ClientSession(
        loop=loop, connector=aiohttp.TCPConnector(verify_ssl=False))
    gatherer = gather_task.GatherTask(urls, session, loop)
    app = setup_application(loop, gatherer)
    gatherer.start()

    web.run_app(app, port=port)


if __name__ == '__main__':
    main()
