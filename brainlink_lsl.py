from lib.BrainLinkParser import BrainLinkParser
from serial import Serial
from pylsl import StreamInfo, StreamOutlet
import time
import logging
import sys
import click

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class EEGHandler:
    
    def __init__(self, dev, headband):
        srate = 484.3 if headband else 513.78
        info = StreamInfo(
            name='BrainLink-eeg',
            type='EEG',
            channel_count=1,
            nominal_srate=srate,
            channel_format='float32',
            source_id=f'BrainLink-{dev}-eeg'
        )
        self._outlet = StreamOutlet(info)
    
    def __call__(self, eeg):
        self._outlet.push_sample([float(eeg)])

class GyroHandler:
        
    def __init__(self, dev):
        info = StreamInfo(
            name='BrainLink-gyro',
            type='Gyro',
            channel_count=3,
            nominal_srate=2.8,
            channel_format='float32',
            source_id=f'BrainLink-{dev}-gyro'
        )    
        self._outlet = StreamOutlet(info)
     
    def __call__(self, x, y, z):
        self._outlet.push_sample([x,y,z])

class ExtraInfoHandler:
    
    def __init__(self, dev):
        info = StreamInfo(
            name='BrainLink-physio',
            type='Physio',
            channel_count=2,
            nominal_srate=1,
            channel_format='float32',
            source_id=f'BrainLink-{dev}-physio'
        )
        self._outlet = StreamOutlet(info)
        self._logger = logging.getLogger()
    
    def __call__(self, data):
        self._logger.log(logging.INFO, f'version: {data.version}, battery: {data.battery}, ap: {data.ap}')
        self._outlet.push_sample([float(data.heart), float(data.temperature)])

@click.command()
@click.option(
    '-d', '--device',
    default='COM3',
    help="""The serial port device to use. Defaults to 'COM3'"""
)
@click.option(
    '--headband', '-b',
    is_flag=True,
    help="""
        Pass this option to indicate that the flexible headband with extra heart rate
        and temperature sensor is used, which decreases the effective EEG sampling
        rate from 512 to 484 Hz if sensors make contact.
    """
)
def brainlink_lsl(device, headband):
    ser = Serial(device, baudrate=115200, timeout=0)
    parser = BrainLinkParser(None, ExtraInfoHandler(device), GyroHandler(device), None, EEGHandler(device, headband))

    while True:
        while ser.in_waiting:
            line = ser.readline()
            parser.parse(line)
        time.sleep((1/512)/3)
        
            

if __name__ == '__main__':
    brainlink_lsl()