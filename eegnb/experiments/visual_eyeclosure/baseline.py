"""Eyes-open/eyes-closed baseline task.

Alternates blocks of eyes-open and eyes-closed rest. A fixation cross is
presented during eyes-open blocks and a "close your eyes" message is
shown during eyes-closed blocks. At each transition a short tone (or an
optional audio file) is played, and LSL/serial markers are sent so EEG
and fNIRS systems receive synchronized events.
"""

from typing import Optional
from time import time

from psychopy import prefs
prefs.hardware["audioLib"] = "PTB"
prefs.hardware["audioLatencyMode"] = 3

from psychopy import core, visual, sound
from pylsl import StreamInfo, StreamOutlet, local_clock

try:  # pyserial is optional
    import serial
except Exception:  # pragma: no cover - handled gracefully
    serial = None

from eegnb.devices.eeg import EEG

__title__ = "Visual Eye Closure Baseline"


def present(
    duration: Optional[float] = None,
    eeg: Optional[EEG] = None,
    save_fn: Optional[str] = None,
    block_duration: float = 60.0,
    n_cycles: int = 5,
    serial_port: Optional[str] = None,
    use_verbal_cues: bool = False,
    open_audio: Optional[str] = None,
    close_audio: Optional[str] = None,
    **kwargs,
) -> None:
    """Run the eye-closure baseline experiment.

    Parameters
    ----------
    duration : float, optional
        Total duration of the recording in seconds. If provided, overrides
        ``n_cycles`` by computing the number of block cycles that fit in the
        requested duration.
    eeg : EEG, optional
        EEG device instance. If provided, markers are sent via ``eeg.push_sample``
        in addition to LSL and the recording is started/stopped automatically.
    save_fn : str, optional
        Path for saving recorded EEG data.
    block_duration : float
        Duration of each eyes-open or eyes-closed block in seconds.
    n_cycles : int
        Number of open/closed cycles. Each cycle consists of one open and one
        closed block. Ignored if ``duration`` is provided.
    serial_port : str, optional
        Serial port to which trigger bytes should be sent. If ``None`` no serial
        triggers are emitted.
    use_verbal_cues : bool
        If ``True`` and ``open_audio``/``close_audio`` are supplied, verbal cues
        are played instead of tones.
    open_audio, close_audio : str, optional
        Paths to audio files for the "open your eyes" and "close your eyes"
        instructions. Used only when ``use_verbal_cues`` is ``True``.
    """

    if duration is not None:
        # Each cycle has two blocks
        n_cycles = max(1, int(duration // (2 * block_duration)))

    # Setup LSL outlet
    info = StreamInfo("Markers", "Markers", 1, 0, "int32", "eyeclosure-baseline")
    outlet = StreamOutlet(info)

    # Setup serial connection if requested
    ser = None
    if serial_port and serial is not None:
        try:
            ser = serial.Serial(serial_port, 115200, timeout=1)
        except Exception as exc:  # pragma: no cover
            print(f"Could not open serial port {serial_port}: {exc}")
            ser = None

    # Prepare window and stimuli
    win = visual.Window([800, 600], monitor="testMonitor", units="deg", fullscr=True)
    win.mouseVisible = False
    fixation = visual.TextStim(win, text="+", height=1.0)
    close_text = visual.TextStim(win, text="Close your eyes", height=1.0)

    # Load sounds
    if use_verbal_cues and open_audio and close_audio:
        open_sound = sound.Sound(open_audio)
        close_sound = sound.Sound(close_audio)
    else:
        open_sound = sound.Sound(440, secs=0.2)
        close_sound = sound.Sound(330, secs=0.2)

    # Start EEG recording if available
    if eeg:
        eeg.start_recording(save_fn=save_fn, duration=block_duration * 2 * n_cycles)

    try:
        for _ in range(n_cycles):
            # Eyes-open block
            ts = local_clock()
            outlet.push_sample([1], ts)
            if eeg:
                eeg.push_sample(marker=[1], timestamp=time())
            if ser:
                ser.write(b"\x01")
            open_sound.play()
            fixation.draw()
            win.flip()
            core.wait(block_duration)

            # Eyes-closed block
            ts = local_clock()
            outlet.push_sample([2], ts)
            if eeg:
                eeg.push_sample(marker=[2], timestamp=time())
            if ser:
                ser.write(b"\x02")
            close_sound.play()
            close_text.draw()
            win.flip()
            core.wait(block_duration)
    finally:
        win.close()
        if eeg:
            eeg.stop_recording()
        if ser:
            ser.close()
