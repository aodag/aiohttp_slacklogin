import os
from aiohttp import web
import aiohttp_session.cookie_storage
import aiohttp_security.abc
import aiohttp_slacklogin


class SimpleAuthorizationPolicy(aiohttp_security.abc.AbstractAuthorizationPolicy):
    async def permits(self, identity, permission, context=None):
        return True

    async def authorized_userid(self, identity):
        return identity


async def index(request: web.Request) -> web.Response:
    userid = await aiohttp_security.authorized_userid(request)
    if not userid:
        login_url = request.app.router["slacklogin.login"].url_for()
        return web.Response(
            text=f'hello <a href="{login_url}">'
            '<img src="https://api.slack.com/img/sign_in_with_slack.png" />'
            "</a>",
            content_type="text/html",
        )
    else:
        return web.Response(
            text=f"hello {userid} " '<a href="">' "Logout" "</a>",
            content_type="text/html",
        )


def main():
    app = web.Application()
    app.router.add_get("/", index)
    aiohttp_slacklogin.setup(
        app,
        client_id=os.environ["SLACK_CLIENT_ID"],
        client_secret=os.environ["SLACK_CLIENT_SECRET"],
        redirect_uri="http://localhost:8080/slacklogin/oauth/callback",
    )
    aiohttp_session.setup(
        app, aiohttp_session.cookie_storage.EncryptedCookieStorage(b"s" * 32)
    )
    aiohttp_security.setup(
        app, aiohttp_security.SessionIdentityPolicy(), SimpleAuthorizationPolicy()
    )
    web.run_app(app)


if __name__ == "__main__":
    main()
