import requests
from bs4 import BeautifulSoup
'''thanks google bard!'''
def find_rss_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    rss_links = []
    for link in soup.find_all("a"):
        if link.has_attr("href") and "rss" in link["href"]:
            rss_links.append(link["href"])

    # print (f"{rss_links} - {type(rss_links)}")
    return rss_links

if __name__ == "__main__":
    url = "https://www.bbc.com/news"
    rss_links = find_rss_links(url)

    for rss_link in rss_links:
        print(rss_link)
