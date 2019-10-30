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
