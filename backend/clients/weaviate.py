"""Encapsulates Weaviate interactions needed by semantic sync."""

from __future__ import annotations

from typing import Any, Dict, List, Sequence

import structlog
import weaviate
from funcy import lsplit

from common.retry import transient_retry
from weaviate.classes.config import Configure, DataType, Property, Tokenization
from weaviate.classes.query import Filter
from weaviate.collections.classes.batch import ErrorObject
from weaviate.collections.classes.data import DataObject

LOGGER = structlog.get_logger(__name__)


class WeaviateSyncAdapter:
    """Encapsulates Weaviate interactions needed by semantic sync."""

    def __init__(self, client: weaviate.WeaviateAsyncClient, collection_name: str) -> None:
        self._client = client
        self._collection_name = collection_name

    async def ensure_schema(self, recreate: bool = False) -> None:
        collections = self._client.collections
        exists = await collections.exists(self._collection_name)
        if exists:
            if recreate:
                await collections.delete(self._collection_name)
            else:
                return
        await collections.create(
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

    async def fetch_existing_page_state(self, page_uid: str) -> Dict[str, Any]:
        collection = self.get_collection()
        state = {
            "page_objects": [],
            "chunk_objects": [],
            "last_synced_edit_time": None,
            "content_hash": None,
        }

        filters = Filter.by_property("page_uid").equal(page_uid)
        try:
            response = await collection.query.fetch_objects(
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
            LOGGER.warning(
                "Failed to fetch existing page state from Weaviate",
                page_uid=page_uid,
                error=str(exc),
                exc_info=exc,
            )
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

    @transient_retry()
    async def delete_stale_objects(self, page_uid: str, content_hash: str) -> None:
        collection = self.get_collection()
        if content_hash:
            filters = Filter.by_property("page_uid").equal(page_uid) & Filter.by_property("content_hash").not_equal(content_hash)
        else:
            filters = Filter.by_property("page_uid").equal(page_uid)
        await collection.data.delete_many(where=filters)

    @transient_retry()
    async def insert_objects(self, objects: Sequence[Dict[str, Any]]) -> List[ErrorObject]:
        collection = self.get_collection()
        if not objects:
            return []

        data_objects: List[DataObject] = []
        object_by_index: Dict[int, Dict[str, Any]] = {}
        for idx, obj in enumerate(objects):
            data_objects.append(
                DataObject(
                    properties=obj["properties"],
                    uuid=obj.get("uuid"),
                    vector=obj.get("vector"),
                )
            )
            object_by_index[idx] = obj

        result = await collection.data.insert_many(data_objects)
        if not result.has_errors:
            return []

        duplicate_substrings = ("already exists", "duplicate", "conflicts with")
        unrecoverable: List[ErrorObject] = []

        for index, error in result.errors.items():
            obj = object_by_index.get(index)
            message = (error.message or "").lower()
            if obj and any(token in message for token in duplicate_substrings):
                try:
                    await collection.data.replace(
                        uuid=obj["uuid"],
                        properties=obj["properties"],
                        vector=obj.get("vector"),
                    )
                    continue
                except Exception as replace_exc:
                    error.message = f"{error.message} | replace failed: {replace_exc}"

            unrecoverable.append(error)

        return unrecoverable

