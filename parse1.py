#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import copy

markup = """
  <details>
    <summary>
      <span class="wrapper">
        <span class="heading">{heading}</span>
        <span class="pill">1/6</span>
      </span>
    </summary>
"""

with open("./out/documents/three.html") as f:
    soup = BeautifulSoup(f, 'html.parser')



print("soup", soup.prettify())
headings = []
articles = []
article = []

new_doc = BeautifulSoup()

# magic = .new_tag("div", **{'class':'magic'})
# magic = .new_tag("div", **{'class':'magic'})
# soup.append(magic)
# magic = soup.new_tag("div")
# soup.append(magic)

article = None

for el in soup.find('body').children:
  print("el:", el)

  el_copy = copy.copy(el)
  new_doc.append(el_copy)

  if (el.name == "h2"):
    article = new_doc.new_tag("article")
    print("heading.........")
    print("article.contents:", article.contents)
    print("article.is_empty_element:", article.is_empty_element)
    new_doc.append(article)
    article.append(el_copy)
  else:
    print("other.......")
    if (article is None):
      new_doc.append(el_copy)
    else:
      article.append(el_copy)

# print("soup:", soup)
print("new_doc:", new_doc)

f= open("new_stuff.html","w+")
f.write(str(new_doc))
