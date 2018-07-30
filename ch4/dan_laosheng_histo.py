from src.csv_prepossessing import open_csv_recordings
import soundfile as sf
import numpy as np
from dur_stats import dur_stats
import matplotlib.pyplot as plt


def histo_plot(duration_list, bins_number, median, range, xlabel, save_name):
    fontsize = 15
    n, bins, patches = plt.hist(duration_list, bins_number, range=range, density=True, facecolor='k')
    plt.axvline(x=median, linestyle="--", color="r")
    axes = plt.gca()
    plt.text(median, 1.01*axes.get_ylim()[1], str(round(median, 2)), fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.savefig(save_name)
    plt.close()


recordings_laosheng = open_csv_recordings("dataset - laosheng.csv")
recordings_dan = open_csv_recordings("dataset - dan.csv")

roletype = "danAll"
song_dur, melodic_line_dur_list, syllable_dur_list, phoneme_dur_list, dict_phoneme_dur = \
    dur_stats(recordings=recordings_dan,
              role_type=roletype)

median_melodic_line_dur = np.median(melodic_line_dur_list)
median_syllable_dur = np.median(syllable_dur_list)
median_phoneme_dur = np.median(phoneme_dur_list)

histo_plot(duration_list=melodic_line_dur_list,
           bins_number=100,
           median=median_melodic_line_dur,
           range=None,
           xlabel="Time (s)",
           save_name=roletype + "_melodic_line_dur.png")

histo_plot(duration_list=syllable_dur_list,
           bins_number=100,
           median=median_syllable_dur,
           range=(0, 20),
           xlabel="Time (s)",
           save_name=roletype + "_syllable_dur.png")

histo_plot(duration_list=phoneme_dur_list,
           bins_number=100,
           median=median_phoneme_dur,
           range=(0, 4),
           xlabel="Time (s)",
           save_name=roletype + "_phoneme_dur.png")

for phn_name in dict_phoneme_dur:
    phoneme_dur_list_individual = dict_phoneme_dur[phn_name]
    if len(phoneme_dur_list_individual):
        median_phoneme_dur_individual = np.median(phoneme_dur_list_individual)
        histo_plot(duration_list=phoneme_dur_list_individual,
                   bins_number=50,
                   median=median_phoneme_dur_individual,
                   range=(0, 4),
                   xlabel="Time (s)",
                   save_name=roletype + "_" + phn_name + "_phoneme_dur.png")