#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import copy
import os
import shutil
import sys
import re
from datetime import datetime
import pytz
import utils

# print 'Args:', str(sys.argv)
print 'Platform:', utils.get_platform(sys.argv)

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

def transform_headings(source_path, target_path, platform):
  # print 'Platform:', platform

  with open(source_path) as f:
    soup = BeautifulSoup(f, 'html.parser')

  statbuf = os.stat(source_path)
  last_modified = statbuf.st_mtime
  # print("Modification time: {}".format(statbuf.st_mtime))

  raw = datetime.fromtimestamp(last_modified, tz= pytz.timezone('Australia/Sydney'))
  formatted = raw.strftime('%d %B %Y, %-I:%M:%S %p %Z')

  new_doc = BeautifulSoup("<!DOCTYPE html>", 'html.parser')

  html = new_doc.new_tag("html", lang="en")
  body = new_doc.new_tag("body")

  header = utils.get_header(platform)

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
        # the TITLE
        if (el.name == "h1"):
          # create container
          container = new_doc.new_tag("div", **{'class':'title-container'})

          # then add (as 1st child) title h1
          container.append(el_copy)

          # then add (as 2nd child) the #toggle
          toggle = new_doc.new_tag("div", id="toggle", **{'class':'collapsed'})
          container.append(toggle)

          # add completed container to body
          body.append(container)

          # last_modified timestamp
          date_container = new_doc.new_tag("div", id="last-modified", **{'class':'last-modified'})
          # print("formatted time:", formatted)
          date_container.string = 'Last modified: ' + str(formatted)
          body.append(date_container)
        else:
          body.append(el_copy)


      else:
        details.append(el_copy)

  script = utils.get_script()
  body.append(script)

  html.append(header)
  html.append(body)
  new_doc.append(html)

  # Create "Pills"
  pills = new_doc.find_all("span", class_="pill")
  pill_count = len(pills)

  for index, pill in enumerate(new_doc.find_all("span", class_="pill")):
    pill_text = str(index + 1) + " / " + str(pill_count)
    pill.string = pill_text

  # print("new_doc:", new_doc)

  # Create <a> tags for all urls
  RE_URL = re.compile(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')

  for tag in new_doc.find_all(text=True):
      tags = []
      url = False

      for t in RE_URL.split(tag.string):
          if RE_URL.match(t):
              a = new_doc.new_tag("a", href=t, target='_blank')
              a.string = t
              tags.append(a)
              url = True
          else:
              tags.append(t)

      if url:
          for t in tags:
              tag.insert_before(t)
          tag.extract()

  # Write to disk
  f= open(target_path, "w+")
  f.write(str(new_doc))



print("Start transform")

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
      if (ext == ".html"):
        transform_headings(source_path, target_path, PLATFORM)
      else:
        shutil.copy2(source_path, target_path)


print("Finish transform")
