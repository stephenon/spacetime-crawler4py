
from lxml import html

if __name__ == "__main__":
    source_code = html.parse("index.html")
    #print(type(source_code))
    print(source_code.text_content())
    #print(source_code.xpath("string()"))

    links = source_code.xpath('//a/@href') # list of all links on current page

'''
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
if __name__ == "__main__":
    print(len(stopwords))
'''