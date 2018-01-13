#!/usr/bin/env python3

#
# (C) Copyrighted rfree 2017, BSD 3-clause Licence.
#
# https://github.com/satoshivision/sopel-factoidfile
#

import os.path
import re
import html
from os import listdir
from os.path import isfile, join


cfg_dir_factoids = '~/sopel-factoidfile/factoids-bitcoins/' # directory with the factoid files

output_fn="/var/www/html/bitcoin-facts/index.html"

def print_dbg(msg):
    print(msg);

print_dbg("Starting");


factoid_dir1 = cfg_dir_factoids + '/'# + factoid_name + '.txt'
factoid_dir  = os.path.expanduser(factoid_dir1)
factoid_files = [ f for f in listdir(factoid_dir)
if (isfile(join(factoid_dir,f)) and bool(re.match('^.*\.txt$',join(factoid_dir,f)))  ) ]
factoid_files.sort()

print_dbg("Files: " + str(factoid_files))

doc = open(output_fn , "w")
doc.write("<html>\n")
doc.write("<head>\n")
doc.write("<title>Factoids list</title>\n")
doc.write(
'''

<style>

.nobr { white-space: nowrap; }

a.fact, a.fact:visited { color: #cc8800; }
a.fact:hover { color: #ff9900; }

a { color: #1144dd; }
a:visited { color: #0000bb; }
a:hover { color: #22aaff; }

</style>

''')
doc.write("</head>\n")
doc.write("\n\n<body>\n\n")
doc.write("<p>Factoids list</p>")

doc.write('<table border="1" cellpadding="4">\n\n')
for factoid_n in factoid_files:
    factoid_fn = join(factoid_dir , factoid_n)
    with open(factoid_fn, 'r') as myfile:
        factoid_text=myfile.read().replace('\n',' ').replace('\r',' ')
    factoid_text = re.sub('[ ]+',' ',factoid_text); # normalize whitespace
    factoid_text = factoid_text.strip()

    title = re.sub( r'^(.*)\.txt$' , r'\1' , factoid_n)
    text_raw = factoid_text
    text_html = html.escape(text_raw)
    text_html = re.sub(r"(http[s]?://[a-zA-Z0-9_/.#-]*)", r'<a href="\1">\1</a>', text_html)
    text_html = re.sub(r'`([a-zA-Z0-9_-]+)', r'<a class="fact" href="#\1">`\1</a>', text_html)

    doc.write("<tr>\n")

    doc.write("<td id='" + html.escape(title) + "'>\n")
    doc.write( "<code class='nobr'>`" + html.escape(title) + "</code>\n" )
    doc.write("</td>\n")

    doc.write("<td>\n")
    doc.write( "<code>" + text_html + "</code>" + "\n")
    doc.write("</td>\n")

    doc.write("</tr>\n\n")

doc.write("</table>")

doc.write("</body>")


