import requests
from lxml.html.clean import Cleaner
from lxml import html, etree
from helper import *
from scraper import *
from sys import getsizeof
from detection import *

evoke = "https://evoke.ics.uci.edu/about/the-evoke-studio/"
url1 = "https://wics.ics.uci.edu/events/2021-03-02/"
#url1 = "https://evoke.ics.uci.edu/qs-personal-data-landscapes-poster"
url2 = "https://wics.ics.uci.edu/events/2020-10-09/"
deadurl = "http://flamingo.ics.uci.edu/._.DS_Store"



# dres = requests.get(deadurl)

# try:
#     html.fromstring(dres.content)
#     print("tesT" + 1)
# except etree.ParserError:
#     pass
#print(type(dres.content))
#print(dres.content == 0)
#print(dres.content.isEmpty())

'''
# GETTING FINGERPRINT FOR URL 1
res = requests.get(url1)

cleaner = Cleaner(scripts=True, style=True) # cleaner for removing scripts and style tags/content
cleanedhtml = cleaner.clean_html(res.content)
#print("SIZE OF URL #1:", getsizeof(res.content))

# response = requests.head(url1)
# print(response.headers)
# print(response.headers['Content-Length'])

source_code = str(html.fromstring(cleanedhtml).text_content())
tokens1 = tokenize(source_code)
fp1 = compute_fingerprint(tokens1)
print("Fingerprint of URL #1:")
print(fp1)

# GETTING FINGERPRINT FOR URL 2
res2 = requests.get(url2)

#cleaner = Cleaner(scripts=True, style=True) # cleaner for removing scripts and style tags/content
cleanedhtml2 = cleaner.clean_html(res2.content)
source_code2 = str(html.fromstring(cleanedhtml2).text_content())
tokens2 = tokenize(source_code2)
fp2 = compute_fingerprint(tokens2)
print("Fingerprint of URL #2:")
print(fp2)

print("SIMILAR: ", similar(fp1, fp2))

'''