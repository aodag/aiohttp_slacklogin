from typing import Dict, Optional
from urllib.parse import urlencode

import aiohttp
from aiohttp import web
from typing_extensions import Protocol


class ISlackApi(Protocol):
    def get_authorize_url(self, state: str) -> str:  # pragma no cover
        ...

    async def get_access_token(self, code: str) -> Optional[Dict]:  # pragma no cover
        ...


class SlackApi:
    def __init__(
        self,
        *,
        redirect_uri: str,
        client_id: str,
        client_secret: str,
        token_url="https://slack.com/api/oauth.access",
        auth_url="https://slack.com/oauth/authorize",
        scope="",
    ):
        self._redirect_uri = redirect_uri
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_url = token_url
        self._auth_url = auth_url
        self._scope = scope

    @property
    def scope(self):
        scopes = self._scope.split(",")
        if "identity.basic" not in scopes:
            scopes = scopes + ["identity.basic"]
        return ",".join(scopes).strip(",")

    def get_authorize_url(self, state: str) -> str:
        query_string = urlencode(
            {
                "redirect_uri": self._redirect_uri,
                "client_id": self._client_id,
                "state": state,
                "scope": self.scope,
            }
        )
        return self._auth_url + "?" + query_string

    async def get_access_token(self, code: str) -> Optional[Dict]:
        params = {
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "redirect_uri": self._redirect_uri,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self._token_url, params=params) as resp:
                return await resp.json()
        return None


def get_slack_api(request: web.Request) -> ISlackApi:
    return request.config_dict["slackapi"]


def add_slack_api(
    app: web.Application, *, redirect_uri: str, client_id: str, client_secret: str
) -> ISlackApi:
    slack_api = SlackApi(
        redirect_uri=redirect_uri, client_id=client_id, client_secret=client_secret
    )
    app["slackapi"] = slack_api
    return slack_api
