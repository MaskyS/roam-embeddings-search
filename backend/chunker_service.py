"""
Chunker Service - A dedicated microservice for text chunking.

This service maintains a SemanticChunker instance in memory to avoid
the ~17s initialization cost on every sync run. It provides a REST API
for chunking text using the Chonkie library with IBM Granite embeddings.
"""

import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
import itertools
import contextvars

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from chonkie import SemanticChunker
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
CHUNKER_PROVIDER = os.getenv("CHUNKER_EMBEDDING_PROVIDER", "granite").lower()
CHUNKER_MODEL = os.getenv(
    "CHUNKER_MODEL", "ibm-granite/granite-embedding-small-english-r2"
)
CHUNKER_THRESHOLD = float(os.getenv("CHUNKER_THRESHOLD", "0.6"))
CHUNKER_CHUNK_SIZE = int(os.getenv("CHUNKER_CHUNK_SIZE", "800"))
CHUNKER_SKIP_WINDOW = int(os.getenv("CHUNKER_SKIP_WINDOW", "1"))
CHUNKER_MIN_CHUNK_SIZE = int(os.getenv("CHUNKER_MIN_CHUNK_SIZE", "50"))
CHUNKER_VOYAGE_MODEL = os.getenv("CHUNKER_VOYAGE_MODEL", "voyage-3-lite")
CHUNKER_PROFILE_YAPPI = os.getenv("CHUNKER_PROFILE_YAPPI", "0") == "1"

if CHUNKER_PROFILE_YAPPI:
    import yappi

    yappi.set_clock_type("wall")
    _yappi_tag = contextvars.ContextVar("chunker_yappi_tag", default=None)
    _yappi_counter = itertools.count(1)

    def _tag_callback():
        tag = _yappi_tag.get()
        return tag if tag is not None else 0

    yappi.set_tag_callback(_tag_callback)

if CHUNKER_PROVIDER == "voyageai":
    import numpy as np  # ensure voyageai embeddings have numpy available

# Global chunker instance
chunker: Optional[SemanticChunker] = None
chunker_init_time: float = 0
chunker_config: Dict[str, Any] = {}
chunker_lock: Optional[asyncio.Lock] = None


# --- Request/Response Models ---


class ChunkRequest(BaseModel):
    """Request model for chunking a single text."""

    text: str = Field(..., description="The text to chunk")


class ChunkResponse(BaseModel):
    """Response model for a single chunk."""

    text: str = Field(..., description="The chunk text")
    start_index: int = Field(..., description="Start character index in original text")
    end_index: int = Field(..., description="End character index in original text")
    token_count: int = Field(..., description="Number of tokens in the chunk")


class ChunkingResponse(BaseModel):
    """Response model for chunking operation."""

    chunks: List[ChunkResponse] = Field(..., description="List of text chunks")
    total_chunks: int = Field(..., description="Total number of chunks created")
    processing_time_ms: float = Field(
        ..., description="Time taken to chunk in milliseconds"
    )


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = Field(..., description="Service status")
    chunker_loaded: bool = Field(..., description="Whether chunker is initialized")
    chunker_init_time_seconds: float = Field(
        ..., description="Time taken to initialize chunker"
    )
    chunker_config: Dict[str, Any] = Field(
        ..., description="Current chunker configuration"
    )
    uptime_seconds: float = Field(..., description="Service uptime in seconds")


