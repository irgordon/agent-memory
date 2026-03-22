#!/usr/bin/env python3

import json
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

REQUIRED_PATHS = [
    "execution_memory.yaml",
    "index.yaml",
    "entries",
    "profiles",
    "schemas",
    "tools",
]

def verify_structure():
    for path in REQUIRED_PATHS:
        if not (ROOT / path).exists():
            fail("missing_required_paths", path)

def verify_single_profile():
    profiles = list((ROOT / "profiles").glob("*.yaml"))

    if len(profiles) != 1:
        fail("invalid_profile_count", len(profiles))

def verify_index_consistency():
    index = ROOT / "index.yaml"

    if not index.exists():
        fail("missing_index", "index.yaml")

def success():
    print(json.dumps({
        "message": "bootstrap complete",
        "stage": "bootstrap",
        "status": "ok"
    }))

def fail(code, detail):
    print(json.dumps({
        "message": "bootstrap failed",
        "stage": "bootstrap",
        "status": "fail",
        "error_code": code,
        "detail": str(detail)
    }))
    sys.exit(1)

def main():
    verify_structure()
    verify_single_profile()
    verify_index_consistency()
    success()

if __name__ == "__main__":
    main()
