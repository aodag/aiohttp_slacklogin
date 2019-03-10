import pytest


class TestSlackApi:
    @pytest.fixture
    def target(self):
        from aiohttp_slacklogin.slackapi import SlackApi

        return SlackApi

    def test_init(self, target):
        redirect_uri = "testing-redirect-uri"
        client_id = "testing-client-id"
        client_secret = "testing-client-secret"
        token_url = "https://example.com/api/oauth.access"
        auth_url = "https://example.com/oauth/authorize"
        scope = ""
        api = target(
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            token_url=token_url,
            auth_url=auth_url,
            scope=scope,
        )
        assert api._redirect_uri == redirect_uri
        assert api._client_id == client_id
        assert api._client_secret == client_secret
        assert api._token_url == token_url
        assert api._auth_url == auth_url
        assert api._scope == scope

    @pytest.mark.parametrize(
        "init_scope,scope",
        [
            ("", "identity.basic"),
            ("identity.basic", "identity.basic"),
            ("x", "x,identity.basic"),
            ("x,y", "x,y,identity.basic"),
            ("x,identity.basic,y", "x,identity.basic,y"),
            ("identity.basics", "identity.basics,identity.basic"),
        ],
    )
    def test_scope(self, target, init_scope, scope):
        redirect_uri = "testing-redirect-uri"
        client_id = "testing-client-id"
        client_secret = "testing-client-secret"
        api = target(
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            scope=init_scope,
        )
        assert api.scope == scope

    def test_get_authorize_url(self, target):
        from urllib.parse import urlparse, parse_qs

        redirect_uri = "testing-redirect-uri"
        client_id = "testing-client-id"
        client_secret = "testing-client-secret"
        token_url = "https://example.com/api/oauth.access"
        auth_url = "https://example.com/oauth/authorize"
        scope = "testing-scope"
        api = target(
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            token_url=token_url,
            auth_url=auth_url,
            scope=scope,
        )
        state = "testing-state"
        result = api.get_authorize_url(state)
        result_parsed = urlparse(result)
        assert result_parsed.hostname == "example.com"
        assert result_parsed.path == "/oauth/authorize"
        assert parse_qs(result_parsed.query) == {
            "client_id": ["testing-client-id"],
            "redirect_uri": ["testing-redirect-uri"],
            "scope": ["testing-scope,identity.basic"],
            "state": ["testing-state"],
        }
