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

# read review paper and extract the text
filename = 'paper'
pdf = open(f'{filename}.pdf', 'rb')
reader = PyPDF2.PdfFileReader(pdf, False)  # create a pdf reader object

# extract pdf content
# get title
try:
    title = reader.getOutlines()[0]['/Title']
except:
    title = reader.getDocumentInfo()['/Title']

# extract text
num_pages = reader.numPages  # number of pages
content = []  # store original content line by line
for page in range(num_pages):
    obj = reader.getPage(page)  # create a page object
    line = obj.extractText().split('\n')  # extract text
    content += line
pdf.close()

# preprocessing
# split out each paragraph
# ...
