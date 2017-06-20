import requests
from bs4 import BeautifulSoup

def process_old2new(old_text):
    r = requests.post('http://web-corpora.net/wsgi/tolstoi_translit.wsgi/', data={'inp_text': old_text.encode('utf-8'), 'go':'Транслитерировать'})
    res = r.content.decode('utf-8')
    soup = BeautifulSoup(res, 'html5lib')
    new_text = soup.findAll('textarea')[1].string.strip()
    return new_text

