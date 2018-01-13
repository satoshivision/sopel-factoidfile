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

span.nobr { white-space: nowrap; }

</style>

''')
doc.write("</head>\n")
doc.write("\n\n<body>\n\n")
doc.write("<p>Factoids list</p>")

doc.write('<table border="1">\n\n')
for factoid_n in factoid_files:
    factoid_fn = join(factoid_dir , factoid_n)
    with open(factoid_fn, 'r') as myfile:
        factoid_text=myfile.read().replace('\n',' ').replace('\r',' ')
    factoid_text = re.sub('[ ]+',' ',factoid_text); # normalize whitespace
    factoid_text = factoid_text.strip()

    title = re.sub( r'^(.*)\.txt$' , r'\1' , factoid_n)
    text_raw = factoid_text
    text_html = html.escape(text_raw)
    text_html = re.sub(r"(http[s]?://[^ \(\)\[\]]*)", r'<a href="\1">\1</a>', text_html)
    text_html = re.sub(r'`([^ \(\)\[\]]+)', r'<a href="#\1">`\1</a>', text_html)

    doc.write("<tr>\n")

    doc.write("<td id='" + html.escape(title) + "'>\n")
    doc.write( "<span class='nobr'>`" + html.escape(title) + "</span>\n" )
    doc.write("</td>\n")

    doc.write("<td>\n")
    doc.write( text_html + "\n")
    doc.write("</td>\n")

    doc.write("</tr>\n\n")

doc.write("</table>")

doc.write("</body>")


