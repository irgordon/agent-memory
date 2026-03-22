#!/usr/bin/env python3

import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parent

REQUIRED_PATHS = [
    "execution_memory.yaml",
    "index.yaml",
    "entries",
    "profiles",
    "schemas",
    "tools",
]


def fail(code, detail):
    print(json.dumps({
        "message": "bootstrap failed",
        "stage": "bootstrap",
        "status": "fail",
        "error_code": code,
        "detail": str(detail),
    }))
    sys.exit(1)


def success():
    print(json.dumps({
        "message": "bootstrap complete",
        "stage": "bootstrap",
        "status": "ok",
    }))


def parse_simple_yaml_mapping(path):
    data = {}
    current_parent = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if not line or line.lstrip().startswith("#"):
            continue

        if not raw_line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if value == "":
                data[key] = {}
                current_parent = key
            else:
                if value == "null":
                    parsed = None
                elif value == "true":
                    parsed = True
                elif value == "false":
                    parsed = False
                else:
                    parsed = value
                data[key] = parsed
                current_parent = None
            continue

        if raw_line.startswith("  ") and current_parent and ":" in line:
            key, value = line.strip().split(":", 1)
            value = value.strip()

            if value == "null":
                parsed = None
            elif value == "true":
                parsed = True
            elif value == "false":
                parsed = False
            else:
                parsed = value

            data[current_parent][key] = parsed
            continue

        fail("yaml_parse_error", path.name)

    return data


def parse_index_entries(path):
    entries = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if not line or line.lstrip().startswith("#"):
            continue

        if line == "entries: []":
            return []

        if line == "entries:":
            entries = []
            continue

        if line.startswith("  - "):
            if entries is None:
                fail("index_format_error", path.name)
            entries.append(line[4:].strip())
            continue

        fail("index_format_error", path.name)

    if entries is None:
        fail("missing_entries_key", path.name)

    return entries


def verify_structure():
    for relative_path in REQUIRED_PATHS:
        target = ROOT / relative_path
        if not target.exists():
            fail("missing_required_paths", relative_path)


def verify_single_profile():
    profiles = list((ROOT / "profiles").glob("*.yaml"))
    if len(profiles) != 1:
        fail("invalid_profile_count", len(profiles))


def verify_execution_memory():
    path = ROOT / "execution_memory.yaml"
    data = parse_simple_yaml_mapping(path)

    required_top = {"state", "last_verified_entry", "invariants"}
    if set(data.keys()) != required_top:
        fail("execution_memory_shape_error", sorted(data.keys()))

    invariants = data.get("invariants")
    if not isinstance(invariants, dict):
        fail("execution_memory_invariants_error", "invariants must be a mapping")

    required_invariants = {
        "deterministic_outputs",
        "append_only_ledger",
        "repository_rooted_execution",
        "fail_closed_verification",
        "no_silent_state_repair",
        "no_manual_override",
    }

    if set(invariants.keys()) != required_invariants:
        fail("execution_memory_invariants_error", sorted(invariants.keys()))

    for key, value in invariants.items():
        if value is not True:
            fail("execution_memory_invariant_false", key)

    return data


def verify_index_and_entries():
    index_path = ROOT / "index.yaml"
    entries = parse_index_entries(index_path)

    for entry_id in entries:
        entry_path = ROOT / "entries" / f"{entry_id}.yaml"
        if not entry_path.exists():
            fail("index_entry_missing_file", entry_id)

    return entries


def verify_last_verified_entry(index_entries, execution_memory):
    last_verified_entry = execution_memory.get("last_verified_entry")

    if last_verified_entry is None:
        return

    if last_verified_entry not in index_entries:
        fail("execution_memory_inconsistent", last_verified_entry)


def main():
    verify_structure()
    verify_single_profile()
    execution_memory = verify_execution_memory()
    index_entries = verify_index_and_entries()
    verify_last_verified_entry(index_entries, execution_memory)
    success()


if __name__ == "__main__":
    main()
