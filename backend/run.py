
import os
import sys

# Ensure backend directory is in sys.path so modules can be imported
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import uvicorn
from ingestion import seed_january_2026


if __name__ == "__main__":
    # Check Elexon data status. Seeds only if database is unseeded, unless --force is passed.
    force_seed = "--force" in sys.argv
    print("Checking Elexon data status...", flush=True)

    try:
        status = seed_january_2026(force=force_seed)
        print(f"Elexon data status: {status.get('status', 'READY')}", flush=True)
    except Exception as e:
        print(f"Warning: Elexon data check encountered an issue: {e}", flush=True)

    port = int(os.environ.get("PORT", 8001))
    host = os.environ.get("HOST", "0.0.0.0")

    print(
        f"Starting UK Wind Day-Ahead Procurement Intelligence API "
        f"on http://{host}:{port} ...",
        flush=True,
    )

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        app_dir=BACKEND_DIR,
        reload=False,
    )
