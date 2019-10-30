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

def get_header(platform):
  if platform == 'web':
    with open("./header-web.html") as header_html:
      header = BeautifulSoup(header_html, 'html.parser')
      return header
  else:
    with open("./header-ios.html") as header_html:
      header = BeautifulSoup(header_html, 'html.parser')
      return header

def get_platform(sys_args):
  if len(sys_args) == 1:
    return 'ios'
  if (sys_args[1] == 'web'):
    return 'web'
  else:
    return 'ios'

def get_target_dir(platform):
  if platform == 'web':
    return './out-web'
  else:
    return './out-ios'

def get_script():
  with open("./script.html") as script_html:
    script = BeautifulSoup(script_html, 'html.parser')
    return script

def create_dir_if_not_exists(path):
  if not os.path.exists(path):
    os.makedirs(path)

def source_to_target_path(source, target_dir):
  parts = source.split("/")
  new_parts = [target_dir] + parts[2:]
  target_path = "/".join(new_parts)
  return target_path

def change_ext(path, new_ext):
  parts = path.split("/")
  file_name = parts[len(parts) - 1]
  file_name_parts = file_name.split(".")
  new_file_name = file_name_parts[0] + "." + new_ext
  start = parts[0:len(parts) - 1]
  new_parts = start + [new_file_name]
  new_path = "/".join(new_parts)
  return new_path
