from aiohttp import web

from . import slackapi, views
from .slackapi import SlackApi


def setup(
    app: web.Application, *, redirect_uri: str, client_id: str, client_secret: str
) -> None:
    slackapi.add_slack_api(
        app, redirect_uri=redirect_uri, client_id=client_id, client_secret=client_secret
    )
    app.add_routes(views.routes)
