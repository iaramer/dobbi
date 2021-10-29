import re
from abc import ABC, abstractmethod
from collections import Counter
from typing import Callable, List, Dict, Tuple, Any

from dobbi.collections.emoji import EMOJI
from dobbi.collections.emoticons import EMOTICONS


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
                s_ = func(str(s_))
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
            string = func(str(string))
        return string

    def regexp(self, regular_expression: str) -> Job:
        """
        Provides a custom regexp to remove all of its usages in the initial string.

        :param regular_expression: The regex to apply.
        :return: The instance of Job to be chained.
        """

        def _regexp(s_: str) -> str:
            return re.sub(regular_expression, '', s_)

        self.f.append(_regexp)
        return self

    def url(self) -> Job:
        """
        Removes http://... and https://... URLs.

        :return: The instance of Job to be chained.
        """

        def _url(s_: str) -> str:
            return re.sub(r'https?://\S+', '', s_)

        self.f.append(_url)
        return self

    def nickname(self) -> Job:
        """
        Removes @nickname type of words.

        :return: The instance of Job to be chained.
        """

        def _nickname(s_: str) -> str:
            return re.sub(r'@\w+', '', s_)

        self.f.append(_nickname)
        return self

    def hashtag(self) -> Job:
        """
        Removes @hashtag type of words.

        :return: The instance of Job to be chained.
        """

        def _hashtag(s_: str) -> str:
            return re.sub(r'#\w+', '', s_)

        self.f.append(_hashtag)
        return self

    def punctuation(self) -> Job:
        """
        Removes all the characters from the following list:
        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

        :return: The instance of Job to be chained.
        """

        def _punctuation(s_: str) -> str:
            return s_.translate(str.maketrans('', '', r'!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'))

        self.f.append(_punctuation)
        return self

    def whitespace(self) -> Job:
        """
        Replaces with ' ' (simple whitespace) all the whitespace symbols from the following list:
        \t\n\r\v\f

        :return: The instance of Job to be chained.
        """

        def _whitespace(s_: str) -> str:
            for ch in ['\t', '\n', '\r', '\v', '\f']:
                if ch in s_:
                    s_ = s_.replace(ch, ' ')
            return s_

        self.f.append(_whitespace)
        return self

    def html(self) -> Job:
        """
        Removes <html> type of words.

        :return: The instance of Job to be chained.
        """

        def _html(s_: str) -> str:
            return re.sub(r'<.*?>', '', s_)

        self.f.append(_html)
        return self

    def emoji(self) -> Job:
        """
        Removes all of the emojis.

        :return: The instance of Job to be chained.
        """

        def _emoji(s_: str) -> str:
            for e in reversed(list(EMOJI.keys())):
                s_ = s_.replace(e, ' ')
            return s_

        self.f.append(_emoji)
        return self

    def emoticon(self) -> Job:
        """
        Removes emoticons. Better to use after emoji().

        :return: The instance of Job to be chained.
        """

        def _emoticon(s_: str) -> str:
            for e in reversed(list(EMOTICONS.keys())):
                s_ = re.sub(e, ' ', s_)
            return s_

        self.f.append(_emoticon)
        return self


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

    def regexp(self, regular_expression: str, replacement='TOKEN_CUSTOM') -> Job:
        """
        Provides a custom regexp to replace all of its occurrences in the initial string.

        :param replacement: Token to replace.
        :param regular_expression: The regex to apply.
        :return: The instance of Job to be chained.
        """

        def _regexp(s_: str) -> str:
            return re.sub(regular_expression, replacement, s_)

        self.f.append(_regexp)
        return self

    def url(self, replacement='TOKEN_URL') -> Job:
        """
        Replaces http://... and https://... URLs.

        :param replacement: Token to replace.
        :return: The instance of Job to be chained.
        """

        def _url(s_: str) -> str:
            return re.sub(r'https?://\S+', replacement, s_)

        self.f.append(_url)
        return self

    def nickname(self, replacement='TOKEN_NICKNAME') -> Job:
        """
        Removes @nickname type of words.

        :param replacement: Token to replace.
        :return: The instance of Job to be chained.
        """

        def _nickname(s_: str) -> str:
            return re.sub(r'@\w+', replacement, s_)

        self.f.append(_nickname)
        return self

    def hashtag(self, replacement='TOKEN_HASHTAG') -> Job:
        """
        Removes @hashtag type of words.

        :param replacement: Token to replace.
        :return: The instance of Job to be chained.
        """

        def _hashtag(s_: str) -> str:
            return re.sub(r'#\w+', replacement, s_)

        self.f.append(_hashtag)
        return self

    def punctuation(self, replacement=' ') -> Job:
        """
        Replaces all the characters from the following list:
        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

        :param replacement: Token to replace.
        :return: The instance of Job to be chained.
        """

        def _punctuation(s_: str) -> str:
            return re.sub(r'[^\w\s]', replacement, s_)

        self.f.append(_punctuation)
        return self

    def whitespace(self, replacement=' ') -> Job:
        """
        Replaces with provided 'replacement' parameter all the whitespace symbols from the following list:
        \t\n\r\v\f

        :param replacement: Token to replace.
        :return: The instance of Job to be chained.
        """

        def _whitespace(s_: str) -> str:
            for ch in ['\t', '\n', '\r', '\v', '\f']:
                if ch in s_:
                    s_ = s_.replace(ch, replacement)
            return s_

        self.f.append(_whitespace)
        return self

    def html(self, replacement='TOKEN_HTML') -> Job:
        """
        Removes <html> type of words.

        :param replacement: Token to replace.
        :return: The instance of Job to be chained.
        """

        def _html(s_: str) -> str:
            return re.sub(r'<.*?>', replacement, s_)

        self.f.append(_html)
        return self

    def emoji(self) -> Job:
        """
        Replaces emojis with their description tokens.

        :return: The instance of Job to be chained.
        """

        def _emoji(s_: str) -> str:
            for e in reversed(list(EMOJI.keys())):
                token = ' ' + EMOJI[e] + ' '
                s_ = s_.replace(e, token)
            return s_

        self.f.append(_emoji)
        return self

    def emoticon(self) -> Job:
        """
        Finds emoticons. Better to use after emoji().

        :return: The instance of Job to be chained.
        """

        def _emoticon(s_: str) -> str:
            for e in reversed(list(EMOTICONS.keys())):
                token = ' ' + EMOTICONS[e] + ' '
                s_ = re.sub(e, token, s_)
            return s_

        self.f.append(_emoticon)
        return self


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
                for k, v in counter.items():
                    if k not in result[tag]:
                        result[tag][k] = 0
                    result[tag][k] += v
        return result

    def regexp(self, regular_expression: str) -> Job:
        """
        Provides a custom regexp to collect all of its occurrences in the initial string.

        :param regular_expression: The regex to apply.
        :return: The instance of Job to be chained.
        """

        def _regexp(s_: str) -> Tuple[str, Counter]:
            return 'regexp', Counter(re.findall(regular_expression, s_))

        self.f.append(_regexp)
        return self

    def url(self) -> Job:
        """
        Finds http://... and https://... URLs.

        :return: The instance of Job to be chained.
        """

        def _url(s_: str) -> Tuple[str, Counter]:
            return 'url', Counter(re.findall(r'https?://\S+', s_))

        self.f.append(_url)
        return self

    def nickname(self) -> Job:
        """
        Finds @nickname type of words.

        :return: The instance of Job to be chained.
        """

        def _nickname(s_: str) -> Tuple[str, Counter]:
            return 'nickname', Counter(re.findall(r'@\w+', s_))

        self.f.append(_nickname)
        return self

    def hashtag(self) -> Job:
        """
        Finds @hashtag type of words.

        :return: The instance of Job to be chained.
        """

        def _hashtag(s_: str) -> Tuple[str, Counter]:
            return 'hashtag', Counter(re.findall(r'#\w+', s_))

        self.f.append(_hashtag)
        return self

    def punctuation(self) -> Job:
        """
        Finds all the characters from the following list:
        !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

        :return: The instance of Job to be chained.
        """

        def _punctuation(s_: str) -> Tuple[str, Counter]:
            return 'punctuation', Counter(re.findall(r'[^\w\s]', s_))

        self.f.append(_punctuation)
        return self

    def whitespace(self) -> Job:
        """
        Finds all the whitespace symbols from the following list:
        \t\n\r\v\f

        :return: The instance of Job to be chained.
        """

        def _whitespace(s_: str) -> Tuple[str, Counter]:
            c = Counter()
            for ch in ['\t', '\n', '\r', '\v', '\f']:
                if ch in s_:
                    c[ch] = len(re.findall(ch, s_))
            return 'whitespace', c

        self.f.append(_whitespace)
        return self

    def html(self) -> Job:
        """
        Finds <html> type of words.

        :return: The instance of Job to be chained.
        """

        def _html(s_: str) -> Tuple[str, Counter]:
            return 'html', Counter(re.findall(r'<.*?>', s_))

        self.f.append(_html)
        return self

    def emoji(self) -> Job:
        """
        Finds emojis.

        :return: The instance of Job to be chained.
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

    def emoticon(self, ignore_emoji=True, ignore_url=True) -> Job:
        """
        Finds emoticons.

        :param ignore_emoji: Whether to ignore the emoji patterns (recommended).
        :param ignore_url: Whether to ignore the http/https type patterns.
        :return: The instance of Job to be chained.
        """

        def _emoticon(s_: str) -> Tuple[str, Counter]:
            if ignore_url:
                s_ = re.sub(r'https?://\S+', ' ', s_)
            if ignore_emoji:
                for e in reversed(list(EMOJI.keys())):
                    s_ = s_.replace(e, ' ')
            c = Counter()
            for e in EMOTICONS:
                emoticons_number = len(re.findall(e, s_))
                if emoticons_number > 0:
                    c[EMOTICONS[e]] = emoticons_number
            return 'emoticon', c

        self.f.append(_emoticon)
        return self
