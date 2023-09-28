from serpapi import GoogleSearch
import requests


##### search page #####
params = {
  "engine": "google_scholar",
  "q": "biology",
  "api_key": "1f0dbcedc450cae96f25b4827e928b936bade3de2e148851ddac25366d461f8d"
}

req = requests.get(
   url='https://serpapi.com/search?engine=google_scholar',
   params=params
)

search = GoogleSearch(params)
results = search.get_dict()
organic_results = results["organic_results"]
# print(organic_results)
# print(organic_results[0]['snippet'])



# ##### cite API #####
# params = {
#   "engine": "google_scholar_cite",
#   "q": "",  # paper's result_id
#   "api_key": ""
# }

# search = GoogleSearch(params)
# results = search.get_dict()
# citations = results["citations"]