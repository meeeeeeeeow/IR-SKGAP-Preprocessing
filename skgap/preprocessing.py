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
import time
import logging

from nltk.stem import PorterStemmer, WordNetLemmatizer
from serpapi import GoogleSearch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path

class Term:
    """Term information"""
    
    def __init__(self):
        """Term model"""
        
        self.tf = 0  # term frequency
        self.position = dict()  # {section idx: times}
        self.cite_pos = dict()  # {citation idx: times}
        
    def add_tf(self):
        """Add term frequency"""
        
        self.tf += 1
        
    def add_pos(self, idx):
        """Store which paragraph of the review paper the term appears in
        
        Args:
            idx (int): paragraph index corresponding to the variable "sections".
        """
        
        if idx not in self.position:
            self.position[idx] = 0
        self.position[idx] += 1
        
    def add_cite_pos(self, idx):
        """Store which citation the term appears in
        
        Args:
            idx (int): citation index corresponding to the variable "citations".
        """
        
        if idx not in self.cite_pos:
            self.cite_pos[idx] = 0
        self.cite_pos[idx] += 1
        
    def get_df(self):
        """Return the document frequency of the term"""
        
        if len(self.position) > 0:
            return len(self.cite_pos) + 1
        else:
            return len(self.cite_pos)
        
    def get_section_tf(self, idx):
        if idx in self.position:
            return self.position[idx]
        else:
            return 0
    
    def get_cite_tf(self, idx):
        if idx in self.cite_pos:
            return self.cite_pos[idx]
        else:
            return 0
        
class Citation:
    """Citation information"""
    
    def __init__(self, title, link, cited_num):
        """Citation model
        
        Args:
            title (string): paper title of citation.
            link (string): citation's web page.
            cited_num (int): number of times this article has been cited.
        """
        
        self.title = title  # paper title
        self.link = link
        self.cited_by = cited_num  # number of times this article has been cited
        self.tokens = []  # all tokens in each article (may be duplicated)
        
    def set_tokens(self, tokens):
        """Store the tokens extracted from each citation's abstract
        
        Args:
            tokens (list): abstract tokens after tokenization and normalization.
        """
        
        self.tokens = tokens
        
def tokenization(ori_text):
    """Return a list of tokens for each section
    
    Args:
        ori_text (string): original content of each section.
    """
    
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
    """Return the term after stemming and lemmatization if the word is not a stopword
       Return None if the word is a stopword
       
    Args:
        word (string): a token.
        stopwords (list): stopword list.
    """
    
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    lem = lemmatizer.lemmatize(word)
    stm = stemmer.stem(lem)
    if stm not in stopwords and lem not in stopwords and word not in stopwords:
        return stm
    else:
        return None
    
def normalization(idx, token_list, stopwords, dictionary, is_review):
    """Return a list of terms for each section (preserve order and repeat words)
    
    Args:
        idx (int): section index or citation index.
        token_list (list): all tokens in each section or citation abstract.
        stopwords (list): stopword list.
        dictionary (dict): dictionary for terms.
        is_review (bool): True: the token_list is from review paper; False: from citation abstract.
    """
    
    new_list = []
    
    for t in token_list:
        if len(t) == 1:  # skip only one letter
            continue
        else:
            w = normalize_process(t, stopwords)
            if w != None:
                new_list.append(w)
                
                # update dictionary
                if t not in dictionary:
                    dictionary[t] = Term()
                dictionary[t].add_tf()
                
                if is_review:
                    dictionary[t].add_pos(idx)
                else:
                    dictionary[t].add_cite_pos(idx)

    return new_list

def parse_abstract(idx, cite, stopwords, dictionary):
    """Extract citation abstract from web page
    
    Args:
        idx (int): citation index corresponding to the variable "citations".
        cite (Citation object): a citation object.
        stopwords (list): stopword list.
        dictionary (dict): dictionary for terms.
    """
    
    link = cite.link
    if link != "":  # if there is an avaliable website
        service_object = Service(binary_path)
        driver = webdriver.Chrome(service=service_object)  # consider of dynamic pages
        driver.get(link)
        time.sleep(3)

        abstract = ""
        try:
            abstract = driver.find_element(By.XPATH, '//*[text()="Abstract"]/following-sibling::*[1]').text
        except:
            pass
        try:
            abstract = driver.find_element(By.XPATH, '//*[text()="abstract"]/following-sibling::*[1]').text
        except:
            pass
        try:
            abstract = driver.find_element(By.XPATH, '//*[text()="ABSTRACT"]/following-sibling::*[1]').text
        except:
            pass
        
        if abstract != "":  # parsing e.g., tokenization, normalization, ...
            tokens = tokenization(abstract)
            cite.set_tokens(normalization(idx, tokens, stopwords, dictionary, False))

        driver.quit()
        
    return cite

