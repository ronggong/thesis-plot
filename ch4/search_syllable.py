from file_path import *
from src.textgrid_preprocessing import parse_syllable_line_list


def search_syllable(recordings, role_type, syl_pinyin):
    for rec in recordings:
        if rec[0] == "part1":
            data_path = nacta_data_path
            sub_folder = role_type
            wav_folder = "wav_left"
            textgrid_folder = "textgrid"
            if rec[2][:2] == "ls" or rec[2][:2] == "da":
                syllable_tier = "dianSilence"
            else:
                syllable_tier = "pinyin"
            phoneme_tier = "details"
        elif rec[0] == "part2":
            data_path = nacta_2017_data_path
            sub_folder = rec[1]
            wav_folder = "wav"
            textgrid_folder = "textgridDetails"
            syllable_tier = "dianSilence"
            phoneme_tier = "details"
        else:
            data_path = primary_school_data_path
            sub_folder = rec[1]+"/"+rec[2]
            wav_folder = "wav_left"
            textgrid_folder = "textgrid"
            syllable_tier = "dianSilence"
            phoneme_tier = "details"

        filename = rec[3]
        if "." in filename:
            filename = os.path.splitext(filename)[0]

        wav_filename = os.path.join(data_path, wav_folder, sub_folder, filename + ".wav")
        textgrid_filename = os.path.join(data_path, textgrid_folder, sub_folder, filename + ".textgrid")

        nested_phoneme_list, is_file_exist, is_phoneme_found = \
            parse_syllable_line_list(ground_truth_text_grid_file=textgrid_filename,
                                     parent_tier=syllable_tier,
                                     child_tier=phoneme_tier)

        if is_file_exist and is_phoneme_found:
            for ii, list_syl in enumerate(nested_phoneme_list):
                if list_syl[0][2] == syl_pinyin and ii != 0 and ii != len(nested_phoneme_list)-1:
                    return wav_filename, textgrid_filename, \
                           [nested_phoneme_list[ii-1], nested_phoneme_list[ii], nested_phoneme_list[ii+1]]