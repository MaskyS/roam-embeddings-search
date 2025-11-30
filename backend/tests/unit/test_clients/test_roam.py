"""Unit tests for the RoamClient."""

from __future__ import annotations

import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock

from clients.roam import RoamClient, query_roam


@pytest.fixture
def roam_client():
    return RoamClient(
        graph_name="test-graph",
        token="test-token",
        requests_per_minute=50,
    )


class TestQueryRoam:
    """Tests for the query_roam standalone function."""

    @pytest.mark.asyncio
    async def test_query_roam_success(self):
        """Should return query results on success."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": [["uid1"], ["uid2"]]}
        mock_response.raise_for_status = MagicMock()

        with patch("clients.roam.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            result = await query_roam(
                token="test-token",
                graph_name="test-graph",
                query="[:find ?uid :where [?e :block/uid ?uid]]",
            )

        assert result == {"result": [["uid1"], ["uid2"]]}

    @pytest.mark.asyncio
    async def test_query_roam_http_error(self):
        """Should return None on HTTP error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=MagicMock(), response=mock_response
        )

        with patch("clients.roam.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            result = await query_roam(
                token="test-token",
                graph_name="test-graph",
                query="[:find ?uid]",
            )

        assert result is None


class TestRoamClientGetAllPageUids:
    """Tests for RoamClient.get_all_page_uids method."""

    @pytest.mark.asyncio
    async def test_get_all_page_uids_success(self, roam_client):
        """Should return list of UIDs."""
        with patch("clients.roam.query_roam", new_callable=AsyncMock) as mock_query:
            mock_query.return_value = {"result": [["uid1"], ["uid2"], ["uid3"]]}
            result = await roam_client.get_all_page_uids()

        assert result == ["uid1", "uid2", "uid3"]

    @pytest.mark.asyncio
    async def test_get_all_page_uids_empty(self, roam_client):
        """Should return empty list when no pages found."""
        with patch("clients.roam.query_roam", new_callable=AsyncMock) as mock_query:
            mock_query.return_value = {"result": []}
            result = await roam_client.get_all_page_uids()

        assert result == []

    @pytest.mark.asyncio
    async def test_get_all_page_uids_query_failure(self, roam_client):
        """Should return empty list on query failure."""
        with patch("clients.roam.query_roam", new_callable=AsyncMock) as mock_query:
            mock_query.return_value = None
            result = await roam_client.get_all_page_uids()

        assert result == []


class TestRoamClientPullManyPages:
    """Tests for RoamClient.pull_many_pages method."""

    @pytest.mark.asyncio
    async def test_pull_many_pages_success(self, roam_client):
        """Should return page data for each UID."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {":block/uid": "page1", ":node/title": "Page 1"},
                {":block/uid": "page2", ":node/title": "Page 2"},
            ]
        }

        with patch.object(roam_client, "_post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await roam_client.pull_many_pages(["page1", "page2"])

        assert len(result) == 2
        assert result[0][":node/title"] == "Page 1"

    @pytest.mark.asyncio
    async def test_pull_many_pages_empty_uids(self, roam_client):
        """Should return empty list for empty input."""
        result = await roam_client.pull_many_pages([])
        assert result == []

    @pytest.mark.asyncio
    async def test_pull_many_pages_http_failure(self, roam_client):
        """Should return None values on HTTP failure."""
        mock_response = MagicMock()
        mock_response.status_code = 500

        with patch.object(roam_client, "_post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await roam_client.pull_many_pages(["page1", "page2"])

        assert result == [None, None]


class TestRoamClientPullManyMetadata:
    """Tests for RoamClient.pull_many_metadata method."""

    @pytest.mark.asyncio
    async def test_pull_many_metadata_success(self, roam_client):
        """Should return metadata for each UID."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": [
                {":block/uid": "page1", ":edit/time": 1700000000000},
                {":block/uid": "page2", ":edit/time": 1700000000001},
            ]
        }

        with patch.object(roam_client, "_post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            result = await roam_client.pull_many_metadata(["page1", "page2"])

        assert len(result) == 2
        assert result[0][":edit/time"] == 1700000000000


class TestRoamClientBuildPayload:
    """Tests for RoamClient._build_payload method."""

    def test_build_payload_single_uid(self, roam_client):
        """Should format single UID correctly."""
        payload = roam_client._build_payload(["uid1"], "[:block/uid]")
        assert payload["eids"] == '[[:block/uid "uid1"]]'
        assert payload["selector"] == "[:block/uid]"

    def test_build_payload_multiple_uids(self, roam_client):
        """Should format multiple UIDs correctly."""
        payload = roam_client._build_payload(["uid1", "uid2", "uid3"], "[:block/uid]")
        assert payload["eids"] == '[[:block/uid "uid1"] [:block/uid "uid2"] [:block/uid "uid3"]]'


class TestRoamClientPost:
    """Tests for RoamClient._post method."""

    @pytest.mark.asyncio
    async def test_post_success(self, roam_client):
        """Should return response on success."""
        mock_response = MagicMock()
        mock_response.status_code = 200

        with patch("clients.roam.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            # Need to acquire the limiter first in test context
            async with roam_client._limiter:
                pass  # Just to ensure limiter is initialized

            response = await roam_client._post("test-endpoint", {"key": "value"}, timeout=30.0)

        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_post_server_error_raises(self, roam_client):
        """Should raise on 5xx errors for retry."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=MagicMock(), response=mock_response
        )

        with patch("clients.roam.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError):
                await roam_client._post("test-endpoint", {}, timeout=30.0)

    @pytest.mark.asyncio
    async def test_post_rate_limit_raises(self, roam_client):
        """Should raise on 429 for retry."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Rate limited", request=MagicMock(), response=mock_response
        )

        with patch("clients.roam.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client

            with pytest.raises(httpx.HTTPStatusError):
                await roam_client._post("test-endpoint", {}, timeout=30.0)
