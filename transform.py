#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import copy
import os
import shutil
import sys

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
        else:
          body.append(el_copy)


      else:
        details.append(el_copy)

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