def get_citataion(query, key, citations):
    """Return all citations of the review paper
    
    Args:
        query (string): title of review paper.
        key (string): Google scholar API key.
        citations (list): store all citations of the review paper.
    """
    
    # search review paper on Google scholar
    search_params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": key
    }  
    search = GoogleSearch(search_params)
    res = search.get_dict()['organic_results'][0]
    cites_id = res['inline_links']['cited_by']['cites_id']  # cited id, for setting search parameters
    
    # get all citations
    try:
        total = res['inline_links']['cited_by']['total']
    except:
        pass  # no citations
    else:
        cite_params = {
            "engine": "google_scholar",
            "q": query,
            "cites": cites_id,
            "api_key": key
        }
        
        all_cite = []
        res = GoogleSearch(cite_params).get_dict()  # first page
        all_cite += res['organic_results']
        other_pages = res['serpapi_pagination']['other_pages'].keys()
        
        for p in other_pages:  # other pages
            next_page = (int(p) - 1) * 10
            cite_params['start'] = next_page
            all_cite += GoogleSearch(cite_params).get_dict()['organic_results']          
        
        for c in all_cite:
            title = c['title']
            try:
                link = c['link']
            except:  # no link
                link = ""
            try:
                cited_num = c['inline_links']['cited_by']['total']
            except:  # no citations
                cited_num = 0
            
            cite = Citation(title, link, cited_num)  # create a citation object
            citations.append(cite)
        
    return citations

# stopwords list
stopwords = ['me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
                'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
                'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
                'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'don', 'should', 'now', 'also', 'as', 'e-mail', 'et', 'al']

if __name__ == '__main__':
    filename = 'Review of information extraction technologies and applications'
    # filename = 'test'
    pdf = open(f'{filename}.pdf', 'rb')
    reader = PyPDF2.PdfFileReader(pdf, False)  # create a pdf reader object
    
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s %(levelname)-8s] %(message)s',
        datefmt='%Y%m%d %H:%M:%S',
	)
    
    title = filename
    num_pages = reader.numPages  # number of pages
    api_key = '1f0dbcedc450cae96f25b4827e928b936bade3de2e148851ddac25366d461f8d'  # your own api key
    
    content = []  # final text
    content_str = ""  # temp for text
    is_first_abstract = True
    title_cnt = 0
    sections = {}  # {title: section content}
    dictionary = {}  # {term: Term obj}
    citations = []  # [Citation obj]

    # extract text and split out sections
    logging.info("Parsing PDF file ...")
    for page in range(num_pages):
        obj = reader.getPage(page)
        text = obj.extract_text()

        for i, t in enumerate(text):
            # abstract
            if text[i:i+8].lower() == 'abstract' and is_first_abstract:
                content_str = t
                is_first_abstract = False
                
            # introduction
            elif text[i:i+14].lower() == '1 introduction' and title_cnt == 0.0 and not is_first_abstract:  # type_1: 2.1
                content.append(content_str)
                content_str = t
                title_cnt = 1.0
                _type = 1
            elif text[i:i+15].lower() == '1. introduction' and title_cnt == 0.0 and not is_first_abstract:  # type_2: 2.1.
                content.append(content_str)
                content_str = t
                title_cnt = 1.0
                _type = 2
                
            # other paragraph
            elif ord(t) >= 49 and ord(t) <= 57 and not is_first_abstract:
                try:
                    # subtitle
                    if text[i+1] == '.' and float(text[i:i+3]) > title_cnt and text[i-2:i+1] != str(title_cnt) and not text[i-1].isalnum() and text[i-5:i-1].lower() != 'fig.' and text[i-6:i].lower() != 'table' and\
                        ((_type == 1 and ((text[i+3] == ' ' and text[i+4].isupper()) or (text[i+3:i+5] == '  ' and text[i+4].isupper()))) or\
                            (_type == 2 and ((text[i+3:i+5] == '. ' and text[i+5].isupper()) or (text[i+3:i+6] == '.  ' and text[i+6].isupper())))):
                        content.append(content_str)
                        content_str = t
                        title_cnt = float(text[i:i+3])
                    # title
                    elif int(t) - int(title_cnt) == 1 and text[i-2:i+1] != str(title_cnt) and not text[i-1].isalnum() and text[i-5:i-1].lower() != 'fig.' and text[i-6:i].lower() != 'table'  and\
                        ((_type == 1 and ((text[i+1] == ' ' and text[i+2].isupper()) or (text[i+1:i+3] == '  ' and text[i+3].isupper()))) or\
                            (_type == 2 and ((text[i+1:i+3] == '. ' and text[i+3].isupper()) or (text[i+1:i+4] == '.  ' and text[i+4].isupper())))):
                        content.append(content_str)
                        content_str = t
                        title_cnt = float(text[i])
                    else:
                        content_str += t
                except:
                    content_str += t
                
            # reference
            elif page > num_pages/2 and text[i:i+10].lower() == 'references':
                content.append(content_str)
                break
            else:
                content_str += t
        content_str += " "  # separate different pages

    pdf.close() 
    
    # preprocessing
    logging.info("Preprocessing and create dictionary ...")
    for i, sec in enumerate(content):
        # sep the parageaph
        key = ""
        if i == 0:
            key = 'abstract'
        elif i == 1:
            key = 'introduction'
        else:
            key = sec.split('\n')[0]
    
        # normalization and create dictionary
        tokens = tokenization(sec)
        sections[key] = normalization(i, tokens, stopwords, dictionary, True)

    # dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1].tf, reverse=True))  # sort by tf
    
    # process for citations
    logging.info("Crawling citations ...")
    citations = get_citataion(title, api_key, citations)  # search paper in Google scholar
    
    logging.info("Parsing abstracts and update dictionary ...")
    for i, cite in enumerate(citations):  # extract abstracts and get terms
        cite = parse_abstract(i, cite, stopwords, dictionary)
        break
    logging.info("Finish preprocessing!")