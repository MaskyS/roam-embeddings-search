"""Client adapters for external services used in semantic sync."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

import httpx
import voyageai
import weaviate
from funcy import lsplit, suppress
from weaviate.classes.config import Configure, DataType, Property, Tokenization
from weaviate.classes.query import Filter


@dataclass
class ChunkerConfig:
    url: str
    retries: int = 3
    base_delay: float = 2.0


class ChunkerClient:
    """Async HTTP client for the chunker microservice."""

    def __init__(self, config: ChunkerConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(timeout=60.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def wait_until_ready(self, timeout: float = 60.0) -> bool:
        loop = asyncio.get_running_loop()
        end_time = loop.time() + timeout
        while loop.time() < end_time:
            with suppress(httpx.HTTPError):
                response = await self._client.get(f"{self._config.url}/health", timeout=5.0)
                if response.status_code == 200 and response.json().get("chunker_loaded"):
                    return True
            await asyncio.sleep(2)
        return False

    async def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Chunk ``text`` returning list of chunk dictionaries."""

        attempt = 0
        while True:
            try:
                response = await self._client.post(
                    f"{self._config.url}/chunk",
                    json={"text": text},
                )
                response.raise_for_status()
                data = response.json()
                return data.get("chunks", [])
            except (httpx.ConnectError, httpx.HTTPStatusError, httpx.ReadTimeout) as exc:
                attempt += 1
                if attempt >= self._config.retries:
                    raise
                await asyncio.sleep(self._config.base_delay * (2 ** (attempt - 1)))

    async def chunk_batch(self, texts: Sequence[str]) -> List[List[Dict[str, Any]]]:
        attempt = 0
        while True:
            try:
                response = await self._client.post(
                    f"{self._config.url}/chunk/batch",
                    json={"texts": list(texts)},
                )
                response.raise_for_status()
                data = response.json()
                return [entry.get("chunks", []) for entry in data.get("results", [])]
            except (httpx.ConnectError, httpx.HTTPStatusError, httpx.ReadTimeout):
                attempt += 1
                if attempt >= self._config.retries:
                    raise
                await asyncio.sleep(self._config.base_delay * (2 ** (attempt - 1)))


class VoyageEmbeddingClient:
    """Thin async wrapper around VoyageAI contextual embeddings."""

    def __init__(
        self,
        api_key: str,
        model: str,
        input_type: str = "document",
        timeout: Optional[float] = None,
    ) -> None:
        kwargs: Dict[str, Any] = {"api_key": api_key}
        if timeout is not None:
            kwargs["timeout"] = timeout
        self._client = voyageai.Client(**kwargs)
        self._model = model
        self._input_type = input_type

    async def embed_documents(
        self,
        pages: Sequence[Sequence[str]],
        *,
        retries: int = 3,
    ) -> List[List[List[float]]]:
        loop = asyncio.get_running_loop()

        def call() -> List[List[List[float]]]:
            result = self._client.contextualized_embed(
                inputs=list(pages),
                model=self._model,
                input_type=self._input_type,
            )
            return [item.embeddings for item in result.results]

        async def run_once():
            return await loop.run_in_executor(None, call)

        for attempt in range(max(1, retries)):
            try:
                return await loop.run_in_executor(None, call)
            except Exception:
                if attempt >= retries - 1:
                    raise
                await asyncio.sleep(min(2 ** (attempt + 1), 10))

    async def embed_query(self, query: str, *, retries: int = 3) -> List[float]:
        loop = asyncio.get_running_loop()

        def call() -> List[float]:
            result = self._client.contextualized_embed(
                inputs=[[query]],
                model=self._model,
                input_type="query",
            )
            return result.results[0].embeddings[0]

        for attempt in range(max(1, retries)):
            try:
                return await loop.run_in_executor(None, call)
            except Exception:
                if attempt >= retries - 1:
                    raise
                await asyncio.sleep(min(2 ** (attempt + 1), 10))


