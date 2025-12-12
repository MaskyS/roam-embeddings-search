# Render Deployment Guide

Deploy the Roam Semantic Search system to [Render](https://render.com/) with one click using the `render.yaml` blueprint.

## Prerequisites

- Render account with billing information added. Hobby tier is enough but instances will require Starter plan.
- Weaviate Cloud instance (for vector storage)
- VoyageAI API key (for embeddings)
- Roam Research API token

## One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/MaskyS/roam-embeddings-search)

Click the button above to deploy. You'll be prompted to:
1. Set a **Blueprint Name** (can be anything you like)
2. Set the **Branch** to `main` (important: must be `main`)
3. Enter the required API keys listed below:

### Required Environment Variables

**For Chunker Service:**
- `VOYAGE_API_KEY` - Your VoyageAI API key

**For Backend Service:**
- `ROAM_API_TOKEN` - Your Roam Research API token
- `ROAM_GRAPH_NAME` - Your Roam graph name
- `VOYAGEAI_API_KEY` - Your VoyageAI API key (same as chunker)
- `WEAVIATE_CLOUD_URL` - Your Weaviate Cloud instance URL (REST Endpoint)
- `WEAVIATE_CLOUD_API_KEY` - Your Weaviate Cloud API key with admin role

> **⚠️ Important:** When pasting environment variable values in Render's UI, ensure there are **no extra spaces or newlines** before or after the values. Trailing whitespace can cause authentication failures and service errors.

All other settings are pre-configured in the `render.yaml` file.

Once both services have been successfully deployed, copy the instance URL of the web service `roam-semantic-backend-<ID>` and use it as backend URL for the Roam extension. The URL looks like `https://roam-semantic-backend-<ID>.onrender.com`

## What Gets Deployed

The blueprint creates two services:

### 1. roam-semantic-chunker
- **Purpose:** Text chunking with semantic boundaries
- **Runtime:** Prebuilt Docker image from GHCR
- **Plan:** Starter
- **Health Check:** `/health`

**Pre-configured Settings:**
- VoyageAI-based chunking (low memory: ~150-250MB)
- Chunk size: 800 tokens
- Similarity threshold: 0.6
- Minimum chunk size: 50 tokens
- Skip window: 1

### 2. roam-semantic-backend
- **Purpose:** Search and sync API
- **Runtime:** Prebuilt Docker image from GHCR
- **Plan:** Starter
- **Health Check:** `/health`
- **Persistent Disk:** 1 GB at `/app/data` (stores sync state and SQLite DB)

**Pre-configured Settings:**
- Connected to chunker service via internal URL
- Weaviate collection: `RoamSemanticChunks`
- Hybrid search enabled (BM25 + vector)
- VoyageAI reranking for improved relevance

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Render Platform                         │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │  roam-semantic-     │      │  roam-semantic-     │       │
│  │  chunker            │◄─────┤  backend            │       │
│  │  (internal only)    │      │  (public API)       │       │
│  └─────────────────────┘      └───────────┬─────────┘       │
│                                           │                 │
│                                  ┌────────▼────────┐        │
│                                  │ Persistent Disk │        │
│                                  │   /app/data     │        │
│                                  └─────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                   │                        │
                   ▼                        ▼
         ┌─────────────────┐    ┌─────────────────────┐
         │  VoyageAI API   │    │  Weaviate Cloud     │
         │  (embeddings)   │    │  (vector storage)   │
         └─────────────────┘    └─────────────────────┘
                                          │
                                          ▼
                              ┌─────────────────────┐
                              │  Roam Research API  │
                              │  (graph data)       │
                              └─────────────────────┘
```

## Service Communication

- **Chunker ↔ Backend:** Uses Render's internal networking (`http://roam-semantic-chunker-<ID>:8000`)
- **Backend → External APIs:** Public internet (VoyageAI, Weaviate Cloud, Roam)
- **User → Backend:** Public HTTPS endpoint provided by Render
