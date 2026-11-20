# Validating Your Conda Environment

## Environment overview

| Environment file | Conda env name | Use for |
|---|---|---|
| `environments/eeg-expy-streaming.yml` | `eeg-expy-streaming` | Acquisition + analysis, no PsychoPy |
| `environments/eeg-expy-full.yml` | `eeg-expy-full` | Full stack including PsychoPy + experiments |
| `environments/eeg-expy-stimpres.yml` | — | Stimulus presentation only |
| `environments/eeg-expy-streamstim.yml` | — | Streaming + stimulus presentation |
| `environments/eeg-expy-docsbuild.yml` | — | Docs build only |

## Check which environment is active

```bash
conda info --envs          # list all envs, active one marked with *
conda list                 # packages in the current env
```

## Verify the package is installed in editable mode

```bash
pip show eegnb
```

The `Location` field should point inside this repo. If not, run:

```bash
pip install -e .[streaming]    # for streaming env
pip install -e .[full]         # for full env
```

## Check for common missing dependencies

```python
# Run in Python to check key imports
import mne
import muselsl
import psychopy        # only in full env
import pylsl
import brainflow
```

## Recreate an environment from scratch

```bash
conda deactivate
conda env remove -n eeg-expy-streaming
conda env create -f environments/eeg-expy-streaming.yml
conda activate eeg-expy-streaming
```

## Linux-specific dependencies

The full environment requires system packages that conda cannot install. If PsychoPy or wxPython fails to import on Linux:

```bash
make install-deps-apt           # installs xvfb, libgtk-3-dev, portaudio19-dev, etc.
make install-deps-wxpython      # installs wxPython wheels for ubuntu-22.04
```

## Python version constraints

- `eeg-expy-full`: Python `>=3.10,<3.12` (PsychoPy 2026.x requirement)
- `eeg-expy-streaming`: Python `>=3.10` (3.12 and 3.13 are experimental in CI)

If you see `python_requires` errors, check that your conda Python matches the constraint in the environment file.
