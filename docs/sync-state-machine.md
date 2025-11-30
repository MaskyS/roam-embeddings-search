# Sync Job State Machine

## State Diagram

```
                     ┌─────────┐
                     │  IDLE   │
                     │         │
                     │ Initial │
                     │ state   │
                     └────┬────┘
                          │
                          │ POST /sync/start
                          │ (creates asyncio.Task)
                          │
                          ▼
                     ┌─────────┐
         ┌──────────│ RUNNING │──────────┐
         │          │         │          │
         │          │ Sync in │          │
         │          │ progress│          │
         │          └────┬────┘          │
         │               │               │
         │               │               │
    POST /sync/cancel    │          Sync completes
    (sets cancel flag)   │          successfully
         │               │               │
         │          Exception            │
         │          raised               │
         │               │               │
         ▼               ▼               ▼
   ┌────────────┐  ┌─────────┐    ┌─────────┐
   │ CANCELLING │  │ FAILED  │    │ SUCCESS │
   │            │  │         │    │         │
   │ Waiting    │  │ Error   │    │ Summary │
   │ for task   │  │ recorded│    │ recorded│
   │ to exit    │  │         │    │         │
   └──────┬─────┘  └─────────┘    └─────────┘
          │              │              │
          │              │              │
     Task catches        │              │
     CancelledError      │              │
          │              │              │
          ▼              │              │
    ┌───────────┐        │              │
    │ CANCELLED │        │              │
    │           │        │              │
    │ Final     │        │              │
    │ state     │        │              │
    └───────────┘        │              │
                         │              │
                         ▼              ▼
                    ┌───────────────────────┐
                    │  Ready for next run   │
                    │  (status reset to     │
                    │   idle on next start) │
                    └───────────────────────┘
```

## Valid State Transitions

| From | To | Trigger | API |
|------|-----|---------|-----|
| `idle` | `running` | User starts sync | `POST /sync/start` |
| `running` | `success` | Sync completes without error | Internal |
| `running` | `failed` | Unhandled exception during sync | Internal |
| `running` | `cancelling` | User requests cancellation | `POST /sync/cancel` |
| `cancelling` | `cancelled` | Task acknowledges cancel signal | Internal |
| Any terminal | `running` | User starts new sync | `POST /sync/start` |

## State Definitions

### `idle`
- **Description**: No sync operation in progress
- **Entry condition**: Application startup, or after previous sync terminal state
- **Job data**: May contain summary from last run
- **Allowed actions**: Start new sync

### `running`
- **Description**: Sync operation actively processing
- **Entry condition**: POST /sync/start called
- **Job data**:
  - `run_id`: Unique identifier for this run
  - `mode`: "full", "since", or "limit"
  - `params`: Configuration used
  - `started_at`: ISO timestamp
  - `progress`: Live progress updates
- **Allowed actions**: Cancel, check status

### `cancelling`
- **Description**: Cancel requested, waiting for task to exit
- **Entry condition**: POST /sync/cancel while running
- **Job data**:
  - `error`: "cancel requested"
- **Allowed actions**: Check status (cancel already in progress)

### `success`
- **Description**: Sync completed successfully
- **Entry condition**: Sync task returns without exception
- **Job data**:
  - `finished_at`: ISO timestamp
  - `summary`: Full sync results
    - `total_pages`: Pages in graph
    - `processed`: Pages examined
    - `updated`: Pages synced
    - `skipped_since`: Filtered by --since
    - `skipped_content`: Filtered by content hash
    - `failed`: Pages that errored
    - `cursor_max_edit_time`: For next incremental
- **Allowed actions**: Start new sync

### `failed`
- **Description**: Sync terminated due to error
- **Entry condition**: Unhandled exception in sync task
- **Job data**:
  - `finished_at`: ISO timestamp
  - `error`: Error message
  - `summary`: Partial results (if available)
- **Allowed actions**: Start new sync

### `cancelled`
- **Description**: Sync was cancelled by user
- **Entry condition**: Task caught CancelledError
- **Job data**:
  - `finished_at`: ISO timestamp
  - `error`: "cancelled"
- **Allowed actions**: Start new sync

## Concurrency Guard

A single `asyncio.Lock` prevents concurrent sync operations:

```python
async with lock:
    if job.get("status") == "running":
        raise HTTPException(409, "Sync already in progress")
    # Start new sync
```

This ensures:
- Only one sync can run at a time
- Status checks are atomic
- No race conditions between start/cancel

## Progress Updates

During `running` state, progress is updated via callbacks:

```python
{
    "event": "batch_complete",
    "batch": 3,
    "processed": {"processed": 150, "total": 500, "percent": 30.0},
    "stats": {"pages_updated": 148, "pages_failed": 2},
    "timestamp": "2024-01-15T10:30:00Z"
}
```

Events include:
- `uids_loaded`: Initial page count known
- `metadata_filtered`: After skip filtering
- `batch_start`: Batch processing begins
- `batch_complete`: Batch processing done
- `chunker_ready`: Chunker service connected
- `since_applied`: --since filter active

## API Reference

### Start Sync
```bash
POST /sync/start
Content-Type: application/json

{
    "mode": "since",         # "full", "since", or "limit"
    "since": 1705000000000,  # Optional: epoch ms filter
    "limit": 100,            # For mode="limit"
    "clear": false,          # Delete collection first
    "recreate_collection": false,
    "resume": false,         # Resume from checkpoint
    "state_file": "/path/to/state.json"
}
```

Response: `202 Accepted` with job state

### Check Status
```bash
GET /sync/status
```

Response: Current job state including progress

### Cancel Sync
```bash
POST /sync/cancel
```

Response: Job state with `status: "cancelling"`

### View History
```bash
GET /sync/runs?limit=10
```

Response: List of recent sync runs from SQLite

## Resume Behavior

If a sync fails mid-run:

1. State file contains:
   - `pending_page_uids`: Remaining pages
   - `processed_count`: Already processed
   - `since`: Original --since value

2. On resume (`resume: true`):
   - Loads state from file
   - Skips already-processed pages
   - Continues from where it stopped

3. On success:
   - State file is deleted
   - SQLite page_state is authoritative
