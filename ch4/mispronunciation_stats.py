from src.csv_prepossessing import open_csv_recordings
from src.textgrid_preprocessing import parse_syllable_line_list
from src.csv_prepossessing import write_csv_two_columns_list
import operator
import matplotlib.pyplot as plt
import numpy as np
from file_path import *


def parse_recordings(rec):
    if rec[0] == "part1":
        data_path = nacta_data_path
        sub_folder = rec[2]
        textgrid_folder = "textgrid"
        wav_folder = "wav_left"
        syllable_tier = "dian"
    elif rec[0] == "part2":
        data_path = nacta_2017_data_path
        sub_folder = rec[2]
        textgrid_folder = "textgridDetails"
        wav_folder = "wav"
        syllable_tier = "dianSilence"
    else:
        data_path = primary_school_data_path
        sub_folder = rec[1] + "/" + rec[2]
        textgrid_folder = "textgrid"
        wav_folder = "wav_left"
        syllable_tier = "dianSilence"

    filename = rec[3]
    line_tier = "line"
    longsyllable_tier = "longsyllable"
    phoneme_tier = "details"
    special_tier = "special"
    special_class_tier = "specialClass"

    return data_path, sub_folder, textgrid_folder, \
           wav_folder, filename, line_tier, longsyllable_tier,\
           syllable_tier, phoneme_tier, special_tier, special_class_tier


def unique_list(duplicate_list):
    uni_list = []
    for l in duplicate_list:
        if l not in uni_list:
            uni_list.append(l)
    return uni_list


def plot_h_bar(people, performance, figsize, figname):

    fig, ax = plt.subplots(figsize=figsize)
    # Example data
    y_pos = np.arange(len(people))
    error = np.random.rand(len(people))

    ax.barh(y_pos, performance, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Occurrence')
    ax.autoscale(enable=True, axis='both', tight=True)
    plt.tight_layout()
    plt.savefig("figs/"+figname)


if __name__ == "__main__":
    recordings_train = open_csv_recordings("mispronunciation_filelist_train.csv")
    recordings_test = open_csv_recordings("mispronunciation_filelist_test.csv")

    dict_special = dict()
    dict_jiantuan = dict()

    num_line = 0
    num_syllable = 0
    num_special = 0
    num_jiantuan = 0
    num_phoneme = 0

    list_special = []
    list_jian = []

    for rec in recordings_train+recordings_test:
        data_path, sub_folder, textgrid_folder, \
        wav_folder, filename, line_tier, longsyllable_tier, syllable_tier, \
        phoneme_tier, special_tier, special_class_tier = parse_recordings(rec)

        textgrid_filename = os.path.join(data_path, textgrid_folder, sub_folder, filename + ".textgrid")

        nested_syllable_list, is_file_exist, is_syllable_found = \
            parse_syllable_line_list(ground_truth_text_grid_file=textgrid_filename,
                                     parent_tier=longsyllable_tier,
                                     child_tier=syllable_tier)

        nested_special_list, is_file_exist, is_special_found = \
            parse_syllable_line_list(ground_truth_text_grid_file=textgrid_filename,
                                     parent_tier=longsyllable_tier,
                                     child_tier=special_tier)

        nested_specialClass_list, is_file_exist, is_specialClass_found = \
            parse_syllable_line_list(ground_truth_text_grid_file=textgrid_filename,
                                     parent_tier=longsyllable_tier,
                                     child_tier=special_class_tier)

        nested_phoneme_list, is_file_exist, is_phoneme_found = \
            parse_syllable_line_list(ground_truth_text_grid_file=textgrid_filename,
                                     parent_tier=longsyllable_tier,
                                     child_tier=phoneme_tier)

        for ii_line in range(len(nested_special_list)):
            line_special_list = nested_special_list[ii_line]
            if line_special_list[0][2] != "1":
                num_line += 1
                line_syllable_list = nested_syllable_list[ii_line]
                line_specialClass_list = nested_specialClass_list[ii_line]
                line_phoneme_list = nested_phoneme_list[ii_line]
                num_syllable += len(line_syllable_list[1])
                num_phoneme += len(line_phoneme_list[1])

                for ii_syl in range(len(line_specialClass_list[1])):
                    special_class = line_specialClass_list[1][ii_syl][2]
                    try:
                        syllable = line_syllable_list[1][ii_syl][2]
                    except IndexError:
                        raise IndexError(rec, ii_line)
                    if special_class == "1":  # shangkou
                        num_special += 1
                        shangkou = line_special_list[1][ii_syl][2]
                        dict_special[shangkou] = dict_special.get(shangkou, 0) + 1
                        list_special.append([syllable, shangkou])
                        # print("shangkou", syllable, shangkou, rec, ii_line)
                    if special_class == "2":  # jiantuan
                        num_jiantuan += 1
                        jiantuan = line_special_list[1][ii_syl][2]
                        dict_jiantuan[jiantuan] = dict_jiantuan.get(jiantuan, 0) + 1
                        list_jian.append([syllable, jiantuan])
                        # print("jiantuan", syllable, jiantuan, rec, ii_line)

    # sort the special and jiantuan dictionary to list
    sorted_dict_special = sorted(dict_special.items(), key = operator.itemgetter(1), reverse=True)
    sorted_dict_jiantuan = sorted(dict_jiantuan.items(), key = operator.itemgetter(1), reverse=True)

    print(sorted_dict_special)
    print(sorted_dict_jiantuan)
    print(num_line, num_syllable, num_special, num_jiantuan, num_phoneme)

    # special_list = [sp[0] for sp in sorted_dict_special]
    # special_num = [sp[1] for sp in sorted_dict_special]
    # plot_h_bar(special_list, special_num, (5, 15), "special_syllable.png")
    #
    # jiantuan_list = [jt[0] for jt in sorted_dict_jiantuan]
    # jiantuan_num = [jt[1] for jt in sorted_dict_jiantuan]
    # plot_h_bar(jiantuan_list, jiantuan_num, (5, 4), "jiantuan_syllable.png")

    list_special_unique = unique_list(list_special)
    list_jian_unique = unique_list(list_jian)

    print(list_special_unique)
    print(list_jian_unique)

    write_csv_two_columns_list(two_columns_list=list_special_unique,
                               filename="special_unique.csv")
    write_csv_two_columns_list(two_columns_list=list_jian_unique,
                               filename="jian_unique.csv")