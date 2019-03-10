import uuid

from aiohttp import web
from aiohttp_security import remember
from aiohttp_session import get_session

from .slackapi import get_slack_api

routes = web.RouteTableDef()


@routes.get("/login", name="slacklogin.login")
async def login(request: web.Request) -> web.Response:
    api = get_slack_api(request)
    state = uuid.uuid4().hex

    session = await get_session(request)
    session["slacklogin.state"] = state
    url = api.get_authorize_url(state)
    return web.HTTPFound(url)


@routes.get("/slacklogin/oauth/callback", name="slacklogin.oauth_callback")
async def oauth_callback(request: web.Request) -> web.Response:
    api = get_slack_api(request)
    code = request.query

    session = await get_session(request)
    state = session["slacklogin.state"]
    if state != code["state"]:
        return web.HTTPBadRequest(text="invalid state")

    token = await api.get_access_token(code=code["code"])

    response = web.Response(text=f"ok {token}")
    identity = f"{token['user']['name']}+{token['user']['id']}@{token['team']['id']}"
    await remember(request, response, identity)
    return response
