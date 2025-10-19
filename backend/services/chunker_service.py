"""
Chunker Service - A dedicated microservice for text chunking.

This service maintains a SemanticChunker instance in memory to avoid
the ~17s initialization cost on every sync run. It provides a REST API
for chunking text using the Chonkie library with IBM Granite embeddings.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from dataclasses import dataclass, asdict
import itertools
import contextvars

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from chonkie import SemanticChunker
import os

from common.logging import configure_logging
import structlog
from funcy import lmap, lsplit, zipdict, ignore
from functools import wraps
configure_logging(json=True)
logger = structlog.get_logger(__name__)


@dataclass
class ChunkerConfig:
    provider: str
    model: str
    threshold: float
    chunk_size: int
    skip_window: int
    min_chunk_size: int
    voyage_model: str
    profile_yappi: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_env(cls) -> "ChunkerConfig":
        defaults = {
            "provider": "granite",
            "model": "ibm-granite/granite-embedding-small-english-r2",
            "threshold": 0.6,
            "chunk_size": 800,
            "skip_window": 1,
            "min_chunk_size": 50,
            "voyage_model": "voyage-3-lite",
            "profile_yappi": False,
        }

        env_overrides = {
            "provider": os.getenv("CHUNKER_EMBEDDING_PROVIDER", "").lower() or None,
            "model": os.getenv("CHUNKER_MODEL") or None,
            "threshold": float(os.getenv("CHUNKER_THRESHOLD")) if os.getenv("CHUNKER_THRESHOLD") else None,
            "chunk_size": int(os.getenv("CHUNKER_CHUNK_SIZE")) if os.getenv("CHUNKER_CHUNK_SIZE") else None,
            "skip_window": int(os.getenv("CHUNKER_SKIP_WINDOW")) if os.getenv("CHUNKER_SKIP_WINDOW") else None,
            "min_chunk_size": int(os.getenv("CHUNKER_MIN_CHUNK_SIZE")) if os.getenv("CHUNKER_MIN_CHUNK_SIZE") else None,
            "voyage_model": os.getenv("CHUNKER_VOYAGE_MODEL") or None,
            "profile_yappi": (os.getenv("CHUNKER_PROFILE_YAPPI") == "1") if os.getenv("CHUNKER_PROFILE_YAPPI") else None,
        }

        env_overrides = {k: v for k, v in env_overrides.items() if v is not None}
        config_dict = {**defaults, **env_overrides}
        return cls(**config_dict)


config = ChunkerConfig.from_env()

if config.profile_yappi:
    import yappi

    yappi.set_clock_type("wall")
    _yappi_tag = contextvars.ContextVar("chunker_yappi_tag", default=None)
    _yappi_counter = itertools.count(1)

    def _tag_callback():
        tag = _yappi_tag.get()
        return tag if tag is not None else 0

    yappi.set_tag_callback(_tag_callback)


def create_chunker(cfg: ChunkerConfig) -> SemanticChunker:
    if cfg.provider == "voyageai":
        from chonkie import VoyageAIEmbeddings
        import numpy as np
        import chonkie.embeddings.voyageai as voyage_module
        import chonkie.embeddings.base as embeddings_base_module

        voyage_module.np = np
        embeddings_base_module.np = np

        embeddings = VoyageAIEmbeddings(model=cfg.voyage_model)
        return SemanticChunker(embeddings)
    else:
        return SemanticChunker(
            embedding_model=cfg.model,
            threshold=cfg.threshold,
            chunk_size=cfg.chunk_size,
            skip_window=cfg.skip_window,
            min_chunk_size=cfg.min_chunk_size,
        )


class ChunkerService:
    def __init__(self):
        self.chunker: Optional[SemanticChunker] = None
        self.lock: Optional[asyncio.Lock] = None
        self.init_time: float = 0
        self.config: ChunkerConfig = config

    async def initialize(self) -> None:
        start_time = time.time()
        logger.info("Initializing SemanticChunker...")

        self.chunker = create_chunker(self.config)
        self.lock = asyncio.Lock()
        self.init_time = time.time() - start_time

        logger.info(f"SemanticChunker initialized in {self.init_time:.2f} seconds")
        logger.info(f"Configuration: {self.config.to_dict()}")

    async def chunk_single(self, text: str) -> List[Any]:
        if self.chunker is None or self.lock is None:
            raise RuntimeError("Chunker not initialized")

        async with self.lock:
            return await asyncio.to_thread(self.chunker.chunk, text)

    async def chunk_batch(self, texts: List[str]) -> List[List[Any]]:
        if self.chunker is None or self.lock is None:
            raise RuntimeError("Chunker not initialized")

        async with self.lock:
            return await asyncio.to_thread(self.chunker.chunk_batch, texts)

    def is_ready(self) -> bool:
        return self.chunker is not None and self.lock is not None

    async def shutdown(self) -> None:
        logger.info("Shutting down ChunkerService")
        self.chunker = None
        self.lock = None


service = ChunkerService()


def profile_if_enabled(func):
    """Decorator that optionally profiles async route handlers with yappi.

    Preserves async signature so FastAPI awaits the result correctly.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not config.profile_yappi:
            return await func(*args, **kwargs)

        # Profiling path
        profiler_tag = next(_yappi_counter)
        profiler_token = _yappi_tag.set(profiler_tag)
        yappi.clear_stats()
        yappi.start(profile_threads=True)
        try:
            return await func(*args, **kwargs)
        finally:
            yappi.stop()
            stats = yappi.get_func_stats(filter_callback=lambda s: s.tag == profiler_tag)
            stats.sort("ttot")
            log_path = f"/tmp/yappi_{func.__name__}_{profiler_tag}.log"
            write_stats = ignore(OSError, default=None)(
                lambda: stats.print_all(out=open(log_path, "w"))
            )
            write_stats()
            yappi.clear_stats()
            _yappi_tag.reset(profiler_token)
    return wrapper


