from urllib import parse
from json import loads
from aiofile import async_open
from aiohttp import ClientSession


def urlsplit(url: str) -> dict:
    return dict(parse.parse_qsl(parse.urlsplit(url).query))


async def get(url: str, **kwargs):
    async with ClientSession() as session:
        async with session.get(url, **kwargs) as reply:
            return await reply.read()


async def post(url: str, **kwargs):
    async with ClientSession() as session:
        async with session.post(url, **kwargs) as reply:
            return await reply.read()


async def get_cookie(url: str, data: dict, **kwargs):
    async with ClientSession() as session:
        async with session.post(url, data=data, **kwargs) as reply:
            data = loads(await reply.read())
            assert data["status"] != "error", data["message"]
            return str(reply.cookies.get("SESSION")).split(" ")[1]


async def save(data: bytes, path: str):
    async with async_open(f"{path}", "wb") as file:
        await file.write(data)


__all__ = [
    "get",
    "post",
    "save",
    "loads",
    "urlsplit",
    "get_cookie"
]