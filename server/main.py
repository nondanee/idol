import asyncio
import logging
import hashlib, base64

from aiohttp import web
from cryptography import fernet
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from pool import create_pool
from routes import setup_routes

def init(loop):
    app = web.Application(loop = loop)
    app.on_startup.append(create_pool)

    # fernet_key = fernet.Fernet.generate_key()
    fernet_key = b'wAYavr8zyR2kvmf1uXGko4MdGJ8cpDFOUW0lHIxoQ-I='
    secret_key = base64.urlsafe_b64decode(fernet_key)

    setup(app, EncryptedCookieStorage(secret_key, max_age = 1296000))

    # app.add_routes([web.static('/static','../static', show_index = True)])
    setup_routes(app)

    return app

def main():

    # logging.basicConfig(level = logging.DEBUG)
    loop = asyncio.get_event_loop()

    app = init(loop)
    web.run_app(app, host = '127.0.0.1', port = 8080)

if __name__ == '__main__':
    main()
