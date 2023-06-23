import logging

import aiohttp
import aiohttp_jinja2
from aiohttp import web
from faker import Faker

log = logging.getLogger(__name__)


def get_random_name():
    faker = Faker()
    return faker.unique.first_name()


async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template("index.html", request, {})

    await ws_current.prepare(request)

    name = get_random_name()
    log.info(f"{name} joined")

    await ws_current.send_json({"text": f">>> Welcome {name}"})

    for ws in request.app["websockets"].values():
        await ws.send_json({"text": f">>> {name} joined"})
    request.app["websockets"][name] = ws_current

    while True:
        msg = await ws_current.receive()

        if msg.type == aiohttp.WSMsgType.text:
            for ws in request.app["websockets"].values():
                if ws is not ws_current:
                    await ws.send_json({"text": f"<{name}> {msg.data}"})
        else:
            break

    del request.app["websockets"][name]
    log.info(f"{name} disconnected")
    for ws in request.app["websockets"].values():
        await ws.send_json({"text": f">>> {name} disconnected"})

    return ws_current
