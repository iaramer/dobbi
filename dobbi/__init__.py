"""
This library provides a quick and ready-to-use text preprocessing tools for text cleaning and normalization.
You can simply remove hashtags, nicknames, emoji, url addresses, punctuation, whitespace and etc.

Examples:

1) Clean a twitter message

dobbi.clean()\
    .hashtag()\
    .nickname()\
    .url()\
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')

Result: 'Why is so funny? Check here:'

2) Replace nickname and url with tokens

dobbi.replace()\
    .hashtag('')\
    .nickname()\
    .url('CUSTOM_URL_TOKEN')\
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')

Result: 'Why TOKEN_NICKNAME is so funny? Check here: CUSTOM_URL_TOKEN'

3) Get text cleanup function

func = dobbi.clean().url().hashtag().punctuation().whitespace().html().function()  # One-liner is less readable.
func('\t #fun #lol    Why  @Alex33 is so... funny? <tag> \nCheck\there: https://some-url.com')

Result: 'Why Alex33 is so funny Check here'

Please pay attention that the functions are applied in the order you specify.
So, chain .punctuation() as one of the last functions.
"""

from dobbi.job import CleanJob, ReplaceJob, CollectionJob


def clean() -> CleanJob:
    """
    Initialization function. Initializes a work to clean the provided string by chaining.

    :return: Instance of the Work object.

    Example:

    dobbi.clean()\
        .hashtag()\
        .nickname()\
        .execute('Why #damn @alex33 is so harmful?')

    Result:

    'Why is so harmful?'
    """
    return CleanJob()


def replace() -> ReplaceJob:
    """
    Initialization function. Initializes a work to change the provided string with some token.

    :return: Instance of the Work object.

    Example:

    dobbi.replace()\
        .hashtag('TOKEN_HASHTAG')\
        .nickname('USER')\
        .execute('Why #damn @alex33 is so harmful?')

    Result:

    'Why TOKEN_HASHTAG  USER is so harmful?'
    """
    return ReplaceJob()


def collect() -> CollectionJob:
    """
    Initialization function. Initializes a work to collect the words by some pattern.

    :return: Instance of the Work object.

    Example:

    dobbi.collect()\
        .hashtag()\
        .nickname()\
        .execute('Why #damn @alex33 is so harmful?')

    Result:

    'Why TOKEN_HASHTAG  USER is so harmful?'
    """
    return CollectionJob()


def get_sock() -> None:
    """
    To free Dobby.

    :return: ???
    """
    print('Dobby has got a sock. Master threw it, and Dobby caught it, and Dobby – Dobby is free!')
