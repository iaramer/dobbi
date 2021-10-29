import dobbi


def test_batch_execute_emoticons():
    string = ':) :D :)'
    dobbi_result = dobbi.collect() \
        .emoticon() \
        .batch_execute([string, string])
    actual = {'emoticon': {'TOKEN_EMOTICON_HAPPY_FACE_OR_SMILEY': 4,
                           'TOKEN_EMOTICON_LAUGHING_OR_BIG_GRIN_OR_LAUGH_WITH_GLASSES': 2}}
    assert dobbi_result == actual


def test_clean_emoticons():
    string = ':)word1:Dword2:)'
    dobbi_result = dobbi.clean() \
        .emoticon() \
        .execute(string)
    actual = 'word1 word2'
    assert dobbi_result == actual


def test_replace_emoticons():
    string = ':)word1:Dword2'
    dobbi_result = dobbi.replace() \
        .emoticon() \
        .execute(string)
    actual = 'TOKEN_EMOTICON_HAPPY_FACE_OR_SMILEY word1 TOKEN_EMOTICON_LAUGHING_OR_BIG_GRIN_OR_LAUGH_WITH_GLASSES word2'
    assert dobbi_result == actual
