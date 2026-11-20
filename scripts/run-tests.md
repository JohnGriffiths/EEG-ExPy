# Running the Test Suite

## Choose the right environment

| Environment | When to use |
|---|---|
| `eeg-expy-streaming` | No PsychoPy required. Covers acquisition and analysis tests. Use for most development. |
| `eeg-expy-full` | Full environment including PsychoPy. Required to test experiment classes. |

Create the environment if you haven't already:

```bash
conda env create -f environments/eeg-expy-streaming.yml   # lightweight
conda env create -f environments/eeg-expy-full.yml        # full
```

## Run the tests

```bash
conda activate eeg-expy-streaming   # or eeg-expy-full
make test
```

Which runs:

```bash
pytest
```

Options are configured in `pyproject.toml`. Coverage reports are written to `htmlcov/`.

## Linux only — virtual display

PsychoPy requires a display. On headless Linux (CI or server), prefix with Xvfb:

```bash
Xvfb :0 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &
export DISPLAY=:0
make test
```

## What is and isn't run by default

`pyproject.toml` excludes by default:
- `tests/test_run_experiments.py` — requires a physical display and hardware
- `examples/` — not collected as tests

To run a specific test file:

```bash
pytest tests/test_analysis_utils_plots.py -v
```

To include coverage for a specific module:

```bash
pytest --cov=eegnb.analysis tests/
```

## Pass extra pytest flags

```bash
make test PYTEST_ARGS="-x -v"   # stop on first failure, verbose
```
