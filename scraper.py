import re
from urllib.parse import urlparse
from lxml import html
from lxml.html.clean import Cleaner
from helper import tokenize, computeWordFrequencies, allWordFrequencies, maxFifty, deqf

# global data structures
DUPLICATE_THRESHOLD = 0.75
visited_pages = dict()
longest_page = {"url" : "http://www.ics.uci.edu", "number of words" : 0}
iue_subdomains = dict() # urls : num of unique pages
fingerprints = set()

# variables for debugging
DEBUG = True

# for reporting global variables results at end of crawl, will be called in launch.py
# only prints report during DEBUGGING
def report():
    if DEBUG:
        # 1, num of UNIQUE pages visited
        print("Report Question #1:")
        print(f"Visited {len(visited_pages)} UNIQUE pages")
        # 2, stop words are excluded from count
        print("Report Question #2:")
        print(f"Longest page: {longest_page['url']}")
        print(f"Number of words: {longest_page['number of words']}")
        # 3, most common 50 words
        print("Report Question #3:")
        frequencies = allWordFrequencies(visited_pages)
        print(maxFifty(frequencies))
        # 4, ics.uci.edu subdomains
        print("Report Question #4:")
        print(sorted(iue_subdomains.items()))

        

def scraper(url, resp):
    links = extract_next_links(url, resp)

    # links from extract_next_links that pass validation check
    #return [link for link in links]   #[link for link in links if is_valid(link)]
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    # RETURNS EMPTY LIST OF URLS FOR EMPTY RESPONSE(?)
    
    '''-----------------------------------------------------------'''
    global visited_pages, longest_page, fingerprints
    visited_pages[url] = {} # visited_page with error might cause problems? if dictionary isn't properly formatted
    # checking for status 200 OK
    if resp.status != 200:
        return list()

    # read HTML from resp.raw_response.content for report
    # read urls before clean
    source_code = html.fromstring(resp.raw_response.content)
    links = source_code.xpath('//a/@href') # list of all links on current page

    # clean html for text reading
    cleaner = Cleaner(scripts=True, style=True) # cleaner for removing scripts and style tags/content
    cleanedhtml = cleaner.clean_html(resp.raw_response.content) # type bytes (same as resp.raw_response.content)
    source_code = html.fromstring(cleanedhtml)
    textcontent = str(source_code.text_content())
    
    tokens = tokenize(textcontent) # list
    #tokens = computeWordFrequencies(tokens) # dictionary

    # store fingerprint for current url
    cur_fp = compute_fingerprint(tokens)
    #print("cur_fp len: " + str(len(cur_fp)))
    if len(cur_fp) == 0 or detect_near_similars(cur_fp):
        print("SIMILARTY DETECTED")
        return list()
    else:
        fingerprints.add(tuple(cur_fp))

    # update globals
    tokens = computeWordFrequencies(tokens) # dictionary
    visited_pages[url] = tokens # update visited_pages
    
    wordtotal = sum(visited_pages[url].values())
    if wordtotal > longest_page["number of words"]: # update longest_page if needed
        longest_page["url"] = url
        longest_page["number of words"] = wordtotal

    parsed = urlparse(url)
    domain = parsed.scheme + "://" + parsed.netloc
    if "ics.uci.edu" in domain:
        if domain in iue_subdomains:
            iue_subdomains[domain] += 1
        else:
            iue_subdomains[domain] = 1


    #print(type(url))    
    # defragment and dequery urls
    #links = [urldefrag(url)[0] for url in links] # urldefrag returns a named tuple (defragmented url, fragment)
    links = [deqf(url) for url in links]

    return links

# handle relative vs absolute urls
# check if under valid domains
# check for subdomains
def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    try:
        parsed = urlparse(url)
        
        if url in visited_pages:
            return False
        if parsed.scheme not in set(["http", "https"]):
            return False
        if re.match(r"^\.today\.uci\.edu", parsed.netloc): # NOT SURE, NEED TO DOUBLE CHECK
            if not re.match(r"^department\/information_computer_sciences\/.*$", parsed.path):
                return False
        if not re.match(r"^.*\.(ics\.uci\.edu|cs\.uci\.edu|informatics\.uci\.edu|stats\.uci\.edu|today\.uci\.edu)$", parsed.netloc):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


# takes in a fingerprint and checks fingerprint dictionary for a match
# Arguments: 
# cur_fp, list of integers representing the fingerprint
def detect_near_similars(cur_fp):
    global fingerprints
    for fp in fingerprints:
        if similar(fp, cur_fp):
            return True
    return False


def similar(A, B):
    global DUPLICATE_THRESHOLD
    card_union = len([i for i in A if i in B])
    s = card_union / (len(A) + len(B) - card_union)
    if s >= DUPLICATE_THRESHOLD:
        print("Similarity Factor:", s)
        return True
    else:
        return False
    #return s >= DUPLICATE_THRESHOLD


#detect near duplicates using fingerprint method
def compute_fingerprint(tokens):
    triple_lst = []
    #print(tokens)
    # add triplets to triple_lst
    for i in range(len(tokens)-2):
        triple_lst.append([tokens[i], tokens[i+1], tokens[i+2]])
    
    # hash each triplet
    hashed_lst = [fingerprint_hash(lst) for lst in triple_lst]
    res = [v for v in hashed_lst if v % 4 == 0]
    return res


def fingerprint_hash(word):
    res = 0
    for w in word:
        for c in w:
            res += ord(c)
    return res