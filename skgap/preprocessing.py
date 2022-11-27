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
# get paper title
try:
    title = reader.getOutlines()[0]['/Title']
except:
    title = reader.getDocumentInfo()['/Title']

# extract text
num_pages = reader.numPages  # number of pages
content_str = ""  # store the full text after adding '\n' for title detection
content = []  # store original content line by line
title_list = []  # store each field's title

for page in range(num_pages):
    obj = reader.getPage(page)  # create a page object
    text = obj.extract_text()
    
    # extract field title (add a '\n' before the number)
    for i, t in enumerate(text):
        if text[i:i+8].lower() == 'abstract':  # get abstract
            content_str += '\n' + t
        elif ord(t) >= 49 and ord(t) <= 57:  # number list
            try: 
                if text[i+1] == ' ' and text[i+2].isupper():
                    content_str += '\n' + t  # title
                elif text[i+1] == '.' and ord(text[i+2]) >= 49 and ord(text[i+2]) <= 57 and text[i+3] == ' ' and text[i+4].isupper():
                    content_str += '\n' + t  # subtitle
            except:
                pass
        else:
            content_str += t
    content = list(filter(None, content_str.split('\n')))  # remove the empty element


print(content)


pdf.close()

# preprocessing
# split out each paragraph
# ...
