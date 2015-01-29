#!/usr/bin/env python

import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import ArrayObject

def main():
    file = sys.argv[1]
    input = PdfFileReader(open(file, 'rb'))
    numPages = input.getNumPages()
    startPage = None; endPage = None
    for numPage in range(numPages):
        page = input.getPage(numPage)
        splitInfoNew = getSplitInfo(page)

        if numPage == 0:
            if splitInfoNew is None:
                sys.stderr.write("First page must have meta info, exiting.\n")
                sys.exit(0)
            splitInfo = splitInfoNew
            splitInfoNew = None
            output = PdfFileWriter()
            startPage = numPage + 1

        if splitInfoNew is not None:
            # Write current pages
            endPage = numPage
            save(output, splitInfo, (startPage, endPage))
            splitInfo = splitInfoNew
            # Begin new file
            output = PdfFileWriter()
            startPage = numPage + 1

        output.addPage(page)

        if numPage == numPages - 1:
            # Write current pages
            endPage = numPage + 1
            save(output, splitInfo, (startPage, endPage))

def save(output, fileName, pages):
    startPage, endPage = pages
    print("Saving pages %d-%d to file %s" % (startPage, endPage, fileName))
    with open(fileName + '.pdf', 'wb') as f:
        output.write(f)

def getSplitInfo(page):
    annotations = page.get('/Annots', [])
    splitInfo = None
    if not isinstance(annotations, list):
        annotations = [ annotations ]
    for annot_ in annotations:
        annot = annot_.getObject()
        # An annotation is contained in an arrayobject
        if isinstance(annot, ArrayObject):
            for a in annot:
                dict = a.getObject()
                if dict.get('/Type') == '/Annot' and dict.get('/Subtype') == '/Text':
                    splitInfo = dict['/Contents']
                    # Remove annotation
                    dict.clear()

    return splitInfo

if __name__ == '__main__':
    main()
