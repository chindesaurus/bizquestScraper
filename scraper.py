#!/usr/bin/python
import sys
import codecs
import urllib2
from bs4 import BeautifulSoup

# sentinel value
totalPages = -1

def getPages(soup):
    global totalPages
    if totalPages == -1:
        # get the number of pages to search
        pages = soup.find('p', 'paging')
        pages = str(pages.text).strip()
        pages = pages.replace("Page 1 of ", "")
        totalPages = int(pages)


def getAskingprice(soup):
    # find all li with class="askingprice"
    askingprice = [li.string or li.span.string for li in soup.find_all('li', "askingprice")]

    # strip whitespace, deal with featured entries wrapped in a span, then return
    askingprice = [x.contents if 'span' in x else x.strip() for x in askingprice]
    return askingprice


def getCashflow(soup):
    # find all li with class="cashflow"
    cashflow = [li.string for li in soup.find_all('li', "cashflow")]

    # strip whitespace and return
    cashflow = [x.strip() for x in cashflow]
    return cashflow


def getLocation(soup):
    location = soup.find_all('li', 'location')
    location.pop(0) # erroneous first entry
    location = [x.text.strip() for x in location]
    return location

def getNames(soup):
    # business names are in anchor tags within h2's
    names = [h2.a.get_text() for h2 in soup.find_all('div', 'colLeft')]
    
    # strip whitespace and make sure everything is UTF encoded
    names = [x.strip().encode('utf-8') for x in names]
    return names;


def main():
    
    # start at page 1 and go through all available pages
    p = 1
    while True:
        # grab the page and prepare for parsing/scraping
        page = urllib2.urlopen('http://www.bizquest.com/buy-a-business-for-sale/page-' + str(p))
        html = page.read()
        soup = BeautifulSoup(html, fromEncoding="ASCII")
        getPages(soup)

        # print names of businesses
        names = getNames(soup)
        for n in names:
            print(n)

        # print asking prices
        askingprice = getAskingprice(soup)
        for a in askingprice:
            print(a)

        # print cashflows
        cashflow = getCashflow(soup)
        for c in cashflow:
            print(c)
        
        # get locations in format: City, State (eg Boston, MA)
        city = []
        state = []
        location = getLocation(soup)
        for loc in location:
            # if there's no comma, the listed location is just a state
            if "," not in loc:
                city.append("")
                state.append(loc)
            # otherwise separate out the city and state
            else:
                # use the position of the comma to slice
                i = loc.index(',')
                city.append(loc[:i])
                state.append(loc[i+2:])
        # print city and state
        for c in city:
            print(c)
        for s in state:
            print(s)
        
        # go to the next page, or break if we're on the last page
        p += 1
        if (p > totalPages):
            break;
      

if __name__ == "__main__":
    main()
