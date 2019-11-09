from data_gathering import read_wave, parse_wave
from data_sanitation import identify_features, generate_clean_wave, handle_wave_edges, identify_anomalies


def main():

    # Data gathering

    read_wave()
    parse_wave()

    # Data sanitation

    identify_features()
    generate_clean_wave()
    handle_wave_edges()
    identify_anomalies()

    # Data analysis

    #encoding/identify bits
    #datastream
    #togglebit
    #checksum
    #{repeated bytes?}

    # Database interaction

    #create_database()
    #add_protocol()
    #add_wave()
    #delete_protocol()
    #delete_wave()
    #find_protocol()
    #find_wave()

    ## GUI

    #signal_diagnostics()?

    pass