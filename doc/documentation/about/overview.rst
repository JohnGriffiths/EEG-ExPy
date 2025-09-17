Overview
================

WHOBPYT (Whole-Brain Optimization for Biophysical PYThon models) is a flexible, PyTorch-compatible simulation and inversion toolkit for large-scale brain models. It supports neural mass models, neural field models, and conductance-based models, enabling biophysically informed inference from EEG and power spectral density (PSD) data.

This package is designed for researchers in computational neuroscience, brain modeling, and mental health, offering tools to fit EEG/PSD data to biologically interpretable models with variational inference and gradient-based optimization.

🔁 Supported Models

🧠 1. Jansen-Rit Neural Mass Model

Cortical column dynamics (pyramidal, excitatory, inhibitory populations)

EEG simulation and inversion

Time-domain fitting via variational free energy or gradient descent

🌐 2. Robinson Neural Field Model 

Spatially extended cortical field equations

Frequency-domain fitting (PSD inversion)

Saturation dynamics for realistic response to external input

Fast convolution and efficient frequency-domain inversion

⚡ 3. Conductance-Based Neural Mass Models

Biophysically realistic membrane dynamics

Voltage-dependent synapses (e.g., NMDA, GABA)

Inversion from EEG using  free energy gradients

🎯 Key Features

🔍 EEG and PSD Inversion: Time and frequency domain fitting

🧠 Biomarker Extraction: E/I balance, alpha peak, Lyapunov exponents

🧪 Model Comparison: Fit and compare multiple neural models to EEG

🧬 Connectome Integration: Multi-node networks and distance-based delays

⚡ GPU Acceleration: PyTorch backends for fast training and simulation

🧰 Modular Design: Swap models, priors, and solvers with minimal code changes

🧠 Applications

Mental health modeling (depression, ADHD, schizophrenia, Alzheimer’s)

Real-time or offline EEG inversion

Biomarker discovery for neuromodulation (TMS, tACS)

Dynamic circuit modeling under pharmacological modulation

Seizure modeling and prediction
