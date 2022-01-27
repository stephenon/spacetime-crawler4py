import re
from urllib.parse import urlparse, urldefrag
from lxml import html
from lxml.html.clean import Cleaner
from helper import tokenize, computeWordFrequencies

# global data structures
# visited_pages = set()
# VISITED_PAGES CHANGED TO DICTIONARY
visited_pages = {}


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
    #visited_pages.add(url)
    # TODO: just urls(hyperlinks) from page
    # checking for status 200 OK
    if resp.status != 200:
        return list()

    # read HTML from resp.raw_response.content
    # read urls before clean
    source_code = html.fromstring(resp.raw_response.content)
    links = source_code.xpath('//a/@href') # list of all links on current page

    # clean html for text reading
    cleaner = Cleaner(scripts=True, style=True) # cleaner for removing scripts and style tags/content
    cleanedhtml = cleaner.clean_html(resp.raw_response.content) # type bytes (same as resp.raw_response.content)
    source_code = html.fromstring(cleanedhtml)
    textcontent = str(source_code.text_content())
    
    tokens = tokenize(textcontent)
    tokens = computeWordFrequencies(tokens)
    print(tokens)
    #print(source_code.text_content()) # after clean
    
    # defragment urls
    links = [urldefrag(url)[0] for url in links] # urldefrag returns a named tuple (defragmented url, fragment)

    # extract information from content for report
    # 

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
