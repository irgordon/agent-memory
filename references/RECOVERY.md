# Recovery Protocol

This procedure governs all recovery actions.

Recovery is a controlled state transition.
Recovery is never implicit.
Recovery must be recorded as a ledger entry.

## When recovery is allowed

Recovery may execute only when:

1. verification has failed
2. repository state is inconsistent
3. a recovery entry will be recorded

## Recovery procedure

### Step 1 — Stop execution

Do not continue.
Do not silently modify files.

### Step 2 — Identify failure

Read the verifier or bootstrap error output.

Examples:

- `missing_required_paths`
- `invalid_profile_count`
- `missing_required_field`
- `index_entry_missing_file`
- `execution_memory_inconsistent`

### Step 3 — Restore valid repository structure

Repair only the specific invalid state.

Do not:

- edit existing ledger entries
- reorder existing history
- invent profile fields
- bypass schema requirements

### Step 4 — Record recovery as a governed action

Create a new entry:

```text
entries/ENTRY-YYYY-MM-DD-NNN.yaml
````

Set:

* `action: recovery`
* `description:` concise description of the corrective action
* `state_transition:` explicit before/after state

### Step 5 — Re-run verification

From repository root:

```bash
python bootstrap.py
python tools/verify_profile_contract.py
```

Recovery is complete only when verification returns success.

## Prohibited actions

Recovery must never:

* edit existing entries
* remove entries from index history
* continue after failed verification
* silently repair state
* apply manual override
