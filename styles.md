---
title: "Stylesheet!"
date: "2019-01-07"
tags: ["one", "two"]
keywords: hello, magic
published: true

---

# Stylesheet

------------------------------------------------------------

# Headings

# Heading h1
## Heading h2
### Heading h3
#### Heading h4
##### Heading h5
###### Heading h6

----
## Text
This is a paragraph.

Followed by another paragraph.

This sentence has some `inline code` (surround with single backticks).

----
## Code block
Use triple backticks:
```js
// some javascript
const magic = () => 3;
```

------------------------------------------------------------
## Text effects

Emphasis / italics: surround with *single asterisks* or _single underscores_.

Strong emphasis / bold: surround with **double asterisks** or __double underscores__.

Combined emphasis: surround with **_double asterisks + single underscores_**.

Strikethrough: surround with ~~double tildes~~.

------------------------------------------------------------
## Simple Lists

Unordered List
- Item 1
- Item 2
- Item 3

Unordered List
- Item 1
- Item 2
```
// Some code
1337
```
- Item 3

Ordered List
1. Item 1
1. Item 2
1. Item 3

Ordered List
1. Item 1
1. Item 2
```
// Some code
1337
```
1. Item 3

------------------------------------------------------------
## Nested Lists

Unordered List
- Item 1
- Item 1a
- Item 1b
- Item 2
```
// Some code
1337
```
- Item 2a
```
// Some code
1337
```
- Item 2b
- Item 3
- Item 3a
- Item 3b

------------------------------------------------------------
## Links
[Link to example.com](http://example.com)

------------------------------------------------------------
## Images

Images in Markdown differ from links only by a preceding exclamation point `!`


Inline style (local URL):
```
![Alt text](../images/yeah-nah.jpg)
```
![Alt text](../images/yeah-nah.jpg)

------------------------------------------------------------

Inline style (web URL):
```
![Alt text](https://bit.ly/2FmmdTx)
```

![Alt text](https://i.ytimg.com/vi/uuc9frxacfE/maxresdefault.jpg)

------------------------------------------------------------
Inline style with hover text:
```
![Alt text](../images/yeah-nah.jpg "This is hover text")
```
![Alt text](../images/yeah-nah.jpg "This is hover text")

------------------------------------------------------------
Reference style:
![Alt text][yeah-nah]

[yeah-nah]: /src/images/yeah-nah.jpg "This is hover text"

------------------------------------------------------------
Inline HTML style:
```
<img src="../images/yeah-nah.jpg" width="50" />
```
<img src="../images/yeah-nah.jpg" width="50" />

------------------------------------------------------------
## Tables

Table examples
- Name is left-aligned
- Suburb is center-aligned
- Postcode is right-aligned

Table 1
- Markdown is not aligned, but renders nicely
- Minimum of one `-` in each header cell

| Name | Suburb | Postcode |
| - | :-: | -: |
| Pikachu | Sydney | 2000 |
| Bulbasaur | Melbourne | 3000 |
| Charmander | Adelaide | 5000 |


Table 2
- Markdown is aligned

| Name       | Suburb      | Postcode |
| ---------- | :---------: | -------: |
| Pikachu    | Sydney      | 2000     |
| Bulbasaur  | Melbourne   | 3000     |
| Charmander | Adelaide    | 5000     |

------------------------------------------------------------
## Blockquotes

> Hello there. I am a blockquote.
> This is part of the same blockquote.

Hello. I am intervening text.

> Hello. I am another block quote.
> I can handle _markdown_ **yeah**!

------------------------------------------------------------
## Inline HTML

<h3>h3 heading</h3>

`<img />` <img src="../images/yeah-nah.jpg" width="50" />

