from src.audio_preprocessing import getMFCCBands2DMadmom
from general.plot_spectrograms import plot_one_spectro_syllable_phoneme
from parameters import *
from file_path import *
from src.csv_prepossessing import open_csv_recordings
from search_syllable import search_syllable


recordings_laosheng = open_csv_recordings("dataset - laosheng.csv")
recordings_dan = open_csv_recordings("dataset - dan.csv")

syl_pinyin = "dan"
role_type = "danAll"
if role_type == "danAll":
    recordings = recordings_dan
else:
    recordings = recordings_laosheng

wav_filename, textgrid_filename, list_phoneme_time_stamps = \
    search_syllable(recordings=recordings[150:],
                    role_type=role_type,
                    syl_pinyin=syl_pinyin)

log_mel = getMFCCBands2DMadmom(wav_filename,
                               fs=fs,
                               hopsize_t=hopsize_t,
                               channel=1)

frame_start = int(round(list_phoneme_time_stamps[0][0][0] / hopsize_t))
frame_end = int(round(list_phoneme_time_stamps[-1][0][1] / hopsize_t))

print(wav_filename)
print(textgrid_filename)
print(list_phoneme_time_stamps)

groundtruth_syllable_onset = \
    [[list_syl[0][0] - list_phoneme_time_stamps[0][0][0], list_syl[0][2]] for list_syl in list_phoneme_time_stamps]

groundtruth_phoneme_onset = \
    [[list_phn[0] - list_phoneme_time_stamps[0][0][0], list_phn[2]]
     for list_syl in list_phoneme_time_stamps
     for list_phn in list_syl[1]]

print(groundtruth_phoneme_onset)

plot_one_spectro_syllable_phoneme(mfcc=log_mel[frame_start:frame_end],
                                  hopsize_t=hopsize_t,
                                  groundtruth_syllable_onset=groundtruth_syllable_onset,
                                  groundtruth_phoneme_onset=groundtruth_phoneme_onset,
                                  figname=role_type + "_" + syl_pinyin + "_phoneme.png")