#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import copy
import os

SOURCE_DIR = "./out"
TARGET_DIR = "./html"

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

def transform_headings(source_path, target_path):
  with open(source_path) as f:
      soup = BeautifulSoup(f, 'html.parser')

  with open("./header.html") as header_html:
    header = BeautifulSoup(header_html, 'html.parser')

  new_doc = BeautifulSoup("<!DOCTYPE html>", 'html.parser')

  html = new_doc.new_tag("html", lang="en")
  body = new_doc.new_tag("body")

  details = None

  for el in soup.children:
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

  # print("new_doc:", new_doc)

  f= open(target_path, "w+")
  f.write(str(new_doc))

print("Starting transform")

def create_dir_if_not_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)

def source_to_target_path(source):
  parts = source.split("/")
  new_parts = [TARGET_DIR] + parts[2:]
  target_path = "/".join(new_parts)
  return target_path

for subdir, dirs, files in os.walk(SOURCE_DIR):

  target_path = source_to_target_path(subdir)
  create_dir_if_not_exists(target_path)

  for file in files:
      source_path = os.path.join(subdir, file)

      _, ext = os.path.splitext(source_path)
      if (ext == ".html"):
        target_path = source_to_target_path(source_path)

        transform_headings(source_path, target_path)

print("Finished transform")
