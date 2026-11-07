import asyncio
import inspect
import json
from datetime import UTC
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from curl_cffi.requests.exceptions import RequestException

from clashroyaleapi import (
    APIError,
    AuthenticationError,
    Battle,
    Client,
    InvalidParameter,
    InvalidResponse,
    NetworkError,
    NotFound,
    Player,
    RateLimitExceeded,
    ServerError,
)

REFERENCE = json.loads((Path(__file__).parents[1] / "docs/api-reference.json").read_text())


def response(data, status=200, headers=None):
    return SimpleNamespace(status_code=status, headers=headers or {}, json=lambda: data)


@pytest.fixture
async def client():
    async with Client("test-token", max_attempts=1) as c:
        c._session.get = AsyncMock()
        yield c


@pytest.mark.parametrize("op", REFERENCE["operations"], ids=lambda o: o["python_method"])
async def test_every_endpoint(client, op):
    method = getattr(client, op["python_method"])
    kwargs = {}
    paths = op["path"]
    query = {}
    for p in op["parameters"]:
        name = next(
            n
            for n in inspect.signature(method).parameters
            if n.replace("_", "").lower() == p["name"].lower()
        )
        value = 5 if p["type"] == "integer" else "#abc" if p["name"].endswith("Tag") else "abc"
        if p["name"] == "before":
            continue
        kwargs[name] = value
        if p["in"] == "path":
            paths = paths.replace(
                "{" + p["name"] + "}", "%23ABC" if p["name"].endswith("Tag") else str(value)
            )
        else:
            query[p["name"]] = value
    paginated = any(p["name"] == "after" for p in op["parameters"])
    is_list = op["response"].endswith("List") or op["response"] in ("ClanWarLog", "RiverRaceLog")
    client._session.get.return_value = response(
        {"items": []} if paginated else [] if is_list else {}
    )
    await method(**kwargs)
    client._session.get.assert_awaited_once_with(
        "https://api.clashroyale.com/v1" + paths, params=query
    )
    if paginated:
        assert inspect.isasyncgenfunction(getattr(client, "iter_" + op["python_method"]))


async def test_pagination_and_repeat(client):
    client._session.get.side_effect = [
        response({"items": [{"name": "one"}], "paging": {"cursors": {"after": "a"}}}),
        response({"items": [{"name": "two"}]}),
    ]
    assert [x.name async for x in client.iter_get_cards()] == ["one", "two"]
    assert client._session.get.await_args.kwargs["params"] == {"after": "a"}
    client._session.get.side_effect = None
    client._session.get.return_value = response(
        {"items": [{}], "paging": {"cursors": {"after": "a"}}}
    )
    with pytest.raises(InvalidResponse, match="repeated"):
        _ = [x async for x in client.iter_get_cards()]


async def test_backward_and_empty(client):
    client._session.get.return_value = response(
        {"items": [], "paging": {"cursors": {"before": "next"}}}
    )
    assert [x async for x in client.iter_get_cards(before="start")] == []
    assert client._session.get.await_count == 1


@pytest.mark.parametrize(
    ("status", "error"),
    [
        (400, InvalidParameter),
        (401, AuthenticationError),
        (403, AuthenticationError),
        (404, NotFound),
        (429, RateLimitExceeded),
        (500, ServerError),
        (503, ServerError),
        (302, APIError),
        (418, APIError),
    ],
)
async def test_errors(client, status, error):
    client._session.get.return_value = response(
        {"message": "oops", "reason": "test", "detail": {"x": 1}}, status
    )
    with pytest.raises(error) as caught:
        await client.get_player("abc")
    assert caught.value.status == status
    assert caught.value.reason == "test"
    assert caught.value.detail == {"x": 1}


async def test_retry_network_and_cancellation(monkeypatch):
    sleep = AsyncMock()
    monkeypatch.setattr("clashroyaleapi.transport.asyncio.sleep", sleep)
    async with Client("token") as c:
        c._session.get = AsyncMock(
            side_effect=[RequestException("private"), response({}, 503), response({"name": "ok"})]
        )
        assert (await c.get_player("abc")).name == "ok"
        assert sleep.await_count == 2
        c._session.get.side_effect = RequestException("secret")
        with pytest.raises(NetworkError, match="API network request failed"):
            await c.get_player("abc")
        c._session.get.side_effect = asyncio.CancelledError()
        with pytest.raises(asyncio.CancelledError):
            await c.get_player("abc")


