#!/usr/bin/python

print "Content-type: text/html"
# print "Access-Control-Allow-Origin: *"
print ""

import bibtexparser
import os

bib = None
plint_cache = ""
entries = []


def plint(text=""):
    global plint_cache
    plint_cache += "%s\n" % (text)
    print text


def main():
    global bib
    global entries

    filepath = "culim.bib"
    bib = bibtexparser.loads(open(filepath).read())

    plint("<ul>")

    entries = bib.entries[:]
    entries = sorted(entries, key=lambda x: -int(x["year"]))
    for entry in entries:
        get_html(entry)
    plint("</ol>")


def get_html(entry):

    html = ""
    html = "<li>"

    # Authors
    # -------
    authors = [author.strip() for author in entry["author"].split("and\s")]
    authors = map(lambda x: x.split(",")[1].strip() + " " + x.split(",")[0].strip(), authors)

    html += '<span class="author">%s</span>' % (authors[0])
    for i in range(1, len(authors)):
        sep = ", "
        if i == len(authors)-1:
            sep = ", and " if len(authors) > 2 else " and "
        html += sep + '<span class="author">%s</span>' % (authors[i])

    # - space -
    html += ". "
    # - space -

    # Year
    # -------
    html += '<span class="year">(%s)</span>' % (entry["year"])

    # - space -
    html += ". "
    # - space -

    # Title
    # -------
    key = entry["id"]
    href = "#" if not os.path.isfile("../%s.pdf" % (key)) else "%s.pdf" % (key)
    if href == "#":
        html += '<span class="title">"%s"</span>' % (entry["title"])
    else:
        html += '<span class="title"><a href="../%s">"%s"</a></span>' % (href, entry["title"])

    # - space -
    html += ". "
    # - space -

    # Book-Title
    # -------
    html += '<span class="book-title">In <i>%s</i>.</span>' % (entry["booktitle"])

    # Close
    # -----
    html += "</li>"

    plint(html)


if __name__ == "__main__":
    main()
    open("publications.html", "w").write(plint_cache)
