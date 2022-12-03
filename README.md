# SKGAP
Sturctural Knowledge Graph of Academic Papers

# preprocessing
## Setting
- use `pyhton` version 3.11.0
- use `pip install -r requirements.txt` to install required packages
- **input file**: Default review paper is "Review of information extraction technologies and applications". If you want to change the input file, please refer to the following steps: *(WARNING! Considering that there are still some bugs parsing the PDF, if you want to change the input file, please select a paper where each paragraph starts with a **number**.)*

  ```python
  if __name__ == '__main__':
      filename = 'Review of information extraction technologies and applications'  # the paper you want to input
      pdf = open(f'{filename}.pdf', 'rb')
      reader = PyPDF2.PdfFileReader(pdf, False)
  ```
  1. put the paper in the same folder as `preprocessing.py`
  2. the file name should be the same as the paper title
  3. change the variable `filename` to the paper title
- **Google scholar API key**：Please refer to the following process to apply for an API key.

  ```python
  if __name__ == '__main__':
      filename = 'Review of information extraction technologies and applications'
      ...
      title = filename
      num_pages = reader.numPages
      api_key = ''  # paste your own api key here
  ```
  1. visit website https://serpapi.com/users/sign_in and login
  2. copy the API key and paste it in the variable `api_key`
  
## Run
After runbing `python preprocessing.py`, corresponding to different loggin info, the operation is as follows:
- `Parsing PDF file ...`：Read the review paper and divide the article into separate paragraphs. (except references)
- `Preprocessing and create dictionary ...`：Tokenize and normalize the content of the review paper and create a dictionaty.
- `Crawling citations ...`：Use Google scholar API to crawl all citations of the review paper.
- `Parsing abstracts and update dictionary ...`：Tokenize and normalize the abstract of each cited paper.
- `Finish preprocessing!`

## Output
### `sections`
- type: dictionary
- tokens of each section in the review paper (preserve repeated words and original order)
```
# format
{
    'section title': [token 1, token 2, ...],
}
```
```
# example
{
    'abstract': ['abstract', 'inform', 'extract', 'import', 'grow', 'ﬁeld', 'part', 'develop', ...],
    'introduction': ['introduct', 'background', 'inform', 'extract', 'ﬁeld', 'journal', 'neural', 'comput', ...],
    '1.1 Evolution of the information extraction ﬁeld': ['evolut', 'inform', 'extract', 'ﬁeld', 'histor', 'messag', 'understand', ...],
}
```

### `dictionary`
- type: dictionary
- store all terms
```
# format
{
    'term': <__main__.Term object at 0x000001A2AEB64A50>,
}
```

### `Term`
- type: Class
- each term's information
```python
# definition
class Term:
    def __init__(self):
        self.tf = 0  # term frequency
        self.position = dict()  # {section idx: times}
        self.cite_pos = dict()  # {citation idx: times}
        
    def add_tf(self):
        self.tf += 1
        
    def add_pos(self, idx):
        if idx not in self.position:
            self.position[idx] = 0
        self.position[idx] += 1
        
    def add_cite_pos(self, idx):
        if idx not in self.cite_pos:
            self.cite_pos[idx] = 0
        self.cite_pos[idx] += 1
        
    def get_df(self):  # you can use term.get_dt to access the document frequency of the term
        if len(self.position) > 0:
            return len(self.cite_pos) + 1
        else:
            return len(self.cite_pos)
```

### `citations`
- type: list
- store all citations
```
# format
[<__main__.Citation object at 0x0000013853428F10>, ...]
```

### `Citation`
- type: Class
- each citation's information
```python
# defenition
class Citation:
    def __init__(self, title, link, cited_num):
        self.title = title  # paper title
        self.link = link
        self.cited_by = cited_num  # number of times this article has been cited
        self.tokens = []  # all tokens in each article (may be duplicated)
```
