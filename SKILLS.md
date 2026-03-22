---
name: agent-memory
description: Deterministic memory and governance substrate for long-running agent work. Use when the user asks to set up agent memory, initialize a governed repo, create an execution ledger, bootstrap agent state, add a ledger entry, recover governed state after verification failure, or establish deterministic governance for multi-session engineering workflows. Make sure to use this skill whenever the user wants persistent, append-only, fail-closed execution state for agent work, even if they do not explicitly say "agent memory."
---

# Agent Memory

A deterministic governance and memory substrate for long-running agent workflows.

This skill creates and manages a repository-rooted execution memory system with:

- append-only ledger entries
- explicit execution state
- profile-based governance
- deterministic bootstrap verification
- fail-closed recovery
- no silent state repair

The repository is treated as a governed state machine, not as an informal scratchpad.

## When to use this skill

Use this skill when the user wants any of the following:

- a governed repository for long-running work
- persistent agent state across sessions
- an execution ledger
- deterministic operational memory
- explicit recovery rules
- profile-verified execution constraints
- append-only history for engineering or architecture work

This skill is especially appropriate for systems engineering, microkernel development, architecture governance, harness-driven repos, and any project where correctness and auditability matter more than convenience.

## Skill structure

Read and use the bundled resources:

- `assets/` contains canonical repo files and templates
- `scripts/` contains deterministic bootstrap and verification tools
- `references/RECOVERY.md` defines the fail-closed recovery protocol

## Operating model

The governed repo has this canonical structure after initialization:

```text
<target>/
├── CHANGELOG.md
├── bootstrap.py
├── execution_memory.yaml
├── index.yaml
├── entries/
│   └── ENTRY_TEMPLATE.yaml
├── profiles/
│   └── general.yaml
├── schemas/
│   ├── profile.schema.yaml
│   └── entry.schema.yaml
└── tools/
    └── verify_profile_contract.py
````

The repo behaves as a deterministic state machine over repository-local files.

## Invariants

These must hold at all times:

* `deterministic_outputs`
* `append_only_ledger`
* `repository_rooted_execution`
* `fail_closed_verification`
* `no_silent_state_repair`
* `no_manual_override`

## Prohibited actions

Never:

* edit an existing ledger entry
* reorder ledger history
* continue after verification failure
* silently repair corrupted state
* infer missing profile fields
* treat host discovery as authority
* bypass profile verification

## Initialization procedure

When the user asks to initialize agent memory, create the target directory and copy all canonical files from `assets/` and `scripts/` into the target repo.

Copy these assets:

* `assets/execution_memory.yaml` → `<target>/execution_memory.yaml`
* `assets/index.yaml` → `<target>/index.yaml`
* `assets/entries/ENTRY_TEMPLATE.yaml` → `<target>/entries/ENTRY_TEMPLATE.yaml`
* `assets/profiles/general.yaml` → `<target>/profiles/general.yaml`
* `assets/schemas/profile.schema.yaml` → `<target>/schemas/profile.schema.yaml`
* `assets/schemas/entry.schema.yaml` → `<target>/schemas/entry.schema.yaml`
* `assets/repo-changelog-template.md` → `<target>/CHANGELOG.md`

Copy these scripts:

* `scripts/bootstrap.py` → `<target>/bootstrap.py`
* `scripts/verify_profile_contract.py` → `<target>/tools/verify_profile_contract.py`

## Bootstrap verification

After initialization, verify the repo from its root:

```bash
python bootstrap.py
python tools/verify_profile_contract.py
```

Expected outputs:

```json
{"message": "bootstrap complete", "stage": "bootstrap", "status": "ok"}
{"message": "profile verification passed", "stage": "verify_profile", "status": "ok"}
```

If bootstrap or profile verification fails:

* stop immediately
* do not silently repair
* inspect the error
* follow `references/RECOVERY.md`

## Adding a ledger entry

When the user completes governed work:

1. Create a new entry file under `entries/` using the template.
2. Use an ID of the form `ENTRY-YYYY-MM-DD-NNN`.
3. Append the new entry ID to `index.yaml` under `entries:`.
4. Update `execution_memory.yaml` field `last_verified_entry`.
5. Re-run verification:

```bash
python bootstrap.py
python tools/verify_profile_contract.py
```

## Entry rules

Each entry must:

* be append-only
* use a unique ID
* describe the state transition
* record verification status
* never mutate an earlier entry

## Recovery

Recovery is governed, not informal.

When verification fails, follow `references/RECOVERY.md` exactly.

Recovery must never:

* bypass verification
* modify prior ledger entries
* invent missing state
* proceed without a recovery entry

## Communication style

When using this skill:

* be explicit
* be deterministic
* name failure states clearly
* avoid fuzzy language about repository state
* treat verification failure as terminal until resolved
* prefer structural certainty over convenience
