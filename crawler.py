import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
from selenium.webdriver.chrome.options import Options
import re

# response = requests.get("https://openaccess.thecvf.com/content/CVPR2021/html/Reddy_Im2Vec_Synthesizing_Vector_Graphics_Without_Vector_Supervision_CVPR_2021_paper.html")
# soup = BeautifulSoup(response.text, "html.parser")
# # print(soup.prettify())

# for child in soup.descendants:
#     if 'vector graphics' in child.text:
#         print(child)

# -----------------------------------------------------

# link = "https://www.sciencedirect.com/science/article/pii/S1532046417302563"

# # options = Options()
# # options.add_argument('--headless')
# # options.add_argument('--disable-gpu')
# # options.add_argument("--window-size=1920,1080")

# service_object = Service(binary_path)
# driver = webdriver.Chrome(service=service_object)
# driver.get(link)

# time.sleep(3)

# # html_text=driver.page_source
# # soup = BeautifulSoup(html_text, 'html.parser')
# # t = soup.find('Abstract')

# # for child in soup.descendants:
# #     if 'abstract' in 


# t = driver.find_element(By.XPATH, '//*[text()="Abstract"]/following-sibling::*[1]')
# print(t.text)

# driver.quit()

# ---------------------------------------------------------------------

link = "https://www.sciencedirect.com/science/article/pii/S1532046417302563"

service_object = Service(binary_path)
driver = webdriver.Chrome(service=service_object)
driver.get(link)
time.sleep(3)


# driver.find_element(By.XPATH, "//button[@data-selenium-selector='text-truncator-toggle']").click()

html_text=driver.page_source
soup = BeautifulSoup(html_text, 'html.parser')
t = soup.select(".abstract.author")
# print(t is None)
print(t[0].text)