# --- FastAPI Application ---


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize chunker on startup, clean up on shutdown."""
    global chunker, chunker_init_time, chunker_config, chunker_lock

    logger.info("Initializing SemanticChunker...")
    start_time = time.time()

    try:
        if CHUNKER_PROVIDER == "voyageai":
            from chonkie import VoyageAIEmbeddings
            import numpy as np
            import chonkie.embeddings.voyageai as voyage_module
            import chonkie.embeddings.base as embeddings_base_module

            voyage_module.np = np
            embeddings_base_module.np = np
            embeddings = VoyageAIEmbeddings(model=CHUNKER_VOYAGE_MODEL)
            chunker = SemanticChunker(embeddings)
            chunker_config = {
                "provider": "voyageai",
                "model": CHUNKER_VOYAGE_MODEL,
            }
        else:
            chunker_config = {
                "provider": "granite",
                "model": CHUNKER_MODEL,
                "threshold": CHUNKER_THRESHOLD,
                "chunk_size": CHUNKER_CHUNK_SIZE,
                "skip_window": CHUNKER_SKIP_WINDOW,
                "min_chunk_size": CHUNKER_MIN_CHUNK_SIZE,
            }

            chunker = SemanticChunker(
                embedding_model=CHUNKER_MODEL,
                threshold=CHUNKER_THRESHOLD,
                chunk_size=CHUNKER_CHUNK_SIZE,
                skip_window=CHUNKER_SKIP_WINDOW,
                min_chunk_size=CHUNKER_MIN_CHUNK_SIZE,
            )
        chunker_lock = asyncio.Lock()

        chunker_init_time = time.time() - start_time
        logger.info(f"SemanticChunker initialized in {chunker_init_time:.2f} seconds")
        logger.info(f"Configuration: {chunker_config}")
        if chunker_config.get("provider") != CHUNKER_PROVIDER:
            logger.warning(
                "Requested provider '%s' but initialized '%s'. Using fallback.",
                CHUNKER_PROVIDER,
                chunker_config.get("provider"),
            )

    except Exception as e:
        logger.error(f"Failed to initialize SemanticChunker: {e}")
        raise

    yield

    logger.info("Shutting down Chunker Service")
    chunker = None
    chunker_lock = None


app = FastAPI(
    title="Chunker Service",
    description="A microservice for semantic text chunking using Chonkie and IBM Granite embeddings",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Track service start time
service_start_time = time.time()


# --- API Endpoints ---


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service status and chunker initialization.
    """
    return HealthResponse(
        status="healthy" if chunker is not None else "initializing",
        chunker_loaded=chunker is not None,
        chunker_init_time_seconds=chunker_init_time,
        chunker_config=chunker_config,
        uptime_seconds=time.time() - service_start_time,
    )


@app.post("/chunk", response_model=ChunkingResponse)
async def chunk_text(request: ChunkRequest):
    """
    Chunk a text into semantically coherent segments.

    Args:
        request: ChunkRequest containing the text to chunk

    Returns:
        ChunkingResponse with list of chunks and metadata

    Raises:
        HTTPException: If chunker is not initialized or chunking fails
    """
    if chunker is None or chunker_lock is None:
        raise HTTPException(
            status_code=503,
            detail="Chunker service is still initializing. Please try again in a moment.",
        )

    if not request.text or not request.text.strip():
        return ChunkingResponse(chunks=[], total_chunks=0, processing_time_ms=0)

    start_time = time.time()

    profiler_token = None
    profiler_tag = None
    if CHUNKER_PROFILE_YAPPI:
        profiler_tag = next(_yappi_counter)
        profiler_token = _yappi_tag.set(profiler_tag)
        yappi.clear_stats()
        yappi.start(profile_threads=True)

    try:
        # Perform chunking (serialize access to shared chunker instance)
        async with chunker_lock:
            chunks = await asyncio.to_thread(chunker.chunk, request.text)

        # Convert chunks to response format
        chunk_responses = []
        for chunk in chunks:
            chunk_responses.append(
                ChunkResponse(
                    text=chunk.text,
                    start_index=chunk.start_index,
                    end_index=chunk.end_index,
                    token_count=chunk.token_count,
                )
            )

        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        return ChunkingResponse(
            chunks=chunk_responses,
            total_chunks=len(chunk_responses),
            processing_time_ms=round(processing_time, 2),
        )

    except Exception as e:
        logger.error(f"Chunking failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to chunk text: {str(e)}")
    finally:
        if CHUNKER_PROFILE_YAPPI and profiler_tag is not None:
            yappi.stop()
            stats = yappi.get_func_stats(
                filter_callback=lambda s: s.tag == profiler_tag
            )
            stats.sort("ttot")
            log_path = f"/tmp/yappi_chunk_{profiler_tag}.log"
            try:
                with open(log_path, "w") as f:
                    stats.print_all(out=f)
            except OSError as exc:
                logger.error(f"Failed to write yappi stats: {exc}")
            finally:
                yappi.clear_stats()
                if profiler_token is not None:
                    _yappi_tag.reset(profiler_token)


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Chunker Service",
        "version": "1.0.0",
        "status": "running",
        "chunker_loaded": chunker is not None,
        "endpoints": {"health": "/health", "chunk": "/chunk (POST)", "docs": "/docs"},
    }


