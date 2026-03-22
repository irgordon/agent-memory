# Agent Memory Skill

Purpose:
This repository provides a reliable way to keep track of long‑running work and the decisions behind it.

This repository implements:

- append-only execution ledger
- deterministic bootstrap verification
- schema-driven profile validation
- fail-closed recovery protocol
- repository-rooted execution model

The system behaves as a state machine over repository files.

No host discovery.
No silent repair.
No implicit authority.

---

## Initialization

Run:

    python bootstrap.py

Expected output:

    {"message": "bootstrap complete", "stage": "bootstrap", "status": "ok"}

If bootstrap fails:

Do not modify files.

Follow:

    references/RECOVERY.md
