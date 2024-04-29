import os
import time
import logging

class DevtestHelper():
    '''
    WARNING: The functions here should only be called in development environments,
    and therefore should have configurable flags that "turn off" the feature(s) in Production.

    Functions that help simulate scenarios, etc. during development testing.
    '''

    mock_delay_times = {
        'HONBASHO_SCHEDULE':  int(os.environ.get('SIM_DELAY_HONBASHO_SCHEDULE', 0))
    }

    def simulate_delay(key: str):
        '''
        Simulates a delayed webservice response for the time (in seconds) configured by
        environment variable `SIM_DELAY_<key>`.

        Simulation is performed only if the delay time is configured.
        '''
        mock_delay_time = DevtestHelper.mock_delay_times[key]
        if mock_delay_time > 0:
            logging.info(f'[simulate_delay] Simulating delay: {mock_delay_time} second(s) [{key}]')
            time.sleep(mock_delay_time)
            logging.info(f'[simulate_delay] Delay simulation end [{key}]')