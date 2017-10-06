import requests
from bs4 import BeautifulSoup
import itertools as it


class Posting(object):
    def __init__(title, url, description):
        self.title = title
        self.url = url
        self.description = description

    def format_row():
        return '{}, {}, {}'.format(self.title, self.description, self.url)


def collect_postings():
    # the postings page for rozee.pk is paginated into
    # sets of 20
    total_jobs = 765
    pg_interval = 20
    
    def unwrap_url(href):
        return href[2:].split('?')[0]
    def extract_posting_urls(url):
        r = requests.get(url)
        assert r.status_code == 200, (r.status_code, r.text)
        s = BeautifulSoup(r.text, 'html.parser')
        postings = s.find_all("h3", class_="s-18")
        #print('postings found: {}'.format(postings))
        urls = (unwrap_url(p.a['href']) for p in postings)
        yield from urls
    
    base = 'https://www.rozee.pk/category/software-web-development-jobs/?fpn={}'
    urls = (base.format(fpn) for fpn in range(0, 765, 20))
    jobs = it.chain(extract_posting_urls(url) for url in urls)
    for j in jobs:
        print(j)

if __name__ == '__main__':
    collect_postings()
    


