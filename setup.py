#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()


def read_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    reqs = []
    for req in lines:
        req = req.strip()
        if req and not req.startswith('#') and not req.startswith('-e'):
            if '#' in req:
                req = req.split('#')[0].strip()
            if req:
                reqs.append(req)
    return reqs

install_requires_analysis = read_requirements('requirements-analysis.txt')
install_requires_streaming = read_requirements('requirements-streaming.txt')
install_requires_stimpres = read_requirements('requirements-stimpres.txt')
install_requires_docsbuild = read_requirements('requirements-docsbuild.txt')

setup(
    name="eeg-expy", 
    version="0.2",
    author="John David Griffiths",
    author_email="j.davidgriffiths@gmail.com",
    description='python library for eeg cognitive neuroscience experiments',
    keywords='eeg, cognitive neuroscience, experiments, evoked response, auditory, visual',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires_analysis,   # base dependencies
    extras_require={
        'docsbuild':  install_requires_docsbuild,
        'streaming':  install_requires_streaming,
        'stimpres':   install_requires_stimpres,
        'streamstim': install_requires_streaming + install_requires_stimpres,
        'full':       install_requires_docsbuild + install_requires_streaming + install_requires_stimpres 
                   },
    url='https://github.com/NeuroTechX/eeg-expy',
    license="BSD (3-clause)",
    entry_points={"console_scripts": ["eegnb=eegnb.cli.__main__:main",
                                      "eegexpy=eegnb.cli.__main__:main"]},
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
