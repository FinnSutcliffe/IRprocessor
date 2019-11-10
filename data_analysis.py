# Functions for decoding protocol and wave

from data_sanitation import identify_features


def search_protocols():                             # Search existing protocols for a match
    pass


def test_patterns(data_wave, zero, one, edges):
    ##########################
    #
    # test a proposed 'one' and 'zero' and determine a best-case deviance level, as well as datastream for it
    #
    # data_wave    :    list of discreet feature durations - assumed to be all binary data
    # zero         :    list of discreet feature durations corresponding to '0'
    # one          :    list of discreet feature durations corresponding to '1'
    # edges        :    Indicates whether data ends cleanly or there is possibility of lost pause
    #
    ##########################

    wave_blank = data_wave[:]                       # Copy of data_wave to be cut up and played with
    datastream = ""
    deviance = 0
    i = 0                                           # while loop used as wave_blank may extend during iteration
    while i < len(wave_blank)-1:                    # at least 2 features left
        f = wave_blank[i]
        diffs = [abs(zero[0]-f), abs(one[0]-f)]     # Comparison of which is closer to the focus
        if diffs[0] == diffs[1]:                    # Equally far from focus, e.g. the same
            old_diffs = diffs
            i += 1
            f = wave_blank[i]                       # examine next feature instead
            diffs = [abs(zero[1]-f), abs(one[1]-f)]  # second halves of both patterns compared rather than just 1
            if diffs[0] <= diffs[1]:                # If equal just default to 0 it wouldn't matter
                datastream += "0"
                deviance += diffs[0] + old_diffs[0]
            else:
                datastream += "1"
                deviance += diffs[1] + old_diffs[1]
            i += 1                                  # move counter to next feature
            continue                                # Second half already compared, so can skip later analysis
        elif diffs[0] < diffs[1]:                   # more likely to be a zero pattern
            leader = zero                           # leader is compared to second half later on
            feature_sum = zero[1] + one[0]          # Next feature, if a sum, will be this
            datastream += "0"
            deviance += diffs[0]
        else:
            leader = one
            feature_sum = one[1] + zero[0]
            datastream += "1"
            deviance += diffs[1]

        i += 1                                      # Move on to the second half of the pattern
        f = wave_blank[i]
        diffs = [abs(leader[1]-f), abs(feature_sum-f)]   # Decide if second part needs to be split
        if diffs[0] <= diffs[1]:                    # Closer to being just a singular features
            deviance += diffs[0]
        else:                                       # Closer to being 2 combined features
            wave_blank.insert(i+1, f-leader[1])  # Insert cut section AFTER current feature
            wave_blank[i] = leader[1]               # Cut current feature shorter

        i += 1                                      # Move on to first half of next pattern

    return datastream, deviance


def identify_bits(data_wave, footer):
    ##########################
    #
    # In absence of existing protocol, identify the patterns for 1 and 0 in the new data_wave
    #
    # data_wave    :    list of discreet feature durations - assumed to be all binary data
    # footer       :    feature durations at the end of a wave as set for a given protocol
    #
    ##########################

    median_multiplier = 0.8
    features = identify_features(data_wave, median_multiplier)  # List of all features in data_wave
    pulses = [x for x in features if x > 0]                     # List of pulses in ascending order
    pauses = [x for x in reversed(features) if x < 0]           # List of pauses in abs. ascending order
    f0 = data_wave[0]
    if f0 > 0:                                                  # If f0 is a pulse
        f1_perms = pauses                                       # f1 must be a pause
    else:
        f1_perms = pulses                                       # else f1 is a pulse

    permutations = []
    for f1 in f1_perms:                                         # Test each possible feature
        zero = [f0, f1]                                         # Generate possible zero
        for f2 in pulses:                                       # Pulses chosen arbitrarily, swapped later on
            for f3 in pauses:
                one = [f2, f3]                                  # Generate possible one
                datastream, deviance = test_patterns(data_wave, zero, one, bool(footer))
                permutations.append([zero, one, datastream, deviance])
                one = [f3, f2]                                  # Also test all permutations where one starts with pause
                datastream, deviance = test_patterns(data_wave, zero, one, bool(footer))
                permutations.append([zero, one, datastream, deviance])

    closest = sorted(permutations, key=lambda x: x[3])[0]       # Sorts permutations by deviance, and returns lowest
    print(sorted(permutations, key=lambda x: x[3])[0])
    return closest


def locate_togglebit():
    pass


def locate_checksum():
    pass


def locate_repeat_bytes():
    pass
