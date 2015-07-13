import bibtexparser

bib = None
plint_cache = ""


def plint(text=""):
    global plint_cache
    plint_cache += "%s\n" % (text)
    print text


def main():
    global bib

    filepath = "culim.bib"
    bib = bibtexparser.loads(open(filepath).read())

    for entry in bib.entries:
        get_html(entry)


def get_html(entry):

    html = ""
    html = "<div>"

    # Authors
    # -------
    authors = [author.strip() for author in entry["author"].split("and\s")]
    print entry["title"]
    print authors
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
    html += '<span class="title">"%s"</span>' % (entry["title"])

    # - space -
    html += ". "
    # - space -

    # Book-Title
    # -------
    html += '<span class="book-title">In proceedings of %s.</span>' % (entry["booktitle"])


    # Close
    # -----
    html += "</div>"


    plint(html)


if __name__ == "__main__":
    main()
    open("get_publications.html", "w").write(plint_cache)
