# Given a main article title or full article (string) please generate following formats
# [Main Article]
# * The preprocessed main article
# * The bag of words of article
# * The document frequence of article
# * Split article into chapters of sections if possible
# [Cited Articles]
# * retrieve all the citeded articles in a dict with {"title": titlestring, "abstract": abstractstring}
# * The preprocessed abstracts of cited article
# * The bag of words of abstracts
# * The df of article
# [General]
# * The global Term frequence

import PyPDF2

filename = 'paper.pdf'
pdf = open(filename, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdf)  # create a pdf reader object
print(pdfReader.numPages)  # number of pages
pageObj = pdfReader.getPage(0)  # create a page object
print(pageObj.extractText())  # extract text
pdf.close()