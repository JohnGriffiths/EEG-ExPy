# Building the Documentation

## Setup

Docs use a separate conda environment with Sphinx and related dependencies.

```bash
conda env create -f environments/eeg-expy-docsbuild.yml
conda activate eeg-expy-docsbuild
make install-docs-build-dependencies
```

## Build

```bash
make docs
```

Which runs `cd doc && make html`. Output lands in `doc/_build/html/`. Open `doc/_build/html/index.html` in a browser to review.

## Clean and rebuild

```bash
make clean
make docs
```

## Structure

| Path | Contents |
|---|---|
| `doc/conf.py` | Sphinx configuration |
| `doc/getting_started/` | User-facing guides (Markdown) |
| `doc/misc/` | Device and hardware notes |
| `examples/` | Gallery examples (run by `sphinx-gallery` during the build) |

## Gallery examples

Sphinx-gallery executes `examples/**/*.py` files during the build and captures their output as documentation pages. If an example script fails (missing data, import error), the build will warn but continue. Run the failing script directly first to debug it:

```bash
python examples/visual_p300/01r__p300_viz.py
```

## CI

Docs are built automatically on push to `master` via `.github/workflows/docs.yml`.