async def test_cache(monkeypatch):
    now = [0.0]
    monkeypatch.setattr("clashroyaleapi.transport.time.monotonic", lambda: now[0])
    async with Client("token", cache_ttl=10, cache_size=1) as c:
        c._session.get = AsyncMock(return_value=response({"items": []}))
        await c.get_cards(limit=1)
        await c.get_cards(limit=1)
        assert c._session.get.await_count == 1
        await c.get_cards(limit=2)
        await c.get_cards(limit=1)
        assert c._session.get.await_count == 3
        now[0] = 11
        await c.get_cards(limit=1)
        assert c._session.get.await_count == 4
    await c.close()
    with pytest.raises(RuntimeError):
        await c.get_cards()


async def test_validation_and_shapes(client):
    for kwargs in ({"before": "a", "after": "b"}, {"limit": 0}):
        with pytest.raises(ValueError):
            await client.get_cards(**kwargs)
    with pytest.raises(ValueError):
        await client.search_clans()
    with pytest.raises(ValueError):
        await client.search_clans(name="ab")
    with pytest.raises(ValueError):
        await client.get_player("#")
    client._session.get.assert_not_awaited()
    for data in ({}, {"items": None}, {"items": [3]}):
        client._session.get.return_value = response(data)
        with pytest.raises(InvalidResponse):
            await client.get_cards()
    client._session.get.return_value = SimpleNamespace(
        status_code=200, headers={}, json=lambda: json.loads("bad")
    )
    with pytest.raises(InvalidResponse):
        await client.get_player("abc")


def test_models_and_retry_after():
    player = Player.model_validate(
        {
            "name": "Test",
            "clan": None,
            "cards": [{"name": "Knight", "future": 42}],
            "future": {"a": 1},
        }
    )
    assert player.cards[0].name == "Knight"
    assert player.to_dict()["cards"][0]["future"] == 42
    assert player.to_dict()["future"] == {"a": 1}
    b = Battle.model_validate({"battleTime": "20261107T010203.000Z", "isHostedMatch": False})
    assert b.battle_time.tzinfo == UTC
    assert b.is_hosted_match is False
    assert Client._delay({"Retry-After": "999"}, 0) == 30
    assert Client._delay({"Retry-After": "bad"}, 0) == 0.5


async def test_real_curl_transport():
    received = []

    async def handle(reader, writer):
        received.append((await reader.readuntil(b"\r\n\r\n")).decode())
        body = b'{"name":"Local","collectionLevel":42}'
        writer.write(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\nContent-Length: "
            + str(len(body)).encode()
            + b"\r\n\r\n"
            + body
        )
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    async with server:
        port = server.sockets[0].getsockname()[1]
        async with Client("local-token", base_url=f"http://127.0.0.1:{port}/v1") as c:
            p = await c.get_player("#abc")
            assert p.collection_level == 42
    assert "GET /v1/players/%23ABC " in received[0]
    assert "authorization: bearer local-token" in received[0].lower()


def test_manifest_complete():
    assert len(REFERENCE["operations"]) == 30
    assert len({o["path"] for o in REFERENCE["operations"]}) == 30
    assert all(o["method"] == "GET" for o in REFERENCE["operations"])


async def test_tag_encoding_and_cache_mutation(client):
    client._session.get.return_value = response({"name": "Test", "future": {"value": 1}})
    await client.get_player("%23abc")
    assert client._session.get.await_args.args[0].endswith("/players/%23ABC")
    async with Client("token", cache_ttl=30) as c:
        c._session.get = AsyncMock(return_value=response({"name": "Test", "future": {"value": 1}}))
        first = await c.get_player("abc")
        first.model_extra["future"]["value"] = 99
        second = await c.get_player("abc")
        assert second.to_dict()["future"]["value"] == 1
        assert c._session.get.await_count == 1