class ChunkRequest(BaseModel):
    text: str = Field(..., description="The text to chunk")


class Chunk(BaseModel):
    text: str = Field(...)
    start_index: int = Field(...)
    end_index: int = Field(...)
    token_count: int = Field(...)


class ChunkResult(BaseModel):
    chunks: List[Chunk]
    processing_time_ms: float


class HealthResponse(BaseModel):
    status: str
    chunker_loaded: bool
    chunker_init_time_seconds: float
    chunker_config: Dict[str, Any]
    uptime_seconds: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await service.initialize()
    except Exception as e:
        logger.error(f"Failed to initialize ChunkerService: {e}")
        raise

    yield

    await service.shutdown()


app = FastAPI(
    title="Chunker Service",
    description="A microservice for semantic text chunking using Chonkie and IBM Granite embeddings",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

service_start_time = time.time()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        chunker_loaded=service.is_ready(),
        chunker_init_time_seconds=service.init_time,
        chunker_config=service.config.to_dict(),
        uptime_seconds=round(time.time() - service_start_time, 2),
    )


@app.post("/chunk", response_model=ChunkResult)
@profile_if_enabled
async def chunk_text(request: ChunkRequest):
    if not service.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Chunker service is still initializing. Please try again in a moment.",
        )

    start = time.time()
    try:
        raw_chunks = await service.chunk_single(request.text)
        processing_time_ms = round((time.time() - start) * 1000, 2)
        return ChunkResult(
            chunks=lmap(lambda ch: Chunk(text=ch.text, start_index=ch.start_index, end_index=ch.end_index, token_count=ch.token_count), raw_chunks),
            processing_time_ms=processing_time_ms,
        )
    except Exception as e:  # pragma: no cover
        logger.error(f"Chunking failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to chunk text: {str(e)}")


@app.get("/")
async def root():
    return {
        "service": "Chunker Service",
        "version": "1.0.0",
        "status": "running",
        "chunker_loaded": service.is_ready(),
        "endpoints": {"health": "/health", "chunk": "/chunk (POST)", "docs": "/docs"},
    }


class BatchChunkRequest(BaseModel):
    texts: List[str]


class BatchChunkResult(BaseModel):
    results: List[ChunkResult]
    total_texts: int
    total_processing_time_ms: float


@app.post("/chunk/batch", response_model=BatchChunkResult)
@profile_if_enabled
async def chunk_batch(request: BatchChunkRequest):
    if not service.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Chunker service is still initializing. Please try again in a moment.",
        )

    start_time = time.time()

    def _filter_non_empty(texts: List[str]) -> tuple[List[int], List[str]]:
        kept, _ = lsplit(lambda p: bool(p[1] and p[1].strip()), enumerate(texts))
        indices = [i for i, _ in kept]
        non_empty = [t for _, t in kept]
        return indices, non_empty

    def _to_chunk(chunk: Any) -> Chunk:
        return Chunk(
            text=chunk.text,
            start_index=chunk.start_index,
            end_index=chunk.end_index,
            token_count=chunk.token_count,
        )

    def _to_chunk_result(chunks: List[Any]) -> ChunkResult:
        return ChunkResult(
            chunks=lmap(_to_chunk, chunks),
            processing_time_ms=0,
        )

    def _reassociate_results(indices: List[int], responses: List[ChunkResult], total: int) -> List[ChunkResult]:
        results = [ChunkResult(chunks=[], processing_time_ms=0) for _ in range(total)]
        mapped = zipdict(indices, responses)
        for idx, response in mapped.items():
            results[idx] = response
        return results

    indices, non_empty_texts = _filter_non_empty(request.texts)

    if non_empty_texts:
        try:
            batch_chunks = await service.chunk_batch(non_empty_texts)
            responses = lmap(_to_chunk_result, batch_chunks)
            results = _reassociate_results(indices, responses, len(request.texts))
        except Exception:
            logger.exception("Batch chunking failed, falling back to sequential")
            results = [ChunkResult(chunks=[], processing_time_ms=0) for _ in request.texts]
            for idx in indices:
                try:
                    chunks = await service.chunk_single(request.texts[idx])
                    results[idx] = _to_chunk_result(chunks)
                except Exception:
                    logger.exception(f"Failed to chunk text at index {idx}")
    else:
        results = [ChunkResult(chunks=[], processing_time_ms=0) for _ in request.texts]

    total_time = (time.time() - start_time) * 1000

    return BatchChunkResult(
        results=results,
        total_texts=len(request.texts),
        total_processing_time_ms=round(total_time, 2),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
