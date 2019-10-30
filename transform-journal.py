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

print("Start json transform")

def transform(source_path, target_path, platform):
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
