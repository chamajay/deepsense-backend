import preprocess


def test_remove_url():
    assert preprocess.remove_url("https://www.google.com you can use this link") == "you can use this link"
    assert preprocess.remove_url("visit from https://www.redit.com here") == "visit from  here"


def test_url_remove_symbols_digits():
    assert preprocess.remove_symbols_digits("I'll come at 8 o'clock") == "Ill come at  oclock"


def test_expand_abbreviations():
    assert preprocess.expand_abbreviations("wtf") == "what the fuck"
    assert preprocess.expand_abbreviations("omg") == "oh my god"


def test_convert_emoji_to_text():
    assert preprocess.convert_emoji_to_text("😂") == "face_with_tears_of_joy"
    assert preprocess.convert_emoji_to_text("😭") == "loudly_crying_face"


def test_remove_accent_chars():
    assert preprocess.remove_accented_chars("ÐèèpŠéńšê") == "DeepSense"


def test_remove_symbols_digits():
    assert preprocess.remove_symbols_digits("#I hate !this @life") == "I hate this life"


def test_remove_special_chars():
    # Double quotes remove check.
    assert preprocess.remove_special_chars('she said "I love you"') == "she said I love you"
    # Remove  white spaces and limit it in to one space check.
    assert preprocess.remove_special_chars("I don't      need you") == "I don't need you"

    assert preprocess.remove_special_chars("I know \nwho you are") == "I know  who you are"


def test_remove_extra_whitespace():
    # Check leading and trailing whitespace remove
    assert preprocess.remove_extra_whitespace(" I feel like ending my life  ") == "I feel like ending my life"
