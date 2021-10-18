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

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections import Counter
from typing import Callable, List, Tuple, Dict

from emo.emoji import EMOJI
from emo.emoticons import EMOTICONS


class Job(ABC):
    """
    Abstract base class for the other job classes in the library.
    """

    def __init__(self):
        self.f = list()

    @abstractmethod
    def function(self) -> Callable:
        pass

    @abstractmethod
    def execute(self, string: str) -> str:
        pass

    @abstractmethod
    def regexp(self, regular_expression: str) -> Callable:
        pass

    @abstractmethod
    def url(self) -> Callable:
        pass

    @abstractmethod
    def nickname(self) -> Callable:
        pass

    @abstractmethod
    def hashtag(self) -> Callable:
        pass

    @abstractmethod
    def punctuation(self) -> Callable:
        pass

    @abstractmethod
    def whitespace(self) -> Callable:
        pass

    @abstractmethod
    def html(self) -> Callable:
        pass

    @abstractmethod
    def emoji(self) -> Callable:
        pass

    @abstractmethod
    def emoticon(self) -> Callable:
        pass


class CleanJob(Job):
    """
    An internal class for performing a clean.
    """

    def function(self, rm_whitespace=True, lower=False) -> Callable:
        """
        Creates a function, which is a combination of previously selected chained functions.

        :param lower: If the resulting string should be lowercase.
        :param rm_whitespace: If the extra whitespace should be removed.
        :return: A function that is the combination of previously chosen chained functions.
        """

        if rm_whitespace:
            self.f.append(lambda x: ' '.join(x.split()))
        if lower:
            self.f.append(lambda x: x.lower())

        def _func(s_) -> Callable:
            for func in self.f:
                s_ = func(s_)
            return s_

        return _func

    def execute(self, string: str, rm_whitespace=True, lower=False) -> str:
        """
        Returns a final string. Use this method to get an answer.

        :param lower: If the resulting string should be lowercase.
        :param string: The string to process.
        :param rm_whitespace: If the extra whitespace should be removed.
        :return: The cleaned string.
        """

        if rm_whitespace:
            self.f.append(lambda x: ' '.join(x.split()))
        if lower:
            self.f.append(lambda x: x.lower())

        for func in self.f:
            string = func(string)
        return string

    def regexp(self, regular_expression: str) -> CleanJob:
        """
        Provides a custom regexp to remove all of its usages in the initial string.

        :param regular_expression: The regex to apply.
        :return: The instance of Work to be chained.
        """

        def _regexp(s_: str) -> str:
            return re.sub(regular_expression, '', s_)

        self.f.append(_regexp)
        return self

    def url(self) -> CleanJob:
        """
        Removes http://... and https://... URLs.

        :return: The instance of Work to be chained.
        """

        def _url(s_: str) -> str:
            return re.sub(r'https?://\S+', '', s_)

        self.f.append(_url)
        return self

    def nickname(self) -> CleanJob:
        """
        Removes @nickname type of words.

        :return: The instance of Work to be chained.
        """

        def _nickname(s_: str) -> str:
            return re.sub(r'@\w+', '', s_)

        self.f.append(_nickname)
        return self

    def hashtag(self) -> CleanJob:
        """
        Removes @hashtag type of words.

        :return: The instance of Work to be chained.
        """

        def _hashtag(s_: str) -> str:
            return re.sub(r'#\w+', '', s_)

        self.f.append(_hashtag)
        return self

    def punctuation(self) -> CleanJob:
        """
        Removes all the characters from the following list:
        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

        :return: The instance of Work to be chained.
        """

        def _punctuation(s_: str) -> str:
            return s_.translate(str.maketrans('', '', r'!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'))

        self.f.append(_punctuation)
        return self

    def whitespace(self) -> CleanJob:
        """
        Replaces with ' ' (simple whitespace) all the whitespace symbols from the following list:
        \t\n\r\v\f

        :return: The instance of Work to be chained.
        """

        def _whitespace(s_: str) -> str:
            for ch in ['\t', '\n', '\r', '\v', '\f']:
                if ch in s_:
                    s_ = s_.replace(ch, ' ')
            return s_

        self.f.append(_whitespace)
        return self

    def html(self) -> CleanJob:
        """
        Removes <html> type of words.

        :return: The instance of Work to be chained.
        """

        def _html(s_: str) -> str:
            return re.sub(r'<.*?>', '', s_)

        self.f.append(_html)
        return self

    def emoji(self) -> CleanJob:
        """
        Removes all of the emojis.

        :return: The instance of Work to be chained.
        """

        def _emoji(s_: str) -> str:
            for e in reversed(EMOJI):
                s_ = s_.replace(e, '')
            return s_

        self.f.append(_emoji)
        return self

    def emoticon(self) -> CleanJob:
        """
        Removes emoticons.

        :return: The instance of Work to be chained.
        """

        def _emoticon(s_: str) -> str:
            for e in reversed(EMOTICONS):
                s_ = re.sub(e, '', s_)
            return s_

        self.f.append(_emoticon)
        return self


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