# --- Batch Endpoint (Future Enhancement) ---


class BatchChunkRequest(BaseModel):
    """Request model for chunking multiple texts."""

    texts: List[str] = Field(..., description="List of texts to chunk")


class BatchChunkResponse(BaseModel):
    """Response model for batch chunking."""

    results: List[ChunkingResponse] = Field(
        ..., description="Chunking results for each text"
    )
    total_texts: int = Field(..., description="Number of texts processed")
    total_processing_time_ms: float = Field(
        ..., description="Total processing time in milliseconds"
    )


@app.post("/chunk/batch", response_model=BatchChunkResponse)
async def chunk_batch(request: BatchChunkRequest):
    """
    Chunk multiple texts in a single request.

    This is more efficient than making multiple individual requests
    as it amortizes the network overhead.
    """
    if chunker is None or chunker_lock is None:
        raise HTTPException(
            status_code=503,
            detail="Chunker service is still initializing. Please try again in a moment.",
        )

    start_time = time.time()

    # Filter out empty texts but keep track of indices
    non_empty_texts = []
    non_empty_indices = []
    for i, text in enumerate(request.texts):
        if text and text.strip():
            non_empty_texts.append(text)
            non_empty_indices.append(i)

    # Use Chonkie's native batch processing
    results = [
        ChunkingResponse(chunks=[], total_chunks=0, processing_time_ms=0)
        for _ in request.texts
    ]

    if non_empty_texts:
        profiler_token = None
        profiler_tag = None
        if CHUNKER_PROFILE_YAPPI:
            profiler_tag = next(_yappi_counter)
            profiler_token = _yappi_tag.set(profiler_tag)
            yappi.clear_stats()
            yappi.start(profile_threads=True)

        try:
            # Process all non-empty texts at once using chunk_batch
            async with chunker_lock:
                batch_chunks = await asyncio.to_thread(
                    chunker.chunk_batch, non_empty_texts
                )

            # Map results back to original indices
            for idx, doc_chunks in zip(non_empty_indices, batch_chunks):
                chunk_responses = [
                    ChunkResponse(
                        text=chunk.text,
                        start_index=chunk.start_index,
                        end_index=chunk.end_index,
                        token_count=chunk.token_count,
                    )
                    for chunk in doc_chunks
                ]

                results[idx] = ChunkingResponse(
                    chunks=chunk_responses,
                    total_chunks=len(chunk_responses),
                    processing_time_ms=0,  # Will be calculated from total time
                )

        except Exception as e:
            logger.exception("Batch chunking failed")
            # Fall back to sequential processing if batch fails
            for idx in non_empty_indices:
                try:
                    async with chunker_lock:
                        chunks = await asyncio.to_thread(
                            chunker.chunk, request.texts[idx]
                        )
                    chunk_responses = [
                        ChunkResponse(
                            text=chunk.text,
                            start_index=chunk.start_index,
                            end_index=chunk.end_index,
                            token_count=chunk.token_count,
                        )
                        for chunk in chunks
                    ]
                    results[idx] = ChunkingResponse(
                        chunks=chunk_responses,
                        total_chunks=len(chunk_responses),
                        processing_time_ms=0,
                    )
                except Exception as e2:
                    logger.exception(f"Failed to chunk text at index {idx}")
        finally:
            if CHUNKER_PROFILE_YAPPI and profiler_tag is not None:
                yappi.stop()
                stats = yappi.get_func_stats(
                    filter_callback=lambda s: s.tag == profiler_tag
                )
                stats.sort("ttot")
                log_path = f"/tmp/yappi_chunk_batch_{profiler_tag}.log"
                try:
                    with open(log_path, "w") as f:
                        stats.print_all(out=f)
                except OSError as exc:
                    logger.error(f"Failed to write yappi stats: {exc}")
                finally:
                    yappi.clear_stats()
                    if profiler_token is not None:
                        _yappi_tag.reset(profiler_token)

    total_time = (time.time() - start_time) * 1000

    return BatchChunkResponse(
        results=results,
        total_texts=len(request.texts),
        total_processing_time_ms=round(total_time, 2),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
