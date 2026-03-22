# Recovery Protocol

This procedure governs all recovery actions.

Recovery is a controlled state transition.
Recovery is never implicit.
Recovery must be recorded as a ledger entry.

---

## When Recovery Is Allowed

Recovery may execute only when:

1. verification has failed
2. repository state is inconsistent
3. recovery entry will be recorded

---

## Recovery Steps

Step 1 — Stop execution

Do not modify files.

Step 2 — Identify failure

Read bootstrap output.

Example:

    error_code: missing_required_paths

Step 3 — Correct repository state

Restore missing or invalid files.

Do not modify existing entries.

Step 4 — Record recovery entry

Create:

    entries/ENTRY-YYYY-MM-DD-NNN.yaml

Action:

    recovery

Step 5 — Re-run bootstrap

    python bootstrap.py

---

## Prohibited Actions

Recovery must never:

- edit existing entries
- reorder ledger history
- bypass verification
- silently repair state
- invent missing data
