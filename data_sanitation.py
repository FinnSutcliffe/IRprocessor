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


def identify_anomalies(clean_wave, median_multiplier):
    ##########################
    #
    # Identifies header, footer, midpoints etc and erroneous (NOT TOGGLEBIT)
    #
    # clean_wave          :      list of discreet feature durations as appearing in wave
    # median_multiplier   :      multiplied by abs. median to calculate anom. duration threshold
    #
    ##########################

    # 0: data
    # 1: anomaly

    anomalies = [0]*len(clean_wave)                     # List to contain enumeration of status of features

    f_threshold = 1
    freqs = [clean_wave.count(i) for i in clean_wave]   # Each feature replaced with its own frequency in clean_wave
    for i in range(len(freqs)):                         # Look through frequencies
        if freqs[i] <= f_threshold:                     # f_threshold and below indicates anomaly
            anomalies[i] = 1                            # mark that index as anomalous


#################################################################################
#    median = sorted([abs(i) for i in clean_wave])[int(len(clean_wave)/2)]      #
 #   for i in range(len(clean_wave)): # NEEDS REWORKING                         #
  #      if abs(clean_wave[i]) > median*median_multiplier: # NEEDS REWORKING    #
   #         anomalies[i] = 1 # NEEDS REWORKING                                 #
#################################################################################

    return anomalies


def identify_border_features(clean_wave, anomalies):
    ##########################
    #
    # Isolate headers and footers based on the position of anomalies in a clean wave, and from that extract data_wave
    #
    # clean_wave          :      list of discreet feature durations as appearing in wave
    # anomalies           :      list of enumerations marking features as anomalous or not
    #
    ##########################

    data_wave = []
    header = []
    footer = []
    for i, a in enumerate(anomalies):
        if a == 1:                                      # If feature identified as anomaly
            if i == 0:                                  # If adjacent to leading edge of wave
                anomalies[i] = 2                        # Set as header
            elif anomalies[i-1] == 2:                   # if adjacent to identified header
                anomalies[i] = 2                        # Separated into separate elif to stop index error with i-1
            else:
                break                                   # Reached the edge of the header

    for i, a in enumerate(reversed(anomalies)):
        if a == 1:                                      # If feature identified as anomaly
            if i == 0:                                  # If adjacent to leading edge of wave
                anomalies[-i-1] = 3                     # Set as header, index needs to be reversed
            elif anomalies[-i] == 3:                    # if adjacent to identified footer
                anomalies[-i-1] = 3                     # Index reversed to select correct part of non-reversed anoms
            else:
                break                                   # Reached the end of the footer

    for i,a in enumerate(anomalies):
        if a == 0:                                      # Normal data feature
            data_wave.append(clean_wave[i])             # Add to data_wave
        elif a == 1:                                    # Non-header/footer anomaly
            data_wave.append(clean_wave[i])             # FOR NOW JUST IGNORE OK HOW OFTEN WILL THIS HAPPEN ANYWAYS...
        elif a == 2:                                    # Part of the header
            header.append(clean_wave[i])
        elif a == 3:                                    # Part of the footer
            footer.append(clean_wave[i])

    return data_wave, header, footer


def handle_wave_edges():                                # Trailing zeros after recording (deliberate trailing edge?...)
    # If first duration of footer != +ve, add a pause on the end of datawave?
    pass
