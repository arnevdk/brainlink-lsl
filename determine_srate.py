from pylsl import resolve_streams, resolve_byprop, StreamInlet, proc_ALL, local_clock
import click
from click_prompt import choice_option


@click.command()
@choice_option('--stream', prompt='LSL stream', type=click.Choice([s.source_id() for s in resolve_streams()]),
              help="Select an LSL stream to determine it's effective sampling rate.")
def determine_srate(stream):
    info = resolve_byprop('source_id', stream)[0]
    inlet = StreamInlet(info, processing_flags=proc_ALL)
    
    start_time = local_clock()
    n_samples = 0
    while True:        
        _ = inlet.pull_sample()
        n_samples +=1
        elapsed_time = local_clock()-start_time
        eff_srate = n_samples/elapsed_time
        if not n_samples %512:
            print(eff_srate)
        
if __name__ == '__main__':
    determine_srate()