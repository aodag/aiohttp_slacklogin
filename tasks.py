from invoke import task
from dotenv import load_dotenv

load_dotenv(verbose=True)


@task
def hello(ctx):
    print("Hello")


@task
def env(ctx):
    import os
    from pprint import pprint

    pprint(dict(os.environ))


@task
def serve(ctx):
    ctx.run("python -m example.simple", pty=True)


@task
def test(ctx):
    ctx.run("black aiohttp_slacklogin --check --diff", pty=True)
    ctx.run("isort -rc aiohttp_slacklogin --check --diff", pty=True)
    ctx.run("pytest -vv --cov=aiohttp_slacklogin --cov-report=term-missing", pty=True)
