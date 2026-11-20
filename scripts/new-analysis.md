# Creating an Analysis Script

Analysis scripts live under `examples/<modality>_<paradigm>/` and follow a consistent pipeline. Use an existing script as a starting point (e.g. `examples/visual_p300/01r__p300_viz.py`).

## Naming convention

```
examples/<modality>_<paradigm>/
    01r__<paradigm>_viz.py        # ERP visualization
    02r__<paradigm>_decoding.py   # classification (optional)
```

## Standard pipeline

```python
import os
from collections import OrderedDict
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from mne import Epochs, find_events
from eegnb.analysis.utils import load_data, plot_conditions
from eegnb.datasets import fetch_dataset

# --- 1. Load data ---
data_dir = os.path.join(os.path.expanduser('~/'), '.eegnb', 'data')
experiment_dir = os.path.join(data_dir, '<ExperimentName>', 'eegnb_examples')

if not os.path.isdir(experiment_dir):
    fetch_dataset(data_dir=data_dir, experiment='<experiment-slug>', site='eegnb_examples')

subject = 1
session = 1
raw = load_data(subject, session,
                experiment='<experiment-slug>',
                site='eegnb_examples',
                device_name='muse2016',
                data_dir=data_dir)

# --- 2. Inspect power spectrum ---
raw.plot_psd()

# --- 3. Filter ---
raw.filter(1, 30, method='iir')

# --- 4. Epoch ---
events = find_events(raw)
event_id = {'condition_a': 1, 'condition_b': 2}
epochs = Epochs(raw, events=events, event_id=event_id,
                tmin=-0.1, tmax=0.8, baseline=None,
                reject={'eeg': 100e-6}, preload=True,
                verbose=False, picks=[0, 1, 2, 3])

print('sample drop %:', (1 - len(epochs.events) / len(events)) * 100)

# --- 5. Plot condition averages ---
conditions = OrderedDict()
conditions['condition_a'] = ['condition_a']
conditions['condition_b'] = ['condition_b']
diff_waveform = ('condition_a', 'condition_b')   # or None

fig, ax = plot_conditions(epochs, conditions=conditions,
                          ci=97.5, n_boot=1000, title='',
                          diff_waveform=diff_waveform)
plt.tight_layout()
plt.show()
```

## Key parameters to adjust per experiment

| Parameter | Description |
|---|---|
| `experiment` | Slug matching `fetch_dataset` experiment list (see `eegnb/datasets/datasets.py`) |
| `tmin` / `tmax` | Epoch window in seconds relative to stimulus onset |
| `event_id` | Maps condition name → marker integer (1 and 2 by default) |
| `picks` | Channel indices to include. Muse has 4 EEG channels (0–3). |
| `reject` | Amplitude threshold for artifact rejection in Volts |
| `diff_waveform` | Tuple `(cond_a, cond_b)` to plot the difference wave, or `None` |

## Running the script

```bash
conda activate eeg-expy-streaming
python examples/<modality>_<paradigm>/01r__<paradigm>_viz.py
```
