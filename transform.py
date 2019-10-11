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

print 'Args:', str(sys.argv)

def get_target_platform():
  if len(sys.argv) == 1:
    return 'ios'
  if (sys.argv[1] == 'web'):
    return 'web'
  else:
    return 'ios'

platform = get_target_platform()
print 'Platform:', platform

def get_header():
  if platform == 'web':
    with open("./header-web.html") as header_html:
      header = BeautifulSoup(header_html, 'html.parser')
      return header
  else:
    with open("./header-ios.html") as header_html:
      header = BeautifulSoup(header_html, 'html.parser')
      return header

def get_target_dir():
  if platform == 'web':
    return './out-web'
  else:
    return './out-ios'


def get_script():
  with open("./script.html") as script_html:
    script = BeautifulSoup(script_html, 'html.parser')
    return script

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

  statbuf = os.stat(source_path)
  last_modified = statbuf.st_mtime
  print("Modification time: {}".format(statbuf.st_mtime))

  raw = datetime.fromtimestamp(last_modified, tz= pytz.timezone('Australia/Sydney'))
  formatted = raw.strftime('%d/%m/%Y')

  new_doc = BeautifulSoup("<!DOCTYPE html>", 'html.parser')

  html = new_doc.new_tag("html", lang="en")
  body = new_doc.new_tag("body")

  header = get_header()

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
          date_container = new_doc.new_tag("div")
          print("last_modified:", formatted)
          date_container.string = str(formatted)
          body.append(date_container)
        else:
          body.append(el_copy)


      else:
        details.append(el_copy)

  script = get_script()
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


def create_dir_if_not_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)

def source_to_target_path(source):
  parts = source.split("/")
  new_parts = [TARGET_DIR] + parts[2:]
  target_path = "/".join(new_parts)
  return target_path

print("Start transform")

SOURCE_DIR = "./middle"
TARGET_DIR = get_target_dir()

# Transform
for subdir, dirs, files in os.walk(SOURCE_DIR):

  target_path = source_to_target_path(subdir)
  create_dir_if_not_exists(target_path)

  for file in files:
      source_path = os.path.join(subdir, file)

      _, ext = os.path.splitext(source_path)
      target_path = source_to_target_path(source_path)
      if (ext == ".html"):
        transform_headings(source_path, target_path)
      else:
        shutil.copy2(source_path, target_path)


print("Finish transform")
