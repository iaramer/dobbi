# Description

An open-source NLP library: fast text cleaning and preprocessing.

# Overview

This library provides a quick and ready-to-use text preprocessing tools for text cleaning and normalization.
You can simply remove hashtags, nicknames, emoji, url addresses, punctuation, whitespace and etc.

## Installation

###  Getting it

To download dobbi, either fork this github repo or simply use Pypi via pip.

```sh
$ pip install dobbi
```

# Usage

Import the library.

```Python
import dobbi
```

## Interaction

The library uses method chaining in order to simplify tasks processing:

```Python
dobbi.clean()\
    .hashtag()\
    .nickname()\
    .url()\
    .execute('Check here: https://some-url.com')
```

## Supported patterns

The library supports the following patterns:
* URL
* Punctuation
* Emoji & emoticons
* Hashtags
* Whitespaces
* Nicknames
* HTML
* Custom regexp

## Examples

1) Clean a twitter message

```Python
dobbi.clean()\
    .hashtag()\
    .nickname()\
    .url()\
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result: 'Why is so funny? Check here:'

2) Replace nickname and url with tokens

```Python
dobbi.replace()\
    .hashtag('')\
    .nickname()\
    .url('CUSTOM_URL_TOKEN')\
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result: 'Why TOKEN_NICKNAME is so funny? Check here: CUSTOM_URL_TOKEN'

3) Get text cleanup function

```Python
func = dobbi.clean().url().hashtag().punctuation().whitespace().html().function()
func('\t #fun #lol    Why  @Alex33 is so... funny? <tag> \nCheck\there: https://some-url.com')
```

Result: 'Why Alex33 is so funny Check here'

*(!) Please, try to avoid the in-line method chaining, as it is significantly less readable.* 

## Additional

Please pay attention that the functions are applied in the order you specify.
So, you're better to chain .punctuation() as one of the last functions.
