Visual Eye Closure Baseline
===========================

This experiment alternates between eyes-open and eyes-closed rest blocks.
During eyes-open blocks a fixation cross is displayed; during eyes-closed
blocks the text ``Close your eyes`` is shown. At each block transition a
short tone is played and event markers are sent over LSL and an optional
serial port.

Run from the command line with, for example:

.. code-block:: bash

    eegnb runexp --experiment visual-eyeclosure-baseline --recdur 600

The ``--recdur`` flag sets the total duration in seconds. With the default
60 s block length the above command runs five open/closed cycles.
