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
from typing import Callable


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


class CleanJob(Job):
    """
    An internal class for performing a clean.
    """

    def function(self, rm_whitespace=True, lower=True) -> Callable:
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

    def execute(self, string: str, rm_whitespace=True, lower=True) -> str:
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
        Provide a custom regexp to remove all of its usages in the initial string.

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


def clean() -> CleanJob:
    """
    Initializes a work to clean the provided string by chaining.

    :return: Instance of Work object.

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

    def function(self, rm_whitespace=True, lower=True) -> Callable:
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

    def execute(self, string: str, rm_whitespace=True, lower=True) -> str:
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
        Provide a custom regexp to replace all of its occurrences in the initial string.

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


def replace() -> ReplaceJob:
    """
    Initializes a work to change the provided string with some token.

    :return: Instance of Work object.

    Example:

    dobbi.replace()\
        .hashtag('TOKEN_HASHTAG')\
        .nickname('USER')\
        .execute('Why #damn @alex33 is so harmful?')

    Result:

    'Why TOKEN_HASHTAG  USER is so harmful?'
    """
    return ReplaceJob()


def get_sock() -> None:
    """
    To free Dobby.

    :return: ???
    """
    print('Dobby has got a sock. Master threw it, and Dobby caught it, and Dobby – Dobby is free!')