class WeaviateSyncAdapter:
    """Encapsulates Weaviate interactions needed by semantic sync."""

    def __init__(self, client: weaviate.WeaviateClient, collection_name: str) -> None:
        self._client = client
        self._collection_name = collection_name

    def ensure_schema(self, recreate: bool = False) -> None:
        collections = self._client.collections
        if collections.exists(self._collection_name):
            if recreate:
                collections.delete(self._collection_name)
            else:
                return
        collections.create(
            name=self._collection_name,
            vectorizer_config=Configure.Vectorizer.none(),
            reranker_config=Configure.Reranker.voyageai(model="rerank-2-lite"),
            properties=[
                Property(name="chunk_text_preview", data_type=DataType.TEXT),
                Property(name="primary_uid", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
                Property(name="page_title", data_type=DataType.TEXT, tokenization=Tokenization.WORD),
                Property(name="page_uid", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
                Property(name="document_type", data_type=DataType.TEXT, tokenization=Tokenization.FIELD),
                Property(name="source_uids_json", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="chunk_token_count", data_type=DataType.INT),
                Property(name="sync_version", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="last_synced_edit_time", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="content_hash", data_type=DataType.TEXT, skip_vectorization=True),
            ],
        )

    def get_collection(self):
        return self._client.collections.get(self._collection_name)

    def fetch_existing_page_state(self, page_uid: str) -> Dict[str, Any]:
        collection = self.get_collection()
        state = {
            "page_objects": [],
            "chunk_objects": [],
            "last_synced_edit_time": None,
            "content_hash": None,
        }

        filters = Filter.by_property("page_uid").equal(page_uid)
        try:
            response = collection.query.fetch_objects(
                filters=filters,
                limit=500,
                return_properties=[
                    "document_type",
                    "last_synced_edit_time",
                    "content_hash",
                    "primary_uid",
                    "page_uid",
                ],
            )
        except Exception as exc:  # pragma: no cover
            print(f"  ✗ Failed to fetch objects for page {page_uid}: {exc}")
            return state

        if not response or not response.objects:
            return state

        page_objects, chunk_objects = lsplit(
            lambda obj: obj.properties.get("document_type") == "page",
            response.objects,
        )
        state["page_objects"].extend(page_objects)
        state["chunk_objects"].extend(chunk_objects)

        if state["page_objects"]:
            page_obj = state["page_objects"][0]
            state["last_synced_edit_time"] = page_obj.properties.get("last_synced_edit_time")
            state["content_hash"] = page_obj.properties.get("content_hash")

        return state

    def delete_stale_objects(self, page_uid: str, content_hash: str) -> None:
        collection = self.get_collection()
        if content_hash:
            filters = Filter.by_property("page_uid").equal(page_uid) & Filter.by_property("content_hash").not_equal(content_hash)
        else:
            filters = Filter.by_property("page_uid").equal(page_uid)
        collection.data.delete_many(where=filters)

    def insert_objects(self, objects: Sequence[Dict[str, Any]]) -> List[Any]:
        collection = self.get_collection()
        object_by_uuid = {obj["uuid"]: obj for obj in objects}
        duplicate_substrings = ("already exists", "duplicate", "conflicts with")

        with collection.batch.dynamic() as batch:
            for obj in objects:
                batch.add_object(
                    properties=obj["properties"],
                    uuid=obj["uuid"],
                    vector=obj.get("vector"),
                )

        unrecoverable: List[Any] = []
        for error in collection.batch.failed_objects:
            message = getattr(error, "message", "") or ""
            uuid = str(getattr(getattr(error, "object_", None), "uuid", ""))

            if uuid and any(token in message.lower() for token in duplicate_substrings):
                obj = object_by_uuid.get(uuid)
                if not obj:
                    unrecoverable.append(error)
                    continue
                try:
                    # Replace existing objects to emulate an upsert when deterministic UUIDs collide.
                    collection.data.replace(
                        uuid=obj["uuid"],
                        properties=obj["properties"],
                        vector=obj.get("vector"),
                    ).get()
                    continue
                except Exception as replace_exc:
                    error.message = f"{message} | replace failed: {replace_exc}"

            unrecoverable.append(error)

        return unrecoverable
