from lxml import html

if __name__ == "__main__":
    source_code = html.parse("index.html")
    #print(type(source_code))
    #print(source_code.text_content())
    print(source_code.xpath("string()"))
    links = source_code.xpath('//a/@href') # list of all links on current page