class ReplaceJob(Job):
    """
    An internal class for performing words replacement.
    """

    def function(self, rm_whitespace=True, lower=False) -> Callable:
        """
        Creates a function, which is a combination of previously selected chained functions.

        :param lower: If the resulting string should be lowercase.
        :param rm_whitespace: If the extra whitespace should be removed.
        :return: A function that is the combination of previously chosen chained functions.
        """

        if rm_whitespace:
            self.f.append(lambda x: ' '.join(x.split()))
        if lower:
            self.f.append(lambda x: x.lower())

        def _func(s_) -> Callable:
            for func in self.f:
                s_ = func(s_)
            return s_

        return _func

    def execute(self, string: str, rm_whitespace=True, lower=False) -> str:
        """
        Returns a final string. Use this method to get an answer.

        :param lower: If the resulting string should be lowercase.
        :param string: The string to process.
        :param rm_whitespace: if the extra whitespace should be removed.
        :return: The processed string.
        """

        if rm_whitespace:
            self.f.append(lambda x: ' '.join(x.split()))
        if lower:
            self.f.append(lambda x: x.lower())

        for func in self.f:
            string = func(string)
        return string

    def regexp(self, regular_expression: str, replacement='TOKEN_CUSTOM') -> ReplaceJob:
        """
        Provides a custom regexp to replace all of its occurrences in the initial string.

        :param replacement: Token to replace.
        :param regular_expression: The regex to apply.
        :return: The instance of Work to be chained.
        """

        def _regexp(s_: str) -> str:
            return re.sub(regular_expression, replacement, s_)

        self.f.append(_regexp)
        return self

    def url(self, replacement='TOKEN_URL') -> ReplaceJob:
        """
        Replaces http://... and https://... URLs.

        :param replacement: Token to replace.
        :return: The instance of Work to be chained.
        """

        def _url(s_: str) -> str:
            return re.sub(r'https?://\S+', replacement, s_)

        self.f.append(_url)
        return self

    def nickname(self, replacement='TOKEN_NICKNAME') -> ReplaceJob:
        """
        Removes @nickname type of words.

        :param replacement: Token to replace.
        :return: The instance of Work to be chained.
        """

        def _nickname(s_: str) -> str:
            return re.sub(r'@\w+', replacement, s_)

        self.f.append(_nickname)
        return self

    def hashtag(self, replacement='TOKEN_HASHTAG') -> ReplaceJob:
        """
        Removes @hashtag type of words.

        :param replacement: Token to replace.
        :return: The instance of Work to be chained.
        """

        def _hashtag(s_: str) -> str:
            return re.sub(r'#\w+', replacement, s_)

        self.f.append(_hashtag)
        return self

    def punctuation(self, replacement=' TOKEN_PUNCTUATION ') -> ReplaceJob:
        """
        Replaces all the characters from the following list:
        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

        :param replacement: Token to replace.
        :return: The instance of Work to be chained.
        """

        def _punctuation(s_: str) -> str:
            return re.sub(r'[^\w\s]', replacement, s_)

        self.f.append(_punctuation)
        return self

    def whitespace(self, replacement=' ') -> ReplaceJob:
        """
        Replaces with provided 'replacement' parameter all the whitespace symbols from the following list:
        \t\n\r\v\f

        :param replacement: Token to replace.
        :return: The instance of Work to be chained.
        """

        def _whitespace(s_: str) -> str:
            for ch in ['\t', '\n', '\r', '\v', '\f']:
                if ch in s_:
                    s_ = s_.replace(ch, replacement)
            return s_

        self.f.append(_whitespace)
        return self

    def html(self, replacement='TOKEN_HTML') -> ReplaceJob:
        """
        Removes <html> type of words.

        :param replacement: Token to replace.
        :return: The instance of Work to be chained.
        """

        def _html(s_: str) -> str:
            return re.sub(r'<.*?>', replacement, s_)

        self.f.append(_html)
        return self

    def emoji(self) -> ReplaceJob:
        """
        Replaces emojis with their description tokens.

        :return: The instance of Work to be chained.
        """

        def _emoji(s_: str) -> str:
            for e in reversed(EMOJI):
                s_ = s_.replace(e, ' ' + EMOJI[e] + ' ')
            return s_

        self.f.append(_emoji)
        return self

    def emoticon(self) -> ReplaceJob:
        """
        Finds emoticons.

        :return: The instance of Work to be chained.
        """

        def _emoticon(s_: str) -> str:
            for e in reversed(EMOTICONS):
                s_ = s_.replace(e, ' ' + EMOTICONS[e] + ' ')
            return s_

        self.f.append(_emoticon)
        return self


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


