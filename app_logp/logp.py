#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-04
# @Author  : ${author} (${email})
# @Link    : ${link}
# @Version : $Id$

import sys,os,re
from bs4 import BeautifulSoup as bs

def _usage():
  print '''
  python logWrap.py [logDir]
  '''

class Cube(object):
  '''pattern object'''
  def __init__(self, pattern, attrs_dict={}):
    self.pattern = pattern
    self.attrs_dict = attrs_dict

    self.ins_list = []
    self.txt_str = ''

    # whether count occurance: -1:invalide >0:count it
    self.attr_count = -1
    self.count = 0
    # whether subcount occurance: -1:invalide >0:count it
    self.attr_subcount = -1
    self.subcount_dict = {}
    # whether get topline: -1:invalide 0:stop >0:ongoing get
    self.attr_top = -1
    self.top_left = 0

    if 'count' in self.attrs_dict:
        self.attr_count = self.attrs_dict['count']
    if 'subcount' in self.attrs_dict:
        self.attr_subcount = self.attrs_dict['subcount']
    if 'top' in self.attrs_dict:
        self.attr_top = int(self.attrs_dict['top'])

  def append_list(self,l):
    ''' only 'count' and 'subcount' case use this '''
    if self.attr_count >= 0:
        # only count
        self.count += 1
    if self.attr_subcount >= 0:
        self.count += 1
        # record match
        self.ins_list.append(l)
        if l in self.subcount_dict:
          self.subcount_dict[l] += 1
        else:
          self.subcount_dict[l] = 1

  def accept_str(self,s):
    if self.attr_top > 0:
      self.top_left = self.attr_top
    elif self.attr_top == 0:
      self.top_left = 1 # indicate start or not?

  def is_accept_str(self,s):
    if self.attr_top > 0:
      return self.top_left
    elif self.attr_top == 0: # if 'top' == 0 means until empty line
      if self.top_left and s.strip() != '':
        return True
      else:
        self.top_left = 0 # reset, stop accept
        return False

  def append_str(self,s):
    ''' only 'top' case use this '''
    self.txt_str += s
    if self.attr_top > 0:
      self.top_left -= 1

  def get_pattern(self):
    return self.pattern

  def get_attrs(self):
    return self.attrs_dict

  def get_top_left(self):
	return self.top_left

#  def dump(self):
#    if 'count' in self.attrs_dict:
#      return "---> {0:5} times\n".format(self.count)
#    if 'subcount' in self.attrs_dict:
#      return "".join(["-- {}\n".format(c) for c in Counter(self.ins_list).most_common()])
#    if 'top' in self.attrs_dict:
#      return "---> {}".format(self.txt_str)

class FileProxy(object):
  ''' file parser'''
  def __init__(self, file_key, file, platxml):
    self.file = file
    self.file_key = file_key
    self.platxml = platxml
    self.cube_list = []
    self.get = 0
    self.top_tmp = -1

    '''pick up Cube'''
    with open(self.platxml) as f:
      for child in bs(f.read()).find(file_key).findChildren():
        print "setup cube {0}".format(child.string)
        self.cube_list.append(Cube(str(child.string), child.attrs))
    '''
    FileProxy only doing putting line or match to cube
    '''
    with open(file) as f:
      for line in f:
        for c in self.cube_list:
          if c.is_accept_str(line):
            #print "*append string* {0:20}-->{1:20} :{2}".format(self.file, c.get_pattern(), line)
            c.append_str(line)
          else:
            m = re.search(c.get_pattern(), line)
            if m:
              if 'top' in c.get_attrs():
                c.accept_str(line)
              else:
                #print "*append match* {0:20}-->{1:20} :{2}".format(self.file, c.get_pattern(), line)
                c.append_list(m.groups())

  def report(self):
    for c in self.cube_list:
      c.dump()

def main():
  logDir = os.path.abspath(sys.argv[1])
  if not os.path.isdir(logDir):
    _usage()
    return 1

  for file in os.listdir(logDir):
    filepath = os.path.join(logDir, file)
    if re.search(u'bugreport', file):
      BugReport(filepath).report()
  #    elif re.search(u'kernel', file):
  #      KernelLog(filepath).report()
  #    elif re.search(u'logcat.*main', file):
  #      LogCat(filepath).report()
