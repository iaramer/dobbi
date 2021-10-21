# Description

An open-source NLP library: fast text cleaning and preprocessing.

# Overview

This library provides a quick and ready-to-use text preprocessing tools for text cleaning and normalization.
You can simply remove hashtags, nicknames, emoji, url addresses, punctuation, whitespace and etc.

## Installation

###  Getting it

To download dobbi, either fork this github repo or simply use [Pypi](https://pypi.org/project/dobbi/) via pip.

```sh
$ pip install dobbi
```

# Usage

Import the library.

```Python
import dobbi
```

## Interaction

The library uses method chaining in order to simplify text processing:

```Python
dobbi.clean()\
    .hashtag()\
    .nickname()\
    .url()\
    .execute('Check here: https://some-url.com')
```

## Supported methods and patterns

The process consists of three stages:
1. Initialization methods: initialize a dobbi Work object
2. Intermediate methods: chain needed patterns in the needed order
3. Terminal methods:

Initialization functions:
* `dobbi.clean()`
* `dobbi.collect()`
* `dobbi.replace()`

Intermediate methods (pattern processing choice):

* `regexp()` - custom regular expressions
* `url()` - URLs
* `html()` - HTML and "<...>" type markups
* `punctuation()` - punctuation
* `hashtag()` - hashtags
* `emoji()` - [emoji](https://en.wikipedia.org/wiki/Emoji)
* `emoticons()` - [emoticons](https://en.wikipedia.org/wiki/List_of_emoticons)
* `whitespace()` - whitespaces
* `nickname()` - @-starting nicknames

Terminal methods:

* `execute(str)` - executes chosen methods on the provided string.
* `function()` - returns a function which is a combination of the chosen methods.

## Examples

### 1) Clean a random Twitter message

```Python
dobbi.clean()\
    .hashtag()\
    .nickname()\
    .url()\
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result

```Python
'Why is so funny? Check here:'
```

### 2) Replace nickname and url with tokens

```Python
dobbi.replace()\
    .hashtag('')\
    .nickname()\
    .url('CUSTOM_URL_TOKEN')\
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result

```Python
'Why TOKEN_NICKNAME is so funny? Check here: CUSTOM_URL_TOKEN'
```

### 3) Get text cleanup function (one-liner)

*(!) Please, try to avoid the in-line method chaining, as it is significantly less readable.*

```Python
func = dobbi.clean().url().hashtag().punctuation().whitespace().html().function()
func('\t #fun #lol    Why  @Alex33 is so... funny? <tag> \nCheck\there: https://some-url.com')
```

Result

```Python
'Why Alex33 is so funny Check here'
```

4) Chain regexp methods

```Python
dobbi.clean()\
    .regexp('#\w+')\
    .regexp('@\w+')\
    .regexp('https?://\S+')\
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result

```Python
'Why is so funny? Check here:'
```

## Additional

Please pay attention that the functions are applied in the order you specify.
So, you're better to chain .punctuation() as one of the last functions.
