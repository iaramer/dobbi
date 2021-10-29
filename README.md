<h1 align='center'>
 🌴 dobbi 🦕
</h1>
<p align='center'>
Takes care of all of this boring NLP stuff
 <br>
 <br>
 <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/dobbi">
 <a href='https://pypi.org/project/dobbi/'><img alt="Version" src="https://img.shields.io/pypi/v/dobbi?logo=pypi"></a>
 <a href='https://opensource.org/licenses/Apache-2.0'><img alt="GitHub" src="https://img.shields.io/github/license/iaramer/dobbi"></a><br> 
</p>

# Description

An open-source NLP library: fast text cleaning and preprocessing.

## TL;DR

This library provides a quick and ready-to-use text preprocessing tools for text cleaning and normalization.
You can simply remove hashtags, nicknames, emoji, url addresses, punctuation, whitespace and whatever.

## Installation

To download *dobbi*, either fork this GitHub repo or simply use [Pypi](https://pypi.org/project/dobbi/) via pip:

```sh
$ pip install dobbi
```

## Usage

Import the library:

```Python
import dobbi
```

## Interaction

The library uses method chaining in order to simplify text processing:

```Python
dobbi.clean() \
    .hashtag() \
    .nickname() \
    .url() \
    .execute('Check here: https://some-url.com')
```

## Supported methods and patterns

The process consists of three stages:
1. Initialization methods: initialize a *dobbi* Work object
2. Intermediate methods: chain patterns in the needed order
3. Terminal methods: choose if you need a function or a result

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
* `whitespace()` - any type of whitespaces
* `nickname()` - @-starting nicknames

Terminal methods:

* `execute(str)` - executes chosen methods on the provided string.
* `function()` - returns a function which is a combination of the chosen methods.

## Examples

### 1) Clean a random Twitter message

```Python
dobbi.clean() \
    .hashtag() \
    .nickname() \
    .url() \
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result:

```Python
'Why is so funny? Check here:'
```

### 2) Replace nicknames and urls with tokens

```Python
dobbi.replace() \
    .hashtag('') \
    .nickname() \
    .url('__CUSTOM_URL_TOKEN__') \
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result:

```Python
'Why TOKEN_NICKNAME is so funny? Check here: __CUSTOM_URL_TOKEN__'
```

### 3) Get the text cleanup function (one-liner)

~~Please, try to avoid the in-line method chaining, as it is less readable.~~ Do as your heart tells you.

```Python
func = dobbi.clean().url().hashtag().punctuation().whitespace().html().function()
func('\t #fun #lol    Why  @Alex33 is so... funny? <tag> \nCheck\there: https://some-url.com')
```

Result:

```Python
'Why Alex33 is so funny Check here'
```

4) Chain regexp methods

```Python
dobbi.clean() \
    .regexp('#\w+') \
    .regexp('@\w+') \
    .regexp('https?://\S+') \
    .execute('#fun #lol    Why  @Alex33 is so funny? Check here: https://some-url.com')
```

Result:

```Python
'Why is so funny? Check here:'
```

## Additional

Please pay attention that the functions are applied in the order you've specified them.
So, you're better to chain `.punctuation()` as one of the last functions.

## Call for collaboration 🤗

If you enjoyed the project I would be grateful if you supported it :)

Below is the list of useful features I would be happy to share with you:

- [ ] Finding bugs
- [ ] Making code optimizations
- [ ] Writing tests
- [ ] Help with new features development
