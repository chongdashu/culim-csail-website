#!/usr/bin/python

print "Content-type: text/html"
# print "Access-Control-Allow-Origin: *"
print ""

import bibtexparser
import os
import re

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
    output_html(bib.entries, "article")
    output_html(bib.entries, "inproceedings")
    output_html(bib.entries, "workshop")
    output_html(bib.entries, "conference")
    


def publication_type_to_name(publication_type):
    if publication_type == "inproceedings":
        return "Proceedings of Refereed Conferences"
    elif publication_type == "article":
        return "Refereed Journal Articles"
    elif publication_type == "conference":
        return "Juried Exhibitions &amp; Demonstrations"
    elif publication_type == "workshop":
        return "Refereed Workshop Papers"
    else:
        return publication_type


def isEntryOfType(entry, publication_type):
    if publication_type == "workshop":
        return entry["type"] == "inproceedings" and entry["booktitle"].lower().find("workshop") >= 0
    if publication_type == "inproceedings":
        return (entry["type"] == "inproceedings") and (not entry.get("booktitle") or (entry["booktitle"].lower().find("workshop") < 0))

    return entry["type"] == publication_type


def output_html(entries, publication_type):

    plint("<h2>%s</h2>" % (publication_type_to_name(publication_type)))
    plint("<ol>")

    entries = [entry for entry in entries if isEntryOfType(entry, publication_type)]
    entries = sorted(entries, key=lambda x: 12*int(x["year"]) + (int(x.get("month")) if x.get("month") else 0))
    entries = entries[::-1]
    for entry in entries:
        get_html(entry)
    plint("</ol>")


def get_html(entry):

    html = ""
    html = "<li>"

    # Authors
    # -------
    authors = [author.strip() for author in entry["author"].split(" and")]
    authors = map(lambda x: x.split(",")[1].strip() + " " + x.split(",")[0].strip(), authors)

    author = "<u>" + authors[0] + "</u>" if authors[0] == "Chong-U Lim" else authors[0]
    html += '<span class="author">%s</span>' % (author)
    for i in range(1, len(authors)):
        sep = ", "
        if i == len(authors)-1:
            sep = ", and " if len(authors) > 2 else " and "
        author = "<u>" + authors[i] + "</u>" if authors[i] == "Chong-U Lim" else authors[i]
        html += sep + '<span class="author">%s</span>' % (author)

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
        html += '<span class="title">"%s."</span>' % (entry["title"])
    else:
        html += '<span class="title"><a href="%s">"%s</a>."</span>' % (href, entry["title"])

    # - space -
    html += " "
    # - space -

    # Book-Title
    # -------
    journal = "journal" if entry["type"] == "article" else "booktitle"
    html += '<span class="book-title">In <i>%s</i></span>' % (entry[journal])

    # - space -
    html += ". "
    # - space -

    # Date
    # ----

    # Address
    # -------
    address = entry.get("location")
    if not address:
        address = entry.get("address")
    if address:
        html += '<span class="location">%s</span>' % (address)

    # - space -
    html += ". "
    # - space -    

    pages = entry.get("pages")
    if not pages:
        pages = entry.get("pagetotal")
    if pages:
        if pages.find("-") >= 0:
            pages = pages.replace("--", "-")
            html += '<span class="pages">p. %s.</span>' % (pages)
        else:
            html += '<span class="pages">%s pp.</span>' % (pages)

    # - space -
    html += ""
    # - space -    



    # Close
    # -----
    html += "</li>"

    plint(html)


if __name__ == "__main__":
    main()
    open("publications.html", "w").write(plint_cache)
