import os
from src.audio_preprocessing import getMFCCBands2DMadmom
from src.textgrid_preprocessing import parse_syllable_line_list
from general.plot_two_spectrograms import plot_two_spectro_onsets
from parameters import *
from file_path import *

wav_path = os.path.join(primary_school_data_path, "wav_left")
textgrid_path = os.path.join(primary_school_data_path, "textgrid")

artist_name = "20171211SongRuoXuan"
aria_anme = "daxp-Meng_ting_de-Mu_gui_ying_gua_shuai-dxjky"

log_mel_teacher = getMFCCBands2DMadmom(os.path.join(wav_path, artist_name, aria_anme, "teacher.wav"),
                                       fs=fs,
                                       hopsize_t=hopsize_t,
                                       channel=1)

log_mel_student = getMFCCBands2DMadmom(os.path.join(wav_path, artist_name, aria_anme, "student01.wav"),
                                       fs=fs,
                                       hopsize_t=hopsize_t,
                                       channel=1)

nested_syllable_lists_teacher = \
    parse_syllable_line_list(ground_truth_text_grid_file=
                             os.path.join(textgrid_path, artist_name, aria_anme, "teacher.textgrid"),
                             parent_tier="line",
                             child_tier="dianSilence")

nested_syllable_lists_student = \
    parse_syllable_line_list(ground_truth_text_grid_file=
                             os.path.join(textgrid_path, artist_name, aria_anme, "student01.textgrid"),
                             parent_tier="line",
                             child_tier="dianSilence")

print(nested_syllable_lists_teacher)
print(nested_syllable_lists_student)

line_teacher = nested_syllable_lists_teacher[0]
line_student = nested_syllable_lists_student[0]

frame_start_teacher = int(round(line_teacher[0][0] / hopsize_t))
frame_end_teacher = int(round(line_teacher[0][1] / hopsize_t))

frame_start_student = int(round(line_student[0][0] / hopsize_t))
frame_end_student = int(round(line_student[0][1] / hopsize_t))

onsets_teacher = [[syl[0]-line_teacher[0][0], syl[2]] for syl in line_teacher[1]]
onsets_student = [[syl[0]-line_student[0][0], syl[2]] for syl in line_student[1]]

plot_two_spectro_onsets(mfcc0=log_mel_teacher[frame_start_teacher: frame_end_teacher],
                        mfcc1=log_mel_student[frame_start_student: frame_end_student],
                        hopsize_t=hopsize_t,
                        groundtruth_onset0=onsets_teacher,
                        groundtruth_onset1=onsets_student)