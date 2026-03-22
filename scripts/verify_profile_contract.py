#!/usr/bin/env python3

import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
PROFILE_DIR = ROOT / "profiles"
SCHEMA_PATH = ROOT / "schemas" / "profile.schema.yaml"


def fail(code, detail):
    print(json.dumps({
        "message": "profile verification failed",
        "stage": "verify_profile",
        "status": "fail",
        "error_code": code,
        "detail": str(detail),
    }))
    sys.exit(1)


def success():
    print(json.dumps({
        "message": "profile verification passed",
        "stage": "verify_profile",
        "status": "ok",
    }))


def parse_simple_yaml(path):
    root = {}
    current_top = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if not line or line.lstrip().startswith("#"):
            continue

        if not raw_line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if value == "":
                root[key] = {}
                current_top = key
            else:
                root[key] = value
                current_top = None
            continue

        if raw_line.startswith("  ") and current_top and ":" in line:
            key, value = line.strip().split(":", 1)
            root[current_top][key.strip()] = value.strip()
            continue

        fail("yaml_parse_error", path.name)

    return root


def load_required_fields(schema_path):
    required = []
    in_required = False

    for raw_line in schema_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if not line or line.lstrip().startswith("#"):
            continue

        if line == "required:":
            in_required = True
            continue

        if in_required and line.startswith("  - "):
            required.append(line[4:].strip())
            continue

        if in_required and not line.startswith("  - "):
            break

    if not required:
        fail("schema_required_missing", schema_path.name)

    return required


def main():
    profiles = list(PROFILE_DIR.glob("*.yaml"))
    if len(profiles) != 1:
        fail("invalid_profile_count", len(profiles))

    profile = parse_simple_yaml(profiles[0])
    required_fields = load_required_fields(SCHEMA_PATH)

    for field in required_fields:
        if field not in profile:
            fail("missing_required_field", field)

    success()


if __name__ == "__main__":
    main()
