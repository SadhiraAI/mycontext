#!/usr/bin/env python3
"""Start the backend on the canonical port (from app config). Ensures a single source of truth."""
import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    _root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(_root))
    os.chdir(_root)

    from app.config import get_settings

    port = get_settings().port
    print(f"Starting backend on port {port} (canonical - frontend proxies /api to this)")
    print(f"  -> http://127.0.0.1:{port}")
    print("  Stop any other uvicorn processes on 8000 or 8002 first.\n")

    subprocess.run([
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", "127.0.0.1", "--port", str(port), "--reload", "--reload-dir", "app",
    ])
