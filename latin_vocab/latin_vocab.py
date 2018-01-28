
import os
import re
import unicodedata

def remove_accents(input_str):
    '''stolen idk'''
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

def words_similar(a,b):
    '''two latin words are prolly the same if the first two thirds is the same'''
    h = int(float(max(len(a),len(b)))*.666666)
    return (a[:h].lower() == b[:h].lower())

def remove_caps_comma_list(l):
    '''a list of words may have repeats differing only by capitals, delete duplicates'''
    r, rr = [], []
    for s in l:
        if s.lower() not in r:
            r.append(s)
    r.reverse()
    for s in r:
        if s.lower() not in rr:
            rr.append(s)
    rr.reverse()
    return rr

psalm_dir = 'psalms'
files = os.listdir(psalm_dir)
pattern = re.compile(r"\W", re.UNICODE)
all_words = {}
for n in files:
    f = open(os.path.join(psalm_dir, n))
    for x in pattern.split(remove_accents(f.read().decode('utf-8-sig'))):
        if len(x) < 1:
            pass
        elif x in all_words:
            all_words[x] += 1
        else:
            all_words[x] = 1
    f.close()

alpha_list = sorted(all_words.keys(), key=lambda s: s.lower())

combined_words = {}
combined, num = [], 0
for i in range(len(alpha_list)):
    if (i == 0) or words_similar(alpha_list[i], alpha_list[i-1]):
        pass
    else:
        combined_words[','.join(remove_caps_comma_list(combined))] = num
        combined, num = [], 0

    combined.append(alpha_list[i])
    num += all_words[alpha_list[i]]
if len(combined) > 0:
    combined_words[','.join(remove_caps_comma_list(combined))] = num

ranked = sorted(combined_words.items(), key=lambda e: e[1], reverse=True)

mdfile = open('readme.md','w')
mdfile.write("""
# Latin vocab from the psalter

In an attempt to start to study liturgucal Latin, I had a crazy idea that I should just use the text of the psalms to figure out which words need to be learned.

This program analyses text from the Psalter as provided by the [jgabc](http://github.com/bbloomf/jgabc) project.  Words are ranked by occurence so that you know which vocab to learn.  It attempts to combine conjugations of the same word.

This readme is the output of the program:

num occ | Word(s)
--------|--------
""")

for word, num in ranked:
    mdfile.write("%-7i | %s\n" % (num, word.replace(',',', ')))
mdfile.close()
