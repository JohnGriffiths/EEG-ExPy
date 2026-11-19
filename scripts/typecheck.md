# Type Checking

## Setup

The `eeg-expy-full` environment includes mypy. Configuration is in `setup.cfg` under `[mypy]`.

```bash
conda activate eeg-expy-full
make typecheck
```

Which runs:

```bash
python -m mypy --exclude 'examples/visual_cueing'
```

`examples/visual_cueing` is excluded due to unresolved type errors there.

## Known suppressions

**PyQt6 stubs** — PyQt6 6.12.0 ships `QtGui.pyi` with invalid syntax. `setup.cfg` skips these stubs entirely:

```ini
[mypy-PyQt6.*]
follow_imports = skip
follow_imports_for_stubs = true
```

Do not remove this section until a fixed PyQt6 release is available.

**Untyped defs** — `check_untyped_defs = true` is currently commented out in `setup.cfg`. Re-enable it once type annotations across the codebase are complete.

## Adding type annotations

- `eegnb/devices/eeg.py` and `eegnb/experiments/Experiment.py` have partial annotations — follow their style.
- Use `Optional[X]` (not `X | None`) for compatibility with Python 3.10.
- `ignore_missing_imports = true` is set globally, so missing stubs for third-party packages do not need `# type: ignore` comments.

## Running against a single file

```bash
python -m mypy eegnb/analysis/utils.py
```
