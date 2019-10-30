#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import copy
import os
import shutil
import utils
import json
import sys

print("Start json transform")

def transform(source_path, target_path, platform):
  with open(source_path) as f:
    data = json.load(f)

  new_doc = BeautifulSoup("<!DOCTYPE html>", 'html.parser')

  html = new_doc.new_tag("html", lang="en")
  body = new_doc.new_tag("body")

  # Title
  title = new_doc.new_tag("h1", **{'class':'title'})
  title.string = data["Title"]
  body.append(title)

  # Journal
  journal = new_doc.new_tag("p", **{'class':'journal'})
  journal.string = data["JournalAbbrev"] + " " + data["Year"]
  body.append(journal)

  # Abstract
  link_container = new_doc.new_tag("p")
  link = new_doc.new_tag("a", href=data["Link"], **{'class':'journal-link'})
  link.string = data["Link"]
  link_container.append(link)
  body.append(link_container)


  # Abstract
  abstract_title = new_doc.new_tag("h3", **{'class':'abstract-title'})
  abstract_title.string = "Abstract"
  body.append(abstract_title)

  for p in data["Abstract"]:
    abstract = new_doc.new_tag("p", **{'class':'abstract'})
    abstract.string = p
    body.append(abstract)

  # Notes
  notes_title = new_doc.new_tag("h3", **{'class':'notes-title'})
  notes_title.string = "Notes"
  body.append(notes_title)

  if ("Notes" in data):
    for p in data["Notes"]:
      note = new_doc.new_tag("p", **{'class':'note'})
      note.string = p
      body.append(note)


  header = utils.get_header(platform)

  html.append(header)
  html.append(body)
  new_doc.append(html)

  # Write to disk
  f= open(target_path, "w+")
  f.write(str(new_doc))

PLATFORM = utils.get_platform(sys.argv)
SOURCE_DIR = "./middle"
TARGET_DIR = utils.get_target_dir(PLATFORM)

# Transform
for subdir, dirs, files in os.walk(SOURCE_DIR):

  target_path = utils.source_to_target_path(subdir, TARGET_DIR)
  utils.create_dir_if_not_exists(target_path)

  for file in files:
      source_path = os.path.join(subdir, file)

      _, ext = os.path.splitext(source_path)
      target_path = utils.source_to_target_path(source_path, TARGET_DIR)
      if (ext == ".json"):
        new_path = utils.change_ext(target_path, 'html')
        print "JSON"
        transform(source_path, new_path, PLATFORM)
      else:
        shutil.copy2(source_path, target_path)


print("Finish json transform")
