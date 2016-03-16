# coding=utf-8

import os
import csv

#csv.register_dialect("transtext", delimiter='`', quotechar=None, quoting=csv.QUOTE_NONE)

# convers CSVs back into files
def handleLang(lang):
  csvReader = csv.reader(open(os.path.join('languages', lang + '.csv'), 'rb'))

  c = 0
  for row in csvReader:
    c = c + 1

    fn = row[0].replace("[[[", "")
    fn = fn.replace("]]]", "") + '.txt'
    f = open(os.path.join('languages', lang, fn), "w+")
    f.write(row[1])
    f.close()

for dirname, dirnames, filenames in os.walk('languages'):
  for subdirname in dirnames:
    handleLang(subdirname)

# handle the language files

languages = []
templates = []

for dirname, dirnames, filenames in os.walk('languages'):
  for subdirname in dirnames:
    languages.append(subdirname)

for dirname, dirnames, filenames in os.walk('originals'):
  for filename in filenames:
    templates.append(filename)

for template in templates:
  f = open(os.path.join("templates", template), "r")
  data = f.read()
  f.close()

  ids = []
  idt = ""
  record = False
  for c in data:
    if c == '~':
      record = ~record
      if ~record:
        ids.append(idt)
        idt = ""
    elif record:
      idt = idt + c

  for lang in languages:
    datalang = data
    for idt in ids:
      try:
        f = open(os.path.join("languages", lang, idt + ".txt"), "r")
        text = f.read().replace("[[[", "").replace("]]]", "")
        f.close()
        datalang = datalang.replace("<!--TRANS_TEXT~"+idt+"~-->", text)
      except:
        print "error on file:", idt

    dir = os.path.join("output", lang)
    if not os.path.exists(dir):
      os.makedirs(dir)
    f = open(os.path.join(dir, template), "w+")
    f.write(datalang)
    f.close()
