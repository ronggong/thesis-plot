from src.csv_prepossessing import open_csv_recordings
import soundfile as sf
import numpy as np
from dur_stats import dur_stats


recordings_laosheng = open_csv_recordings("dataset - laosheng.csv")
recordings_dan = open_csv_recordings("dataset - dan.csv")

song_dur, melodic_line_dur_list, syllable_dur_list, phoneme_dur_list, dict_phoneme_dur = \
    dur_stats(recordings=recordings_dan,
              role_type="danAll")

melodic_line_dur_min, melodic_line_dur_max, melodic_line_dur_mean, melodic_line_dur_std = \
        min(melodic_line_dur_list), max(melodic_line_dur_list), \
        np.mean(melodic_line_dur_list), np.std(melodic_line_dur_list)

syllable_dur_min, syllable_dur_max, syllable_dur_mean, syllable_dur_std = \
    min(syllable_dur_list), max(syllable_dur_list), \
    np.mean(syllable_dur_list), np.std(syllable_dur_list)

phoneme_dur_min, phoneme_dur_max, phoneme_dur_mean, phoneme_dur_std = \
    min(phoneme_dur_list), max(phoneme_dur_list), \
    np.mean(phoneme_dur_list), np.std(phoneme_dur_list)

print("melodic line number", len(melodic_line_dur_list))
print("syllable number", len(syllable_dur_list))
print("phoneme number", len(phoneme_dur_list))

print("melodic line duration, min, max, mean, std", melodic_line_dur_min, melodic_line_dur_max, melodic_line_dur_mean, melodic_line_dur_std)
print("syllable duration, min, max, mean, std", syllable_dur_min, syllable_dur_max, syllable_dur_mean, syllable_dur_std)
print("phoneme duration, min, max, mean, std", phoneme_dur_min, phoneme_dur_max, phoneme_dur_mean, phoneme_dur_std)


# print(np.sum(song_dur))
# print(np.median(song_dur))
