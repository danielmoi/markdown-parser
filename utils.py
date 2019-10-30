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
