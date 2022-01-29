import re
from urllib.parse import urlparse
# FILE WITH HELPER FUNCTIONS FOR scraper.py

stopwords = {"how's", 'between', 'their', 'cannot', 'does', "doesn't", 'same', 'of', "couldn't", "you'd", "hadn't", 'most',
    "mustn't", 'be', 'through', 'nor', "he'd", "won't", 'into', 'an', "they'd", "when's", "who's", 'if', "we're", 'below', 'for',
    "haven't", 'only', 'you', 'your', 'then', 'is', "we'll", 'by', 'me', "there's", 'ourselves', "why's", "weren't", "i'd",
    'there', "can't", 'here', 'such', 'were', "isn't", 'up', 'what', 'very', 'yours', 'they', 'herself', 'has', 'with', "you'll",
    'those', 'i', 'myself', "it's", "we've", 'on', 'but', 'it', "you've", "they've", 'or', "they'll", "didn't", 'down', 'should',
    'yourselves', 'am', 'are', 'theirs', 'over', 'having', 'again', "don't", "i'll", 'and', 'who', 'do', 'itself', "she'll", 'whom',
    "that's", 'than', "where's", "he's", 'where', 'she', 'each', 'yourself', 'about', 'other', 'no', 'did', 'until', 'while',
    "here's", 'after', 'hers', 'both', 'off', 'was', "wasn't", 'how', 'our', "shan't", 'from', 'once', "she'd", 'he', 'this',
    'ours', "shouldn't", 'against', 'during', 'these', 'doing', 'more', 'under', 'before', 'some', 'as', "let's", 'its', 'few',
    'because', 'being', "what's", 'would', 'too', 'out', 'so', 'to', 'my', 'have', 'why', 'been', 'all', 'above', 'at', 'had',
    'not', 'when', "i've", 'himself', 'we', "wouldn't", 'them', 'a', "she's", 'could', "you're", 'his', "aren't", 'any',
    "they're", "he'll", "hasn't", 'that', 'further', 'which', 'themselves', "i'm", 'in', 'the', 'own', "we'd", 'ought', 'her',
    'him'}

'''
O(n) where n is the number of tokens in the input file.

Runs over entire file once to gather all the tokens, then
runs over all the tokens again, lowering them all to lower case

O(n) + O(n) = O(n)

Arguments:
htmlstring: string containing html content of page
'''
# ADJUSTED FOR STRING ARGUMENT INSTEAD OF TEXTFILEPATH
def tokenize(htmlstring):
    tokens = re.findall(r'[a-zA-Z0-9\']{3,}', htmlstring) # list of tokens

    # lower tokens before returning
    for i in range(0, len(tokens)):
        tokens[i] = tokens[i].lower()
    return tokens

'''
O(n) where n is the number of tokens in the input

Iterates over all the tokens in the input,
adding it to a dictionary or updating the value if the token already
exists within the dictionary

O(1) look uptime to check for token membership in dictionary or to update existing value

O(n) * O(1) = O(n)

'''
def computeWordFrequencies(tokens):
    frequencies = {}
    for token in tokens:
        if token not in stopwords:
            if token not in frequencies:
                frequencies[token] = 1
            else:
                frequencies[token] += 1
        #if token in stopwords:
        #    print("stopword: " + token)
    return frequencies

'''
Argument:
visited_pages from scraper.py

returns a dictionary with the total count for each word across all crawled urls
'''
def allWordFrequencies(pages):
    frequencies = {}
    for url in pages:
        for word in pages[url]:
            if word not in frequencies:
                frequencies[word] = pages[url][word]
            else:
                frequencies[word] += pages[url][word]
    return frequencies

'''
Argument:
output of allWordFrequencies

Returns a list of top 50 words ordered by frequency (descending)
'''
def maxFifty(frequencies):
    top50 = []
    for i in range(50):
        topword = max(frequencies.items(), key=lambda x: x[1])
        top50.append(topword[0])
        del frequencies[topword[0]]
    return top50

def deqf(url):
    parsed = urlparse(url)
    return parsed._replace(fragment="").geturl()
    #return parsed.scheme + "://" + parsed.netloc + parsed.path