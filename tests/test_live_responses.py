"""Regression cases captured from real Supercell responses, with names/tags replaced."""

import inspect
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from clashroyaleapi import Client, LeaderboardEntry, LeagueSeasonV2, Page
from scripts.live_audit import export, normalize

FIXTURES = json.loads((Path(__file__).parent / "fixtures/live-responses.json").read_text())
CASES = [(method, case) for method, cases in FIXTURES.items() for case in cases]


@pytest.mark.parametrize(("method", "case"), CASES, ids=[m for m, _ in CASES])
async def test_live_response_round_trip(method, case):
    async with Client("test-token", max_attempts=1) as client:
        client._session.get = AsyncMock(
            return_value=SimpleNamespace(status_code=200, headers={}, json=lambda: case["response"])
        )
        result = await getattr(client, method)(**case["arguments"])
        raw = case["response"]
        if isinstance(result, list) and isinstance(raw, dict):
            raw = raw["items"]
        if isinstance(result, Page) and isinstance(raw, list):
            raw = {"items": raw}
        assert normalize(export(result)) == normalize(raw)
        if method == "get_leaderboard":
            assert isinstance(result.items[0], LeaderboardEntry)
            assert result.items[0].rank is not None
            assert result.items[0].score is not None
        if method == "get_seasons_v2":
            assert isinstance(result[0], LeagueSeasonV2)
        if method == "get_events":
            assert result[0].event_tag is not None


def test_live_corrected_response_annotations():
    assert "LeaderboardEntry" in str(inspect.signature(Client.get_leaderboard))
    assert "LeagueSeasonV2" in str(inspect.signature(Client.get_seasons_v2))


@pytest.mark.parametrize(
    ("status", "body", "expected"),
    [
        (404, {"reason": "notFound"}, "unresolved_resource"),
        (404, {"message": "This API endpoint has been temporarily disabled"}, "upstream_disabled"),
        (410, {"message": "This API endpoint has been permanently removed."}, "upstream_disabled"),
        (403, {"reason": "accessDenied"}, "failed"),
        (503, {"message": "maintenance"}, "upstream_error"),
        (200, {"items": [3]}, "failed"),
    ],
)
async def test_audit_does_not_hide_failures(tmp_path, status, body, expected):
    from scripts.live_audit import Audit

    async with Client("test-token", max_attempts=1) as client:
        client._session.get = AsyncMock(
            return_value=SimpleNamespace(status_code=status, headers={}, json=lambda: body)
        )
        audit = Audit(client, tmp_path)
        await audit.call("get_cards")
        assert audit.records[-1]["outcome"] == expected
        assert audit.request_count == 1
        assert "test-token" not in next(tmp_path.glob("*.json")).read_text()
