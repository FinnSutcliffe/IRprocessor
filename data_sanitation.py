# Functions for cleaning and organising data into a analysable state




def identify_features(unclean_wave, median_multiplier):
    ##########################
    #
    # Identifies discreet feature durations from unclean wave
    #
    # unclean wave      :      list of continuous feature durations as appearing in wave
    # median_multiplier :      multiplied by median to calculate diff-peak threshold
    #
    ##########################

    features = []                                       # Ultimate list of discreet durations
    sorted_durations = sorted(unclean_wave)             # Pauses first and in descending order as -ve
    differences = [abs(sorted_durations[i+1]-sorted_durations[i])  # Feature change will spike difference
                   for i in range(len(sorted_durations)-1)]
    med_diff = sorted(differences)[int(len(differences)/2)]  # Median value of differences

    last_spike = 0
    for i in range(len(differences)):
        if differences[i] > med_diff * median_multiplier:  # Searching for spikes in difference
            section = sorted_durations[last_spike:i+1]  # Separate all those before spike (including ith)
            mean = int(sum(section)/len(section))       # Take average of separated
            features.append(mean)                       # Append average to features list
            last_spike = i+1                            # record start of next section

    section = sorted_durations[last_spike:]             # Capture section after last spike
    mean = int(sum(section)/len(section))               # Take average of last section
    features.append(mean)                               # Append average

    return features


def generate_clean_wave(unclean_wave, features):
    ##########################
    #
    # Transposes features onto unclean wave
    #
    # unclean wave      :      list of continuous feature durations as appearing in wave
    # features          :      list of discreet features
    #
    ##########################

    clean_wave = []

    for noisy_duration in unclean_wave:
        differences = [abs(noisy_duration - feature) for feature in features]  # Create list of differences
        pos = differences.index(min(differences))       # Position of smallest difference
        clean_wave.append(features[pos])                # Appends feature at pos (smallest difference => closest value)

    return clean_wave


def handle_wave_edges():                                # Trailing zeros after recording (deliberate trailing edge?...)
    pass


def identify_anomalies():                               # Identifies header, footer, midpoints etc and erroneous
    pass                                                # freq = 1,similar adjacent features?, regular position?
