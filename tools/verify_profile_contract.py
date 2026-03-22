#!/usr/bin/env python3

import json
import sys
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

PROFILE_DIR = ROOT / "profiles"
SCHEMA_PATH = ROOT / "schemas" / "profile.schema.yaml"

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def fail(code, detail):
    print(json.dumps({
        "message": "profile verification failed",
        "stage": "verify_profile",
        "status": "fail",
        "error_code": code,
        "detail": str(detail)
    }))
    sys.exit(1)

def success():
    print(json.dumps({
        "message": "profile verification passed",
        "stage": "verify_profile",
        "status": "ok"
    }))

def main():
    profiles = list(PROFILE_DIR.glob("*.yaml"))

    if len(profiles) != 1:
        fail("invalid_profile_count", len(profiles))

    profile = load_yaml(profiles[0])
    schema = load_yaml(SCHEMA_PATH)

    required = schema.get("required", [])

    for field in required:
        if field not in profile:
            fail("missing_required_field", field)

    success()

if __name__ == "__main__":
    main()
