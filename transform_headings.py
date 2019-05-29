#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import copy
import os

def create_summary(doc, heading_text):
  summary = doc.new_tag("summary")

  wrapper = doc.new_tag("span", **{'class':'wrapper'})

  heading = doc.new_tag("span", **{'class':'heading'})
  heading.string = heading_text
  wrapper.append(heading)

  pill = doc.new_tag("span", **{'class':'pill'})
  wrapper.append(pill)

  summary.append(wrapper)

  return summary

def main(path):
  print("path:", path)
  with open(path) as f:
      soup = BeautifulSoup(f, 'html.parser')

  print("soup:", soup)
  with open("./header.html") as header_html:
    header = BeautifulSoup(header_html, 'html.parser')

  new_doc = BeautifulSoup("<!DOCTYPE html>")

  html = new_doc.new_tag("html", lang="en")
  body = new_doc.new_tag("body")

  details = None

  for el in soup.find('body').children:
    # print("el:", el)

    el_copy = copy.copy(el)

    if (el.name == "h2"):
      details = new_doc.new_tag("details")
      body.append(details)
      summary = create_summary(new_doc, el.text)
      details.append(summary)
    else:
      if (details is None):
        body.append(el_copy)
      else:
        details.append(el_copy)

  html.append(header)
  html.append(body)
  new_doc.append(html)

  # print("soup:", soup)
  print("new_doc:", new_doc)

  parent_dir = os.path.abspath(__file__)
  print("parent_dir:", parent_dir)
  huh = os.path.dirname(path)
  print("huh:", huh)
  parts = path.split("/")
  print("parts:", parts)
  new_parts = ["./transformed"] + parts[2:]
  output_path = "/".join(new_parts)

  if not os.path.exists(os.path.dirname(output_path)):
    os.makedirs(os.path.dirname(output_path))


  f= open(output_path, "w+")
  f.write(str(new_doc))
