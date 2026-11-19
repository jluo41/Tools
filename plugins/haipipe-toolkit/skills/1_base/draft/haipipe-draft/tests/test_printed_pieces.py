"""health row `printed`: a sentence cut by a page break and a float caption still counts as printed (t02_results 261118)."""
from src.folder_health import in_pieces

PDF = "end of page For 4 Figure 4: Error by scale and subgroup. gender, the change was small across all ten models. next"


def test_a_sentence_split_by_a_caption_is_found():
    assert in_pieces("For gender, the change was small across all ten models.", PDF)


def test_a_sentence_not_printed_is_not_found():
    assert not in_pieces("For age, the change was large.", PDF)


def test_words_out_of_order_are_not_found():
    assert not in_pieces("the change was small For gender,", PDF)
