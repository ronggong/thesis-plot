from src.textgridParser import textGrid2WordList
from src.textgridParser import wordListsParseByLines


def parse_syllable_line_list(ground_truth_text_grid_file):
    # parse line
    line_list = textGrid2WordList(ground_truth_text_grid_file, whichTier='line')

    # parse syllable
    syllable_list = textGrid2WordList(ground_truth_text_grid_file, whichTier='dianSilence')

    # parse lines of ground truth
    nested_syllable_lists, _, _ = wordListsParseByLines(line_list, syllable_list)

    return nested_syllable_lists