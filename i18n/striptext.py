# coding=utf-8

import os
import csv
import hashlib



bracketList = ['•', '&nbsp;', '\%\s', '@CARRIERHANDLE', '@carrierhandle', '@mycoverageapp', '\\n', '\\r', '&#160;', '&lt;', '&gt;']

languages = []
originals = []

for dirname, dirnames, filenames in os.walk('languages'):
  for subdirname in dirnames:
    languages.append(subdirname)

for dirname, dirnames, filenames in os.walk('originals'):
  for filename in filenames:
    originals.append(filename)

print languages
print originals

count = 0
specialWord = list("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX") #<!-- TRANSLATE_IGNORE_STA -->
specialLength = len(specialWord)

def getHash(text):
  return hashlib.sha224(text).hexdigest()

def bracketExtras(text):
  result = text
  for extra in bracketList:
    result = result.replace(extra, "[[[" + extra + "]]]")
  return result

def addToSpecial(c):
  for i in range(specialLength - 1):
    specialWord[i] = specialWord[i + 1]

  specialWord[specialLength - 1] = c

  sw = ''.join(specialWord)
  if sw == "<!-- TRANSLATE_IGNORE_STA -->":
    return 1
  elif sw == "<!-- TRANSLATE_IGNORE_END -->":
    return 2
  return 0

def stripText(fileName):
  global count
  f = open(os.path.join("originals", fileName), "r")
  html = f.read()
  f.close()

  state = 0
  tag = ""
  text = ""

  start = 0
  end = 0
  i = 0
  ignoring = False
  replaces = []
  for c in html:
    special = addToSpecial(c)

    if ignoring:
      if special == 2:
        ignoring = False
        print "STOPPED IGNORING"
    elif special == 1:
      ignoring = True
      print "IGNORING NOW"

    if state == 0:
      if c == "<":
        if len(text.strip()) > 2:
          text = text.strip()
          end = i
          replace = (start, end, getHash(text), text)
          if not ignoring:
            replaces.append(replace)
          count = count + 1
          text = ""
        else:
          text = ""
        state = 1
        tag = ""
      else:
        if len(text) == 0:
          start = i
        text += c
    elif state == 1:
      if c == " " or c == "\t":
        state = 2
      elif c == ">":
        state = 3
      else:
        tag = tag + c
    elif state == 2:
      if c == ">":
        state = 3
    elif state == 3:
      # tag complete
      if c == "<":
        state = 1
        tag = ""
      else:
        state = 0
        if len(text) == 0:
          start = i
        text = text + c
    i = i + 1

  replaces = replaces[::-1]

  for replace in replaces:
    s = replace[0]
    e = replace[1]
    it = str(replace[2])
    t = bracketExtras(replace[3])
    d = "<!--TRANS_TEXT~"+it+"~-->"
    html = html[:s] + d + html[e:]
    f = open("languages/en/" + it + ".txt", "w+")
    f.write(t);
    f.close()

  f = open(os.path.join("templates", fileName), "w+")
  f.write(html)
  f.close()

for fileName in originals:
  stripText(fileName)

# convert the language files into a CSV (english only!)

basepath = os.path.join('languages', 'en')
#csv.register_dialect("transtext", delimiter='`', quotechar=None, quoting=csv.QUOTE_NONE)
csvWriter = csv.writer(open(os.path.join('languages', 'en.csv'), 'wb'))

#csvWriter.writerow(["key", "text"])
for dirname, dirnames, filenames in os.walk(basepath):
  for filename in filenames:
    if filename[0] == '.':
      continue
    bn = os.path.basename(filename)
    key = "[[[" + os.path.splitext(bn)[0] + "]]]"
    f = open(os.path.join(basepath, filename))
    data = f.read()
    f.close()
    csvWriter.writerow([key, data])
