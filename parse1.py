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
details = []

new_doc = BeautifulSoup()

# magic = .new_tag("div", **{'class':'magic'})
# magic = .new_tag("div", **{'class':'magic'})
# soup.append(magic)
# magic = soup.new_tag("div")
# soup.append(magic)

details = None

def create_summary(heading_text):
  summary = new_doc.new_tag("summary")

  wrapper = new_doc.new_tag("span", **{'class':'wrapper'})

  heading = new_doc.new_tag("span", **{'class':'heading'})
  heading.string = heading_text
  wrapper.append(heading)

  pill = new_doc.new_tag("span", **{'class':'pill'})
  wrapper.append(pill)

  summary.append(wrapper)

  return summary

for el in soup.find('body').children:
  print("el:", el)

  el_copy = copy.copy(el)

  if (el.name == "h2"):
    details = new_doc.new_tag("details")
    new_doc.append(details)
    summary = create_summary(el.text)
    details.append(summary)
  else:
    print("other.......")
    if (details is None):
      new_doc.append(el_copy)
    else:
      details.append(el_copy)

# print("soup:", soup)
print("new_doc:", new_doc)

f= open("new_stuff.html","w+")
f.write(str(new_doc))
