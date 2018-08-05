from file_path import *
from src.textgrid_preprocessing import parse_syllable_line_list


def dur_stats(recordings, role_type):
    """
    Statistics of melodic line, syllable and phoneme durations
    :param recordings:
    :param role_type:
    :return:
    """
    song_dur = []
    syllable_number = 0
    phoneme_number = 0
    textgrid_file_number = 0

    melodic_line_dur_list = []
    syllable_dur_list = []
    phoneme_dur_list = []

    dict_phoneme_dur = {u'':[], u'U^':[], u'an':[],
                        u'in':[], u' ':[], u'aI^':[],
                        u'7N':[], u'yn':[], u'@n':[],
                        u'eI^':[], u'1':[], u'7':[],
                        u'iN':[], u'9':[], u"r\\'":[],
                        u'?':[], u'@':[], u'E':[],
                        u'H':[], u'M':[], u'O':[],
                        u'N':[], u'oU^':[], u'AN':[],
                        u'AU^':[], u'a':[], u'c':[],
                        u'En':[], u'f':[], u'i':[],
                        u'k':[], u'j':[], u'm':[],
                        u'l':[], u'o':[], u'n':[],
                        u'UN':[], u'u':[], u'w':[],
                        u'y':[], u'x':[]}
    for rec in recordings:
        if rec[0] == "part1":
            data_path = nacta_data_path
            sub_folder = role_type
            textgrid_folder = "textgrid"
            wav_folder = "wav_left"
            if rec[2][:2] == "ls" or rec[2][:2] == "da":
                syllable_tier = "dianSilence"
            else:
                syllable_tier = "pinyin"
            phoneme_tier = "details"
        elif rec[0] == "part2":
            data_path = nacta_2017_data_path
            sub_folder = rec[1]
            textgrid_folder = "textgridDetails"
            wav_folder = "wav"
            syllable_tier = "dianSilence"
            phoneme_tier = "details"
        else:
            data_path = primary_school_data_path
            sub_folder = rec[1]+"/"+rec[2]
            textgrid_folder = "textgrid"
            wav_folder = "wav_left"
            syllable_tier = "dianSilence"
            phoneme_tier = "details"

        filename = rec[3]
        if "." in filename:
            filename = os.path.splitext(filename)[0]

        textgrid_filename = os.path.join(data_path, textgrid_folder, sub_folder, filename + ".textgrid")
        wav_filename = os.path.join(data_path, wav_folder, sub_folder, filename + ".wav")

        nested_syllable_list, is_file_exist, is_syllable_found = \
            parse_syllable_line_list(ground_truth_text_grid_file=textgrid_filename,
                                     parent_tier="line",
                                     child_tier=syllable_tier)

        nested_phoneme_list, is_file_exist, is_phoneme_found = \
            parse_syllable_line_list(ground_truth_text_grid_file=textgrid_filename,
                                     parent_tier="line",
                                     child_tier=phoneme_tier)

        if is_file_exist:
            textgrid_file_number += 1
            melodic_line_dur_list += [syl_list[0][1] - syl_list[0][0] for syl_list in nested_syllable_list]
        if is_syllable_found:
            syllable_number += 1
            syllable_dur_list += [syl_onset_offset[1] - syl_onset_offset[0] for syl_list in nested_syllable_list for syl_onset_offset in syl_list[1]]
        if is_phoneme_found:
            phoneme_number += 1
            phoneme_dur_list += [phn_onset_offset[1] - phn_onset_offset[0] for phn_list in nested_phoneme_list for phn_onset_offset in phn_list[1]]

            for phn_name, phn_dur in [[phn_onset_offset[2], phn_onset_offset[1] - phn_onset_offset[0]]
                                      for phn_list in nested_phoneme_list for phn_onset_offset in phn_list[1]]:
                dict_phoneme_dur[phn_name] += [phn_dur]

        # data, samplerate = sf.read(wav_filename)

        # song_dur.append(data.shape[0]/float(samplerate))

    return song_dur, melodic_line_dur_list, syllable_dur_list, phoneme_dur_list, dict_phoneme_dur
