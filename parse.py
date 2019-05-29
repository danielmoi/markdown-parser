#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

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

# for index, tag in enumerate(soup.find_all('h2')):
#   if (index != 0):
#     tag.insert_before("</details>")
#   print("tag:", tag)
#   text = tag.string
#   print("text:", text)
#   converted = BeautifulSoup(markup.format(heading=text), 'html.parser')
#   tag.replace_with(converted)

# soup = BeautifulSoup("<html>data</html>")

# headings = soup.find_all('h2')

result = BeautifulSoup()

print("soup", soup.prettify())
headings = []
articles = []
article = []
# new_article = result.new_tag("article")
# for index, el in enumerate(soup.find('body').children):
for el in soup.find('body').children:
  print("-----------------")
  print("el:", el)
  print("article", article)
  # print("new_article:", new_article)
  # print("result:", result)
  # print("🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶")
  # print("new_article:", new_article)

  if (el.name == "h2"):
    print("We got a heading")
    # headings.append(el)


    if (article.count > 0):
      articles.append(article)

    article = []
    # result.append(new_article)
    # new_article = result.new_tag("article")
    # new_article.append(el)
    article.append(el)

  else:
    print("el:", el)
    # new_article.append(el)
    article.append(el)

articles.append(article)
# result.append(new_article)
print("-----------------------")
print("headings:", headings)
print("articles:", articles)

print("🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶🌶")
print("result:", result.prettify())
# for index, el in enumerate(headings):
#   ammended.append(headings)

for el in articles:
  print("el:", el)
  magic = el.find("h2")
  print("magic:", magic)
