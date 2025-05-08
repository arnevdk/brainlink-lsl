# brainlink-lsl


A python script to connect the Macrotelect
[Brainlink Pro](https://o.macrotellect.com/BrainLinkPro.html) EEG headband to
[LabStreamingLayer](https://labstreaminglayer.readthedocs.io/)
for real-time brain-computer interfacing.

## Installation and dependencies


For installation with `conda`, use
```sh
conda env create --file environment.yml
conda activate brainlink-lsl
```
This will automatically install the necessary python dependencies and `liblsl`.

The `lib` directory contains the necessary compiled libraries obtained from
https://github.com/Macrotellect/BrainLinkParser-Python to parse the data read
out from the BrainLink Pro, but Macrotelect only makes these available for
Windows and MacOS, Linux is not supported.

## Usage

Connect to the Brainlink Pro as a Bluetooth audio device. A serial port should then
come available on your device through which the script can read the data.

Next, use the command `python brainlink_lsl.py` with the following options depending
on your setup:
```
Usage: brainlink_lsl.py [OPTIONS]

Options:
  -d, --device TEXT  The serial port device to use. Defaults to 'COM3'
  -b, --headband     Pass this option to indicate that the flexible headband
                     with extra heart rate and temperature sensor is used,
                     which decreases the effective EEG sampling rate from 512
                     to 484 Hz if sensors make contact.
  --help             Show this message and exit.
```

Some downstream applications, like time-locked BCI paradigms implemented in the
OpenVibe software, need the nominal sampling rate advertised by
the LSL stream to closely match the effective sampling rate of the stream.
While Macrotelect advertises a 512 Hz sampling rate for the BrainLink Pro,
closer inspection reveals that the average effective sampling rate for our device was closer to 513.78 Hz
when using the rigid head brace. When using the flexible headband hardware, the
mismatch is even larger and the average effective sampling rate for our device
was 484.30 Hz.

Using the script `determine_srate.py`, you can examine the average
effective sampling rate for your device and adjust the values in the `brainlink_lsl.py` script if necessary.
First, run `python brainlink_lsl.py`. In another terminal, run `python determine_srate.py`
and select the stream for which you want to determine the sampling rate.

## Output streams

Upon running `python brainlink_lsl`, the following streams are made available through LSL:
* `BrainLink-<COM port>-eeg`: the raw EEG data at 484.30 Hz for the headband setup, or 513.78 Hz for the head brace setup.
* `BrainLink-<COM port>-gyro`: the gyroscope's x, y, and z axis output at 2.8 Hz.
* `BrainLink-<COM port>-physio`: physiological data like heart rate and
   temperature at 1 Hz.
