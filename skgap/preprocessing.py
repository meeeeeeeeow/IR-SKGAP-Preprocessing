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
# try:
#     title = reader.getOutlines()[0]['/Title']
# except:
#     title = reader.getDocumentInfo()['/Title']

# extract text
num_pages = reader.numPages  # number of pages
content_str = ""  # store the full text after adding '\n' for title detection
content = []  # store original content paragraph by paragraph
is_first_abstract = True
title_cnt = 0.0

for page in range(num_pages):
    obj = reader.getPage(page)  # create a page object
    text = obj.extract_text()
    
    # extract field title (add a '\n' before the number)
    for i, t in enumerate(text):
        # abstract
        if text[i:i+8].lower() == 'abstract' and is_first_abstract:  # get abstract
            content_str = '\n' + t
            is_first_abstract = False
            
        # introduction
        elif text[i:i+14].lower() == '1 introduction' and title_cnt == 0.0:  # type_1: 2.1
            content.append(content_str)
            content_str = t
            title_cnt = 1.0
            print(text[i:i+10])
            _type = 1
        elif text[i:i+15].lower() == '1. introduction' and title_cnt == 0.0:  # type_2: 2.1.
            content.append(content_str)
            content_str = t
            title_cnt = 1.0
            print(text[i:i+10])
            _type = 2
            
        # other paragraph
        elif ord(t) >= 49 and ord(t) <= 57 and not is_first_abstract:  # number list
            try:
                # subtitle
                if text[i+1] == '.' and float(text[i:i+3]) > title_cnt and text[i-2:i+1] != str(title_cnt) and not text[i-1].isalnum() and text[i-5:i-1].lower() != 'fig.' and text[i-6:i].lower() != 'table' and\
                    ((_type == 1 and ((text[i+3] == ' ' and text[i+4].isupper()) or (text[i+3:i+5] == '  ' and text[i+4].isupper()))) or\
                        (_type == 2 and ((text[i+3:i+5] == '. ' and text[i+5].isupper()) or (text[i+3:i+6] == '.  ' and text[i+6].isupper())))):
                    content.append(content_str)
                    content_str = t
                    title_cnt = float(text[i:i+3])
                    print(text[i:i+10])
                # title
                elif int(t) - int(title_cnt) == 1 and text[i-2:i+1] != str(title_cnt) and not text[i-1].isalnum() and text[i-5:i-1].lower() != 'fig.' and text[i-6:i].lower() != 'table'  and\
                    ((_type == 1 and ((text[i+1] == ' ' and text[i+2].isupper()) or (text[i+1:i+3] == '  ' and text[i+3].isupper()))) or\
                        (_type == 2 and ((text[i+1:i+3] == '. ' and text[i+3].isupper()) or (text[i+1:i+4] == '.  ' and text[i+4].isupper())))):
                    content.append(content_str)
                    content_str = t
                    title_cnt = float(text[i])
                    print(text[i:i+10])
            except:
                pass
        else:
            content_str += t
            
    content.append(content_str)

# print(len(content)) 錯的

# split out each paragraph
paragraph = {}  # {title: content}
title_cnt = 0




pdf.close()
