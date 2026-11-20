# Adding a New Experiment

Experiments live under `eegnb/experiments/<modality>_<paradigm>/`. Follow the structure of an existing experiment (e.g. `visual_p300/p300.py`).

## 1. Create the experiment directory

```
eegnb/experiments/<modality>_<paradigm>/
    __init__.py
    <name>.py
```

The `__init__.py` can be empty.

## 2. Write the experiment class

Inherit from `BaseExperiment` (single continuous block) or `BlockExperiment` (multi-block with per-block instructions).

```python
from eegnb.experiments import Experiment
from eegnb.devices.eeg import EEG
from typing import Optional

class MyExperiment(Experiment.BaseExperiment):

    def __init__(self, duration=120, eeg: Optional[EEG] = None, save_fn=None,
                 n_trials=2010, iti=0.4, soa=0.3, jitter=0.2, use_vr=False):
        super().__init__("My Experiment", duration, eeg, save_fn,
                         n_trials, iti, soa, jitter, use_vr)

    def load_stimulus(self):
        # Load and return stimulus objects as a list of condition lists.
        # e.g. return [condition_a_stims, condition_b_stims]
        raise NotImplementedError

    def present_stimulus(self, idx: int):
        # Draw the stimulus for trial `idx` to self.window.
        # Push an EEG marker if self.eeg is set:
        #
        #   label = self.trials["parameter"].iloc[idx]
        #   if self.eeg:
        #       timestamp = time()
        #       marker = [self.markernames[label]] if self.eeg.backend == "muselsl" \
        #                else self.markernames[label]
        #       self.eeg.push_sample(marker=marker, timestamp=timestamp)
        #
        # End with self.window.flip().
        raise NotImplementedError
```

For `BlockExperiment`, additionally override `present_block_instructions(self, current_block)`.

## Key fields set by BaseExperiment

| Field | Description |
|---|---|
| `self.window` | PsychoPy `Window` (available after `setup()`) |
| `self.trials` | DataFrame with columns `parameter` (0/1) and `timestamp` |
| `self.markernames` | List `[1, 2]` — event codes sent to the EEG device |
| `self.eeg` | `EEG` device object, or `None` if running without hardware |

## 3. Register in `eegnb/experiments/__init__.py`

Check whether the experiment should appear in the CLI experiment list in `eegnb/cli/introprompt.py`.

## 4. Add an examples script

Create `examples/<modality>_<paradigm>/`:
- `00x__<name>_run_experiment.py` — runs the experiment
- `01r__<name>_viz.py` — loads data, epochs, and plots the ERP

Follow the pattern in `examples/visual_p300/` for the analysis script structure:
load → `raw.filter()` → `mne.find_events()` → `mne.Epochs()` → `plot_conditions()`.

## 5. Add stimulus assets if needed

Stimulus image folders go under `eegnb/stimuli/`. Add a path constant to `eegnb/stimuli/__init__.py` and import it in your experiment file.
