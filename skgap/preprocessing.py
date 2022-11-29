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
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re

# split out each section
def split_out_sec(num_pages, sections, sec):
    
    # ignore header and footer
    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        all_parts.append([y, text])

    num = 0  # store the section number
    for page in range(num_pages):
        
        final_parts = []  # store the processed text
        check_parts = []
        all_parts = []

        obj = reader.getPage(1)  # create a page object
        obj.extract_text(visitor_text=visitor_body)  # get all text of the page
        
        for part in all_parts:
            if part[0] == 0.0:
                if len(check_parts) > len(final_parts):
                    final_parts = check_parts
                check_parts = []
            else:
                check_parts.append(part[1])
        
        text = "".join(final_parts).split('\n')
        
        for line in text:
            if page > num_pages/2 and line[:10].lower() == "references":  # end (store ref using Google scholar, not file)
                return sections
            elif line[:8].lower() == "abstract":
                num = 1
                sec = "abstract"
                sections[sec] = [line[8:]]
            # elif num == 1 and ("1 introduction" in line.lower() or "1. introdiction" in line.lower()):
            #     num = 1
            #     sec = "abstract"
            #     sections[sec] = [line[8:]]
            elif re.match(r"[0-9][\.0-9]*\.?\ ", line):
                # idx_list = list(filter(None, line.split(' ')[0].split('.')))
                # idx_list = idx_list + ['0'] * (2 - len(idx_list))
                # idx = float(idx_list[0] + '.' + idx_list[1])
                # if int(idx) - int(num) in [0, 1]:
                #     num = idx
                # else:
                #     continue
                
                if "summary" in line.lower():
                    idx = line.lower().find("summary")
                    sec = "summary"
                    sections[sec] = [line[idx+len(sec):]]
                else:
                    sec = line
                    sections[sec] = []
            elif num != 0:
                sections[sec].append(line)

if __name__ == '__main__':
    filename = 'Review of information extraction technologies and applications'
    # filename = 'test'
    pdf = open(f'{filename}.pdf', 'rb')
    reader = PyPDF2.PdfFileReader(pdf, False)  # create a pdf reader object

    # extract pdf content
    # title = reader.getOutlines()[0]['/Title']
    # title = reader.getDocumentInfo()['/Title']
    title = filename
    num_pages = reader.numPages  # number of pages
    
    sections = {}  # store original content paragraph by paragraph
    sec = "title"
    sections[sec] = [title]
    sections = split_out_sec(num_pages, sections, sec)
    
    cnt = 0       
    for k in sections.keys():
        cnt += 1
        print(k)
    print(cnt)
    
    raise SystemExit

        # for i, t in enumerate(text):
        #     # abstract
        #     if text[i:i+8].lower() == 'abstract' and is_first_abstract:
        #         content_str = t
        #         is_first_abstract = False
                
        #     # introduction
        #     elif text[i:i+14].lower() == '1 introduction' and title_cnt == 0.0 and not is_first_abstract:  # type_1: 2.1
        #         content.append(content_str)
        #         content_str = t
        #         title_cnt = 1.0
        #         _type = 1
        #     elif text[i:i+15].lower() == '1. introduction' and title_cnt == 0.0 and not is_first_abstract:  # type_2: 2.1.
        #         content.append(content_str)
        #         content_str = t
        #         title_cnt = 1.0
        #         _type = 2
                
        #     # other paragraph
        #     elif ord(t) >= 49 and ord(t) <= 57 and not is_first_abstract:
        #         try:
        #             # subtitle
        #             if text[i+1] == '.' and float(text[i:i+3]) > title_cnt and text[i-2:i+1] != str(title_cnt) and not text[i-1].isalnum() and text[i-5:i-1].lower() != 'fig.' and text[i-6:i].lower() != 'table' and\
        #                 ((_type == 1 and ((text[i+3] == ' ' and text[i+4].isupper()) or (text[i+3:i+5] == '  ' and text[i+4].isupper()))) or\
        #                     (_type == 2 and ((text[i+3:i+5] == '. ' and text[i+5].isupper()) or (text[i+3:i+6] == '.  ' and text[i+6].isupper())))):
        #                 content.append(content_str)
        #                 content_str = t
        #                 title_cnt = float(text[i:i+3])
        #             # title
        #             elif int(t) - int(title_cnt) == 1 and text[i-2:i+1] != str(title_cnt) and not text[i-1].isalnum() and text[i-5:i-1].lower() != 'fig.' and text[i-6:i].lower() != 'table'  and\
        #                 ((_type == 1 and ((text[i+1] == ' ' and text[i+2].isupper()) or (text[i+1:i+3] == '  ' and text[i+3].isupper()))) or\
        #                     (_type == 2 and ((text[i+1:i+3] == '. ' and text[i+3].isupper()) or (text[i+1:i+4] == '.  ' and text[i+4].isupper())))):
        #                 content.append(content_str)
        #                 content_str = t
        #                 title_cnt = float(text[i])
        #             else:
        #                 content_str += t
        #         except:
        #             content_str += t
                
        #     # reference
        #     elif page > num_pages/2 and text[i:i+10].lower() == 'references':
        #         content.append(content_str)
        #         break
        #     else:
        #         content_str += t
        # content_str += " "  # separate different pages

    pdf.close()

    # basic preprocessing
    def tokenization(ori_text):
        new_text = ""
        is_parentheses = False
        ori_text = ori_text.lower()  # lowercasting
        
        for i, t in enumerate(ori_text):
            if is_parentheses:
                is_parentheses = False
            elif t == '(':  # skip the words in the ()
                is_parentheses = True
            elif not t.isalpha():  # remove numbers and marks (didn't consider dash)
                new_text += " "
            else:
                new_text += t
        
        return list(filter(None, new_text.split(' ')))
        
    def normalize_process(word, stopwords):
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        
        lem = lemmatizer.lemmatize(word)
        stm = stemmer.stem(lem)
        if stm not in stopwords and lem not in stopwords and word not in stopwords:
            return stm
        else:
            return None
        
    def normalization(token_list, stopwords):
        new_list = []
        
        for t in token_list:
            if len(t) == 1:  # skip only one letter
                continue
            else:
                w = normalize_process(t, stopwords)
                if w != None:
                    new_list.append(w)
                    
        # 處理重複的字
        # 直接一起做 dictionary

        return new_list
        
    # main
    stopwords = ['me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
                'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
                'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'don', 'should', 'now', 'also', 'as', 'e-mail', 'et', 'al']

    for sec in content:
        tokens = tokenization(sec)
        terms = normalization(tokens, stopwords)
        # print(terms)
        
        # 要先做成 set 還是先每個段落都處理?
        # 目前想的是
            # 一list存原本所有字
            # 一set存所有term(dictionary)
            # 一??存所有df跟他出現在哪個文章(應該跟dict一起)
        

    '''
    Note
    1. 沒有考慮 dash
    2. 頁首或頁尾會印有出版書刊, 日期, doi 等，還沒刪掉
    3. 每篇 paper 格式都不同，PyPDF2 爬到的東西只有純文字，chapter number 都是用 naive 的 rule 去寫，無法 cover 到所有 paper
    4. 呈上，有 pretrained model (見上) 可用，但跑不起來 (連不到 server)
    5. 呈上上，目前的規則是觀察 IR paper 都會有 title number，如果沒有就抓不到 -> 可能要直接爬網頁比較有機會
    6. 呈上上上，title 亦然，每篇 paper 存 title 的方法都不一樣
    '''