class CollectionJob(Job):
    """
    An internal class for performing words collection.
    """

    def function(self) -> Callable:
        """
        Creates a function, which is a combination of previously selected chained functions.

        :return: A function that is the combination of previously chosen chained functions.
        """

        def _func(s_) -> List[Counter]:
            result = list()
            for func in self.f:
                result.append(func(s_))
            return result

        return _func

    def execute(self, string: str) -> Dict[str, Dict]:
        """
        Returns a list of strings counted. Use this method to get an answer.

        :param string: The string to process.
        :return: The counted patterns.
        """

        result = dict()
        for func in self.f:
            tag, counter = func(string)
            result[tag] = dict(counter)
        return result

    def batch_execute(self, strings: List[str]) -> Dict[str, Dict]:
        """
        Returns a list of strings counted. Use this method to get an answer.

        :param strings: The strings to process.
        :return: The counted patterns.
        """

        result = dict()
        for string in strings:
            for func in self.f:
                tag, counter = func(string)
                if tag not in result:
                    result[tag] = dict()
                result[tag] = result[tag] | dict(counter)
        return result

    def regexp(self, regular_expression: str) -> CollectionJob:
        """
        Provides a custom regexp to collect all of its occurrences in the initial string.

        :param regular_expression: The regex to apply.
        :return: The instance of Work to be chained.
        """

        def _regexp(s_: str) -> Tuple[str, Counter]:
            return 'regexp', Counter(re.findall(regular_expression, s_))

        self.f.append(_regexp)
        return self

    def url(self) -> CollectionJob:
        """
        Finds http://... and https://... URLs.

        :return: The instance of Work to be chained.
        """

        def _url(s_: str) -> Tuple[str, Counter]:
            return 'url', Counter(re.findall(r'https?://\S+', s_))

        self.f.append(_url)
        return self

    def nickname(self) -> CollectionJob:
        """
        Finds @nickname type of words.

        :return: The instance of Work to be chained.
        """

        def _nickname(s_: str) -> Tuple[str, Counter]:
            return 'nickname', Counter(re.findall(r'@\w+', s_))

        self.f.append(_nickname)
        return self

    def hashtag(self) -> CollectionJob:
        """
        Finds @hashtag type of words.

        :return: The instance of Work to be chained.
        """

        def _hashtag(s_: str) -> Tuple[str, Counter]:
            return 'hashtag', Counter(re.findall(r'#\w+', s_))

        self.f.append(_hashtag)
        return self

    def punctuation(self) -> CollectionJob:
        """
        Finds all the characters from the following list:
        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

        :return: The instance of Work to be chained.
        """

        def _punctuation(s_: str) -> Tuple[str, Counter]:
            return 'punctuation', Counter(re.findall(r'[^\w\s]', s_))

        self.f.append(_punctuation)
        return self

    def whitespace(self) -> CollectionJob:
        """
        Finds all the whitespace symbols from the following list:
        \t\n\r\v\f

        :return: The instance of Work to be chained.
        """

        def _whitespace(s_: str) -> Tuple[str, Counter]:
            c = Counter()
            for ch in ['\t', '\n', '\r', '\v', '\f']:
                if ch in s_:
                    c[ch] = len(re.findall(ch, s_))
            return 'whitespace', c

        self.f.append(_whitespace)
        return self

    def html(self) -> CollectionJob:
        """
        Finds <html> type of words.

        :return: The instance of Work to be chained.
        """

        def _html(s_: str) -> Tuple[str, Counter]:
            return 'html', Counter(re.findall(r'<.*?>', s_))

        self.f.append(_html)
        return self

    def emoji(self) -> CollectionJob:
        """
        Finds emojis.

        :return: The instance of Work to be chained.
        """

        def _emoji(s_: str) -> Tuple[str, Counter]:
            c = Counter()
            for e in EMOJI:
                emojis_number = s_.count(e)
                if emojis_number > 0:
                    c[EMOJI[e]] = emojis_number
            return 'emoji', c

        self.f.append(_emoji)
        return self

    def emoticon(self, ignore_url=True) -> CollectionJob:
        """
        Finds emoticons.

        :param ignore_url: Whether to ignore the http/https type patterns
        :return: The instance of Work to be chained.
        """

        def _emoticon(s_: str) -> Tuple[str, Counter]:
            if ignore_url:
                s_ = re.sub(r'https?://\S+', ' ', s_)
            c = Counter()
            for e in EMOTICONS:
                emoticons_number = len(re.findall(e, s_))
                if emoticons_number > 0:
                    c[EMOTICONS[e]] = emoticons_number
            return 'emoticon', c

        self.f.append(_emoticon)
        return self


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
