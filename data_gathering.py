# Functions for reading the GPIO pins and creating an unclean wave. <UPDATE AS NECESSARY>




def read_wave():                    # Interfaces with RPI pins to read demodulated IR signals
    # NEEDS TO BE OPTIMISED
    pass                            # Returns binary array, and corresponding array of times from t-0

def parse_wave():                   # Takes binary and time arrays, generates array of continuous features
    # pauses -ve, pulses +ve
    pass