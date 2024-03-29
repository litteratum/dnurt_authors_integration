import bs4 as bs
from dnurt_integration.dnurtdb import database as db
import requests
from dnurt_integration.shared import updating_status


class GscholarAuthor:
    def __init__(self, _id):
        self.gs_id = _id
        self.doc_count = 0
        self.h_index = 0

    @property
    def gs_id(self):
        return self._gs_id

    @gs_id.setter
    def gs_id(self, val):
        self._gs_id = val

    @property
    def h_index(self):
        return self._h_index

    @h_index.setter
    def h_index(self, val):
        self._h_index = val


def get_author_by_id(_id):
    source = \
        requests.get('https://scholar.google.com.ua/citations?user={}&hl=en'
                     .format(_id)).content
    soup = bs.BeautifulSoup(source, 'lxml')
    tds = soup.find_all('td')

    author = GscholarAuthor(_id)
    author.h_index = tds[4].string

    return author


def update_db():
    ids = db.get_gs_authors_ids()
    lend = len(ids)
    current = 1
    updating_status[5] = lend
    for _id in ids:
        author = get_author_by_id(_id)
        if author:
            db.gscholar_update(author)
        updating_status[4] = current
        current += 1

    db.disconnect()
